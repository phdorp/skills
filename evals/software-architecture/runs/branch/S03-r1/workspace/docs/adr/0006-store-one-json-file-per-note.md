# 6. Store each note as one JSON file

## Status

proposed

## Context

This replaces ADR-0001 (use SQLite for storage). SQLite files are binary and hard to diff and
repair by hand, so the architect wants notes stored in a plain-text form a user can read and fix.

Notes must still survive crashes (R-2, QG-1, QS-1), and the program may use only the Python
standard library (R-3, QG-2). The standard library ships `json`, and ADR-0004 already gives an
atomic write (temporary file, `os.fsync`, `os.replace`) that works per file.

## Decision

We will store each note as its own JSON file in one store directory, named by the note's id.
Every write goes through the atomic write rule of ADR-0004. The store directory replaces the
SQLite database file; its default location is not yet decided (see Consequences).

## Consequences

A crash during a write leaves either the old note file or the new one, as ADR-0004 requires.
Notes can be read, diffed and repaired with a text editor.

Harder:

- QS-1 says the store still opens after a crash. A single unreadable note file must not stop
  the store from opening; the store has to skip and report such a file. This needs its own test.
- There are no multi-note transactions. Operations that change several notes at once can leave
  the store half-changed; none exist today.
- `list` and `search` (R-1) read every file, which is slower than a SQL query on a large store.
- The default location (`~/.notes.db` in ADR-0001) changes to a directory. The architect must
  decide the new default path; it is not decided here.

Effects on other ADRs: ADR-0001 stays `accepted` until this ADR is accepted, then becomes
`superseded by ADR-0006`. ADR-0003 is unchanged in substance: only `notes/store.py` may touch the
storage, but after this change that module uses `json` and file operations instead of `sqlite3`.
ADR-0004 is unchanged; its atomic write rule now applies to each note file. ADR-0002's central
list already names the storage engine and on-disk format, so it needs no change.
Code in `notes/store.py` still imports `sqlite3`; it is not changed by this ADR.
