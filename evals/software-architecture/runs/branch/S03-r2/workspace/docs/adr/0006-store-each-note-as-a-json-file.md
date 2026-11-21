# 6. Store each note as one JSON file

## Status

proposed

## Context

This ADR replaces ADR-0001 (SQLite). Notes must survive crashes (R-2, QG-1, QS-1), and the
program may use only the Python standard library (R-3, QG-2). SQLite files are binary and hard
to diff or repair by hand; a text file per note can be read, diffed and fixed in an editor.
Each file is written as ADR-0004 requires, so a crash leaves a note either fully stored or absent.

## Decision

We will store each note as its own UTF-8 JSON file (`id`, `text`, `created`) in a notes
directory, by default `~/.notes/`, overridable with `NOTES_DIR`. Every file is written
atomically as ADR-0004 requires. `notes/store.py` remains the only module that reads or writes
these files.

## Consequences

Notes are easy to diff, back up and repair with a text editor. Each `add` is one atomic file
write, so no transaction layer is needed. `search` and `list` read every file, which is slower
than an indexed query on large collections (R-1). The existing `~/.notes.db` has no migration
path yet. Once accepted, ADR-0001 becomes `superseded by ADR-0006`. ADR-0003 still holds, but
its statement that only `store.py` imports `sqlite3` becomes stale; it needs a new ADR or a
note when this one is accepted.
