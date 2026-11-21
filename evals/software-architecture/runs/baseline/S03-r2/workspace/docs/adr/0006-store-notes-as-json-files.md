# 6. Store notes as one JSON file per note

## Status

accepted 2026-11-21

Supersedes [ADR-0001](0001-use-sqlite-for-storage.md).

## Context

SQLite stores all notes in one binary file. That file is hard to diff and cannot be repaired by
hand with a text editor. Crash safety (R-2, QG-1, QS-1) and the standard-library-only rule
(R-3, QG-2) still apply. [ADR-0004](0004-write-notes-atomically.md) gives a safe write for any
single file, so one file per note keeps crash safety without a database.

## Decision

Store each note as its own file in the notes directory, `~/.notes/` by default, overridable
with `NOTES_DIR` (this replaces `NOTES_DB`).

- File name: `<id>.json`, where `<id>` is the note id.
- File content: a JSON object with the fields `id` (integer), `text` (string) and `created`
  (UTC timestamp, ISO 8601, seconds precision).
- Every note file is written as ADR-0004 requires.

Only `notes/store.py` reads or writes these files (ADR-0003).

## Consequences

- A note can be read, diffed and repaired with a text editor.
- Crash safety comes from ADR-0004: a crash leaves each note either fully stored or absent.
- Listing and searching read every note file. This is slower than a database index for very
  large collections. It is accepted for now; see the open search-speed request (R-1) in
  [ADR-0005](0005-add-postgresql-backend.md).
- `NOTES_DB` and `~/.notes.db` no longer apply. Existing SQLite data is not migrated by this
  decision; any migration is a separate decision.
