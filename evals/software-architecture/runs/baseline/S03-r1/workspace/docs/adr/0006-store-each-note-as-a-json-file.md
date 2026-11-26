# 6. Store each note as one JSON file

## Status

accepted 2026-11-21, supersedes [ADR-0001](0001-use-sqlite-for-storage.md)

## Context

SQLite files are binary. They are hard to diff and cannot be repaired with a text editor, which
the users and maintainers need when a store goes wrong. Crash safety must still hold (R-2, QG-1,
QS-1), and the program may use only the Python standard library (R-3, QG-2). The `json` module
is in the standard library, and ADR-0004 already gives an atomic write for any file the store
writes.

A second storage engine is not wanted: ADR-0005 (PostgreSQL) is rejected, because a server
database contradicts R-3.

## Decision

The store keeps each note in its own file in one directory:

- the directory is `~/.notes/` by default; the environment variable `NOTES_DIR` sets another one;
- the file name is `<id>.json`, where `<id>` is the note's integer id;
- the file holds one JSON object with the keys `id` (integer), `text` (string) and `created`
  (ISO 8601 UTC timestamp, whole seconds);
- a new note gets the id one higher than the highest existing id, starting at 1;
- every file is written as ADR-0004 requires: temporary file in the same directory, `os.fsync`,
  then `os.replace`.

Only `notes/store.py` reads or writes these files (ADR-0003).

## Consequences

- Each note can be read, diffed and repaired with a text editor.
- A crash leaves each note either fully written or absent, as before.
- `os.replace` overwrites silently, so creating a note must not replace an existing file. The
  mechanism is left to the building block.
- Search reads every note file. This is acceptable for the current use (R-1) and is the first
  place to look if search becomes slow.
- The `NOTES_DB` variable, the file `~/.notes.db` and the `notes` table are gone. Migrating an
  existing `~/.notes.db` is not decided in this ADR and needs its own decision.
