# 6. Store one JSON file per note

## Status

proposed

## Context

This replaces ADR-0001 (SQLite). SQLite files are binary: they are hard to diff and cannot be
repaired by hand. Notes must survive crashes (R-2, QG-1, QS-1), and the program may use only
the Python standard library (R-3, QG-2). ADR-0004 requires every file the store writes to be
written to a temporary file, flushed, and moved into place with `os.replace`. Only the store
touches the storage (ADR-0003, QG-3, QS-3).

## Decision

We will store each note as one JSON file in one notes directory, one file per note. Each file
is written atomically as ADR-0004 requires.

## Consequences

Notes can be read, diffed, and repaired with a text editor. A crash leaves each note either
fully written or absent (QS-1), through the rule in ADR-0004. Each `add` writes one new file.
Listing and searching read every file, which may be slower than SQLite for large collections
(R-1). Because the store is the only block that knows the storage (ADR-0003), changing the
format stays inside `notes/store.py`. ADR-0001 stays `accepted` until this ADR is accepted;
then it becomes `superseded by ADR-0006`. The default location of the directory, and any change
to the README and arc42 that the new format needs, are left to the work that follows this ADR.
