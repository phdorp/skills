# 6. Store each note as one JSON file

## Status

proposed

## Context

Notes must survive crashes (R-2, QG-1, QS-1), and the program may use only the Python standard
library (R-3, QG-2). ADR-0001 stores all notes in one SQLite file. The architect has decided to
move off SQLite because SQLite files are hard to diff and repair by hand. This ADR replaces
ADR-0001 if it is accepted; until then ADR-0001 stays in force.

## Decision

Store each note as its own JSON file, in one directory, by default `~/.notes/`, named by the note's
id. The `Store` class in `notes/store.py` reads and writes these files with the standard `json`
module. Every write follows ADR-0004 (temporary file, `os.fsync`, `os.replace`). No database
engine is used.

## Consequences

- A crash during `add` leaves either the new note file or none; the store keeps opening (QS-1).
  Atomic replacement of one file replaces the SQLite transaction as the crash-safety mechanism.
- Readers ignore leftover temporary files from an interrupted write.
- Notes are plain text and can be diffed, read, and repaired with a text editor.
- `list` and `search` read every note file. Search speed on large note counts is not measured.
- ADR-0003 names `sqlite3` and the database file in its Decision. If this ADR is accepted, ADR-0003
  still holds in its intent (only `store.py` touches storage) but its wording needs updating.
  That update is not made here.
- ADR-0004 applies to every note file without change.
- The README and the default path `~/.notes.db` in ADR-0001 are out of date once this is
  implemented; they are not changed by this ADR.
