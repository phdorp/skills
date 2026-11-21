"""Durable storage in a single SQLite file.

Durability model (requirement 2, "no sighting is lost"):
  * Every write is one explicit transaction (BEGIN IMMEDIATE ... COMMIT).
    SQLite either commits the whole row or none of it, so a crash or power
    loss mid-write leaves the database as it was before the command.
  * synchronous=FULL makes COMMIT return only after data is on disk.
  * Nothing is ever rewritten in place outside a transaction, so there is
    no separate file that can be half-written.

This module is the only place that knows about SQL.
"""

import sqlite3
import time
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from typing import Iterator

from birdlog.model import Sighting

SCHEMA_VERSION = 1

_SCHEMA_V1 = [
    """
    CREATE TABLE sightings (
        id            INTEGER PRIMARY KEY,
        species       TEXT    NOT NULL,
        place         TEXT    NOT NULL,
        observed_at   INTEGER NOT NULL,  -- UTC epoch seconds
        utc_offset_min INTEGER NOT NULL,
        count         INTEGER NOT NULL CHECK (count > 0),
        created_at    INTEGER NOT NULL   -- UTC epoch seconds, when logged
    )
    """,
    # Serves "latest first" listing without a full scan or sort.
    "CREATE INDEX sightings_by_time ON sightings (observed_at DESC, id DESC)",
]

_MIGRATIONS = {1: _SCHEMA_V1}


class Store:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        # isolation_level=None: we manage transactions explicitly via _tx().
        self._conn = sqlite3.connect(path, timeout=5.0, isolation_level=None)
        self._conn.execute("PRAGMA synchronous=FULL")
        self._migrate()

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Connection]:
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            yield self._conn
        except BaseException:
            self._conn.execute("ROLLBACK")
            raise
        else:
            self._conn.execute("COMMIT")

    def _migrate(self) -> None:
        current = self._conn.execute("PRAGMA user_version").fetchone()[0]
        if current > SCHEMA_VERSION:
            raise RuntimeError(
                f"database schema v{current} is newer than this birdlog (v{SCHEMA_VERSION})"
            )
        with self._tx() as c:
            # Re-check inside the write lock in case another process migrated.
            current = c.execute("PRAGMA user_version").fetchone()[0]
            for version in range(current + 1, SCHEMA_VERSION + 1):
                for statement in _MIGRATIONS[version]:
                    c.execute(statement)
            if current != SCHEMA_VERSION:
                c.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")

    def add(self, sighting: Sighting) -> Sighting:
        with self._tx() as c:
            cur = c.execute(
                "INSERT INTO sightings "
                "(species, place, observed_at, utc_offset_min, count, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    sighting.species,
                    sighting.place,
                    sighting.observed_at,
                    sighting.utc_offset_min,
                    sighting.count,
                    int(time.time()),
                ),
            )
            return replace(sighting, id=cur.lastrowid)

    def latest(self, limit: int | None = None) -> list[Sighting]:
        """Most recent observation first. limit=None returns everything."""
        rows = self._conn.execute(
            "SELECT id, species, place, observed_at, utc_offset_min, count "
            "FROM sightings ORDER BY observed_at DESC, id DESC LIMIT ?",
            (-1 if limit is None else limit,),
        )
        return [_row_to_sighting(r) for r in rows]

    def all_chronological(self) -> list[Sighting]:
        rows = self._conn.execute(
            "SELECT id, species, place, observed_at, utc_offset_min, count "
            "FROM sightings ORDER BY observed_at ASC, id ASC"
        )
        return [_row_to_sighting(r) for r in rows]


def _row_to_sighting(row: tuple) -> Sighting:
    id_, species, place, observed_at, offset, count = row
    return Sighting(
        species=species,
        place=place,
        observed_at=observed_at,
        utc_offset_min=offset,
        count=count,
        id=id_,
    )
