"""The only module that knows how notes are stored (ADR-0001, ADR-0003)."""
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from notes.model import Note


def default_path():
    return Path(os.environ.get("NOTES_DB", Path.home() / ".notes.db"))


class Store:
    def __init__(self, path):
        self._db = sqlite3.connect(path)
        self._db.execute("CREATE TABLE IF NOT EXISTS notes "
                         "(id INTEGER PRIMARY KEY, text TEXT NOT NULL, created TEXT NOT NULL)")
        columns = {row[1] for row in self._db.execute("PRAGMA table_info(notes)")}
        if "tags" not in columns:
            with self._db:
                self._db.execute("ALTER TABLE notes ADD COLUMN tags TEXT NOT NULL DEFAULT ''")

    def add(self, text, tags=()):
        created = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with self._db:
            cur = self._db.execute("INSERT INTO notes (text, created, tags) VALUES (?, ?, ?)",
                                   (text, created, ",".join(tags)))
        return Note(cur.lastrowid, text, created, tuple(tags))

    def all(self, tag=None):
        notes = self._query("SELECT id, text, created, tags FROM notes ORDER BY id", ())
        return [n for n in notes if tag is None or tag in n.tags]

    def search(self, term):
        return self._query("SELECT id, text, created, tags FROM notes WHERE text LIKE ? ORDER BY id DESC",
                           (f"%{term}%",))

    def _query(self, sql, params):
        return [Note(id, text, created, tuple(t for t in tags.split(",") if t))
                for id, text, created, tags in self._db.execute(sql, params)]

    def close(self):
        self._db.close()
