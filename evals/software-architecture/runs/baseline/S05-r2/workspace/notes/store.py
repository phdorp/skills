"""The only module that knows how notes are stored (ADR-0004, ADR-0003).

Each note is one UTF-8 text file, `<id>.txt`, in the notes directory. The id is the creation
time in UTC, so sorting by id sorts by creation time.
"""
import os
import re
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from notes.model import Note

ID_FORMAT = "%Y%m%dT%H%M%S%fZ"
ID_PATTERN = re.compile(r"\d{8}T\d{12}Z")


def default_path():
    return Path(os.environ.get("NOTES_DIR", Path.home() / ".notes"))


def utc_now():
    return datetime.now(timezone.utc)


class Store:
    def __init__(self, directory):
        self._dir = Path(directory)
        self._dir.mkdir(parents=True, exist_ok=True)

    def add(self, text):
        when = utc_now()
        while True:
            note_id = when.strftime(ID_FORMAT)
            try:
                self._write(note_id, text)
                break
            except FileExistsError:  # another note has this id; take the next microsecond
                when += timedelta(microseconds=1)
        return Note(note_id, text, when.isoformat(timespec="seconds"))

    def all(self):
        return self._load(lambda text: True)

    def search(self, term):
        needle = term.lower()
        return self._load(lambda text: needle in text.lower())

    def _load(self, keep):
        found = []
        for path in self._note_files():
            text = path.read_text(encoding="utf-8").removesuffix("\n")
            if keep(text):
                found.append(_note_from(path.stem, text))
        return found

    def _note_files(self):
        files = [p for p in self._dir.glob("*.txt")
                 if ID_PATTERN.fullmatch(p.stem) and p.is_file()]
        return sorted(files, key=lambda p: p.stem, reverse=True)

    def _write(self, note_id, text):
        """Store the note completely or not at all: write a hidden temporary file, flush it to
        disk, then hard-link it to its final name. link() fails instead of overwriting."""
        final = self._dir / f"{note_id}.txt"
        fd, tmp = tempfile.mkstemp(dir=self._dir, prefix=".", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(text + "\n")
                f.flush()
                os.fsync(f.fileno())
            os.link(tmp, final)
            _fsync_dir(self._dir)
        finally:
            os.unlink(tmp)


def _note_from(note_id, text):
    created = datetime.strptime(note_id, ID_FORMAT).replace(tzinfo=timezone.utc)
    return Note(note_id, text, created.isoformat(timespec="seconds"))


def _fsync_dir(directory):
    fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
