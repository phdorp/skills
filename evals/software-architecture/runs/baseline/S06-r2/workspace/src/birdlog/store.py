"""Durable sighting storage backed by SQLite (stdlib ``sqlite3`` only).

Durability model
----------------
* Each ``add`` is a single INSERT in autocommit mode. ``add`` returns only
  after SQLite has committed it.
* ``journal_mode=WAL`` plus ``synchronous=FULL`` means a committed row
  survives a power cut or kernel panic, and an interrupted write leaves
  the database in its last committed state (never a half-written row).
* A sighting the user was told was logged is therefore never lost. A write
  that did not return successfully may or may not be present; the caller
  was never told it succeeded.
"""

from __future__ import annotations

import os
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Union

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS sightings (
    id              INTEGER PRIMARY KEY,
    species         TEXT    NOT NULL,
    location        TEXT    NOT NULL,
    count           INTEGER NOT NULL CHECK (count > 0),
    observed_at     INTEGER NOT NULL,   -- UTC epoch seconds
    utc_offset_min  INTEGER NOT NULL,   -- local offset at observation time
    latitude        REAL,
    longitude       REAL,
    created_at      INTEGER NOT NULL    -- UTC epoch seconds, when it was logged
);
CREATE INDEX IF NOT EXISTS sightings_latest
    ON sightings (observed_at DESC, id DESC);
"""

_COLUMNS = "id, species, location, count, observed_at, utc_offset_min, latitude, longitude"


@dataclass(frozen=True)
class Sighting:
    species: str
    location: str
    count: int
    observed_at: datetime  # must be timezone-aware
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    id: Optional[int] = None


class Store:
    """Owns one SQLite connection. Use as a context manager or call ``close``."""

    def __init__(self, path: Union[str, os.PathLike]) -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # isolation_level=None: autocommit, so every statement is its own
        # transaction and nothing sits in an open buffer.
        self._conn = sqlite3.connect(self._path, timeout=5.0, isolation_level=None)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=FULL")
        self._migrate()

    def _migrate(self) -> None:
        version = self._conn.execute("PRAGMA user_version").fetchone()[0]
        if version > SCHEMA_VERSION:
            raise RuntimeError(
                f"database schema v{version} is newer than this birdlog (v{SCHEMA_VERSION})"
            )
        if version < SCHEMA_VERSION:
            # CREATE ... IF NOT EXISTS keeps this idempotent if interrupted.
            self._conn.executescript(_SCHEMA)
            self._conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")

    def add(self, sighting: Sighting) -> int:
        """Persist a sighting and return its id. Returns only once committed."""
        observed = sighting.observed_at
        offset = observed.utcoffset()
        if offset is None:
            raise ValueError("observed_at must be timezone-aware")
        cur = self._conn.execute(
            "INSERT INTO sightings (species, location, count, observed_at, "
            "utc_offset_min, latitude, longitude, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                sighting.species,
                sighting.location,
                sighting.count,
                int(observed.timestamp()),
                int(offset.total_seconds() // 60),
                sighting.latitude,
                sighting.longitude,
                int(time.time()),
            ),
        )
        return int(cur.lastrowid)

    def latest(self, limit: Optional[int] = None) -> List[Sighting]:
        """Most recently observed first. Ties broken by newest id."""
        return self._select("ORDER BY observed_at DESC, id DESC", limit)

    def chronological(self) -> List[Sighting]:
        """Oldest observation first. Used for exports."""
        return self._select("ORDER BY observed_at ASC, id ASC", None)

    def _select(self, order_by: str, limit: Optional[int]) -> List[Sighting]:
        sql = f"SELECT {_COLUMNS} FROM sightings {order_by}"
        params: tuple = ()
        if limit is not None:
            sql += " LIMIT ?"
            params = (limit,)
        return [_from_row(r) for r in self._conn.execute(sql, params)]

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


def _from_row(row: tuple) -> Sighting:
    sid, species, location, count, epoch, offset_min, lat, lon = row
    tz = timezone(timedelta(minutes=offset_min))
    return Sighting(
        species=species,
        location=location,
        count=count,
        observed_at=datetime.fromtimestamp(epoch, tz),
        latitude=lat,
        longitude=lon,
        id=sid,
    )
