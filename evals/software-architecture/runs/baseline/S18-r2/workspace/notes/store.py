"""The only module that knows how notes are stored (ADR-0001, ADR-0003)."""
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from notes.model import Note

# Columns in the order _note() expects them.
_COLUMNS = "id, text, created, tags"


def default_path():
    return Path(os.environ.get("NOTES_DB", Path.home() / ".notes.db"))


def _note(row):
    id_, text, created, tags = row
    return Note(id_, text, created, tuple(t for t in tags.split(",") if t))


class Store:
    def __init__(self, path):
        self._db = sqlite3.connect(path)
        self._db.execute("CREATE TABLE IF NOT EXISTS notes "
                         "(id INTEGER PRIMARY KEY, text TEXT NOT NULL, created TEXT NOT NULL, "
                         "tags TEXT NOT NULL DEFAULT '')")
        # Stores created before tags existed lack the column; migrate them in place (ADR-0004).
        columns = {row[1] for row in self._db.execute("PRAGMA table_info(notes)")}
        if "tags" not in columns:
            with self._db:
                self._db.execute("ALTER TABLE notes ADD COLUMN tags TEXT NOT NULL DEFAULT ''")

    def add(self, text, tags=()):
        for tag in tags:
            if not tag or "," in tag:
                raise ValueError(f"invalid tag {tag!r}: tags must be non-empty and contain no comma")
        created = datetime.now(timezone.utc).isoformat(timespec="seconds")
        joined = ",".join(tags)
        with self._db:
            cur = self._db.execute("INSERT INTO notes (text, created, tags) VALUES (?, ?, ?)",
                                   (text, created, joined))
        return Note(cur.lastrowid, text, created, tuple(tags))

    def all(self, tag=None):
        if tag is None:
            rows = self._db.execute(f"SELECT {_COLUMNS} FROM notes ORDER BY id")
        else:
            rows = self._db.execute(f"SELECT {_COLUMNS} FROM notes "
                                    "WHERE instr(',' || tags || ',', ?) > 0 ORDER BY id",
                                    (f",{tag},",))
        return [_note(row) for row in rows]

    def search(self, term):
        rows = self._db.execute(f"SELECT {_COLUMNS} FROM notes WHERE text LIKE ? ORDER BY id DESC",
                                (f"%{term}%",))
        return [_note(row) for row in rows]

    def close(self):
        self._db.close()
