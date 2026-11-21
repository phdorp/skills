# 6. Store one JSON file per note

## Status

proposed

## Context

This ADR replaces ADR-0001 (SQLite for storage). SQLite files are binary and hard to diff and
repair by hand, so users cannot inspect or fix their notes with a text editor. Notes must still
survive crashes (R-2, QG-1, QS-1), and the program may use only the Python standard library
(R-3, QG-2). ADR-0005 (a second engine) is rejected, so this is the only storage engine.

## Decision

We will store each note as one JSON file in a single notes directory. Every write follows
ADR-0004 (temporary file, `os.fsync`, `os.replace`). Only `notes/store.py` reads or writes these
files (ADR-0003).

## Consequences

Notes can be read, diffed and repaired with a text editor. Crash safety comes from the atomic
write rule of ADR-0004, not from a database transaction, so each command that changes notes
writes one file and listing or searching reads many. The directory location, the note id scheme
and the migration of an existing `~/.notes.db` are not decided here and need their own decision
before this ADR is accepted. ADR-0001 stays `accepted` until this ADR is accepted. ADR-0003
mentions `sqlite3`; that reference becomes stale when this ADR is accepted, while its rule that
only the store touches storage still holds.
