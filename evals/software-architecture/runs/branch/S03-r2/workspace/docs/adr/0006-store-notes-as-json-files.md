# 6. Store each note as one JSON file

## Status

proposed

## Context

This ADR replaces ADR-0001 (use SQLite for storage). ADR-0001 stays accepted until this ADR is
accepted.

The architect moved off SQLite because SQLite files are binary: they are hard to diff and to
repair by hand. Notes must still survive crashes (R-2, QG-1, QS-1), and the program may still
use only the Python standard library (R-3, QG-2). Each file write follows ADR-0004.

## Decision

Store each note as one JSON file in a notes directory. The file name is derived from the note's
id. The directory defaults to `~/.notes/`; `NOTES_DB` sets it.

Every note file is written as ADR-0004 requires: temporary file, `os.fsync`, `os.replace`.

## Consequences

- A crash during `add` leaves either the new note file or no file for it; existing notes stay
  readable (QS-1).
- Note files are plain text. They can be diffed, read, and repaired with a text editor.
- `list` and `search` read every note file; there is no index.
- ADR-0003 names `sqlite3` and the database file. Once this ADR is accepted, its rule still
  holds with "note files" in place of the database, but its wording needs a separate update.
- Not decided here: how ids are assigned without a table's autoincrement, and how an existing
  `~/.notes.db` is migrated or read.
