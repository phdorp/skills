# 6. Store one JSON file per note

## Status

proposed

## Context

ADR-0001 stores all notes in one SQLite file. SQLite files are binary, so they are hard to diff
and cannot be repaired with a text editor. Notes must survive crashes
(R-2, QG-1, QS-1), and the program may use only the Python standard library (R-3, QG-2).
This ADR replaces [ADR-0001 Use SQLite for storage](0001-use-sqlite-for-storage.md).

## Decision

We will store each note as its own JSON file in a notes directory, by default `~/.notes/`,
named by the note id (for example `3.json`). Every file is written as ADR-0004 requires.

## Consequences

Notes can be read, diffed and repaired with a text editor. Crash safety comes from the
atomic write of ADR-0004 instead of SQLite transactions, so each `add` writes one file.
`list` and `search` read every file, which is slower for large collections.
The store must still allocate note ids, and it must migrate or ignore an existing
`~/.notes.db`; both are open for the implementation.
`notes/store.py` and its tests change; `notes/cli.py` does not (ADR-0003).
ADR-0005 is rejected, so it is not affected.
