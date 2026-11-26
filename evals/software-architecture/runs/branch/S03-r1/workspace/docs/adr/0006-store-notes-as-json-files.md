# 6. Store one JSON file per note

## Status

proposed

## Context

This ADR replaces ADR-0001 (use SQLite for storage). SQLite files are binary: they are hard to
diff and cannot be repaired by hand. Notes must still survive crashes (R-2, QG-1, QS-1), and the
program may use only the Python standard library (R-3, QG-2). The store must stay the only module
that touches storage (QG-3, QS-3, ADR-0003).

## Decision

Store each note as its own JSON file, written with the standard `json` module. Every note file is
written by the atomic rule in ADR-0004 (temporary file, `os.fsync`, `os.replace`). The directory
holding the note files replaces the database file.

## Consequences

- Crash safety rests on ADR-0004 per file. SQLite transactions are gone, so an operation that
  must change several notes at once has no built-in all-or-nothing guarantee.
- Note files are text and can be diffed, read, and repaired with an editor.
- Listing and searching read every note file. This is slower with many notes; it is the problem
  the rejected ADR-0005 aimed at, and it is accepted here without a second engine.
- ADR-0003 still holds: only `notes/store.py` touches the note files. Its wording names `sqlite3`
  and "the database file"; that wording becomes stale when this ADR is accepted and is not edited
  here.
- ADR-0004 says "any file the store writes besides the database"; once this ADR is accepted, every
  note file falls under ADR-0004's rule.
- Still open for the architect: the default directory for the note files (today `~/.notes.db`,
  overridable with `NOTES_DB`), and how the environment variable is renamed.
