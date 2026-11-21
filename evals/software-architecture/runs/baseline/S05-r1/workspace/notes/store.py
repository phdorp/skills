"""The only module that knows how notes are stored (ADR-0004, ADR-0003).

Each note is one UTF-8 text file in the notes directory, named after its creation time
(`20261121T101500123456Z.txt`), so any text editor can read and edit it.
"""
import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from notes.model import Note

_NAME_FORMAT = "%Y%m%dT%H%M%S%fZ"


def default_path():
    return Path(os.environ.get("NOTES_DIR", Path.home() / ".notes"))


def _iso(moment):
    return moment.isoformat(timespec="seconds")


class Store:
    def __init__(self, directory):
        self._dir = Path(directory)
        self._dir.mkdir(parents=True, exist_ok=True)

    def add(self, text):
        created = datetime.now(timezone.utc)
        path = self._dir / f"{created.strftime(_NAME_FORMAT)}.txt"
        while path.exists():  # two notes created in the same microsecond
            created += timedelta(microseconds=1)
            path = self._dir / f"{created.strftime(_NAME_FORMAT)}.txt"
        self._write_atomic(path, text)
        return Note(path.stem, text, _iso(created))

    def all(self):
        """All notes, newest first."""
        return [note for _, note in sorted(self._entries(), key=lambda e: e[0], reverse=True)]

    def search(self, term):
        """Notes containing `term` (case-insensitive), oldest first."""
        needle = term.casefold()
        return [note for _, note in sorted(self._entries(), key=lambda e: e[0])
                if needle in note.text.casefold()]

    def _entries(self):
        for path in self._dir.glob("*.txt"):
            try:
                created = datetime.strptime(path.stem, _NAME_FORMAT).replace(tzinfo=timezone.utc)
            except ValueError:  # a file made by hand: use its modification time
                created = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            text = path.read_text(encoding="utf-8")
            if text.endswith("\n"):
                text = text[:-1]
            yield created, Note(path.stem, text, _iso(created))

    def _write_atomic(self, path, text):
        # Write to a temporary file, then rename it into place: a crash leaves either
        # the whole note or no note (QS-1). Temporary files do not end in ".txt".
        fd, tmp = tempfile.mkstemp(dir=self._dir, prefix=".", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(text + "\n")
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
        except BaseException:
            os.unlink(tmp)
            raise
