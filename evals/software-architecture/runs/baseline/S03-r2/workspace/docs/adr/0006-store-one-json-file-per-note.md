# 6. Store one JSON file per note

## Status

accepted 2026-11-21

Supersedes [ADR-0001](0001-use-sqlite-for-storage.md).

## Context

Notes must survive crashes (R-2, QG-1, QS-1), the program may use only the Python standard
library (R-3, QG-2), and the store must stay a single module (QS-3). Users must be able to
inspect, diff and repair their notes by hand. A SQLite file is binary: it is hard to diff and
cannot be repaired with a text editor, so it no longer meets these needs.

## Decision

Store each note as one JSON file, named `<id>.json`, in one notes directory, by default
`~/.notes/`. The directory is set with `NOTES_DIR`.

Each file is written under the rule of [ADR-0004](0004-write-notes-atomically.md): temporary
file in the same directory, `os.fsync`, then `os.replace`.

Only `notes/store.py` reads or writes these files ([ADR-0003](0003-cli-reaches-storage-only-through-store.md)).

## Consequences

- A crash leaves each note either fully written or absent; one damaged note does not affect the others.
- Notes are plain text and can be read, diffed and repaired with a text editor.
- Search has no index: `search` reads every note file. Acceptable for the note volumes in scope;
  revisit if search becomes slow (see the rejected [ADR-0005](0005-add-postgresql-backend.md)).
- Many small files: one extra `fsync` and one directory entry per note.
- Existing data in `~/.notes.db` is not migrated by this decision; a migration is a separate piece of work.
