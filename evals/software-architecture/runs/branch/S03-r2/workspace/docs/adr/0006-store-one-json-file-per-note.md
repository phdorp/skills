# 6. Store one JSON file per note

## Status

proposed

## Context

This ADR replaces ADR-0001 (Use SQLite for storage). SQLite files are binary, hard to diff, and
hard to repair by hand. Users must be able to inspect and repair their notes with a text editor
and standard tools.

Notes must survive crashes (R-2, QG-1, QS-1). The program may use only the Python standard
library (R-3, QG-2). The store is the only block that knows the storage (QG-3, QS-3, ADR-0003).

## Decision

Store each note as its own JSON file, named `<id>.json`, in one directory. The default directory
replaces `~/.notes.db`; the `NOTES_DB` override is replaced by a directory override.

Every note file is written as ADR-0004 requires: temporary file in the same directory, `os.fsync`,
then `os.replace`.

The store reads and writes JSON with the standard `json` module.

## Consequences

- Replaces ADR-0001 when accepted. ADR-0001 keeps `accepted` until then.
- A crash during `add` leaves either the note's file or no file, never a partial file (QS-1).
- Each `add` writes one file and costs one `fsync`, as ADR-0004 describes.
- `all` and `search` read every note file. Their cost on large collections is not measured here.
- ADR-0003 (accepted) says only `notes/store.py` imports `sqlite3`. The rule still holds with
  `json` and `os` in its place; its wording is outdated and is not changed here.
- The note ID scheme and the directory default path are part of the on-disk format, which
  ADR-0002 decides centrally. They are proposed here and need the architect's approval.
