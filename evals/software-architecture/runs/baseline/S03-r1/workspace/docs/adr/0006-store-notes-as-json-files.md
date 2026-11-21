# 6. Store notes as one JSON file per note

## Status

accepted 2026-11-21, supersedes [ADR-0001](0001-use-sqlite-for-storage.md)

## Context

SQLite files are binary: they are hard to diff and cannot be repaired with a text editor. Users
need to inspect and fix their notes by hand (R-2, QG-1). Crash safety must still hold (QS-1),
and the program may use only the Python standard library (R-3, QG-2). A server database
contradicts R-3, so it is not an option ([ADR-0005](0005-add-postgresql-backend.md) is rejected).

## Decision

Store each note in its own JSON file inside a store directory, by default `~/.notes/`, which
`NOTES_DIR` can override. A file is named `<id>.json` and holds the keys `id`, `text` and
`created`.

Every file is written as [ADR-0004](0004-write-notes-atomically.md) requires: a temporary file,
`os.fsync`, then the final name.

- A new note is published with `os.link` from the temporary file to `<id>.json`. `os.link`
  fails if the name already exists, so two processes can never overwrite each other's note. On
  failure the store takes the next free id and retries.
- Ids are integers: one more than the highest existing id, starting at 1.

Only `notes/store.py` reads or writes these files ([ADR-0003](0003-cli-reaches-storage-only-through-store.md)).

## Consequences

A crash leaves each note either fully written or absent, as before, and a user can open, diff
and correct any note in a text editor.

`search` and `all` read every file, so search time grows with the number of notes. This gives
up the faster search that motivated ADR-0005.

This ADR does not migrate notes from `~/.notes.db` or the `NOTES_DB` variable; a migration is a
separate change.
