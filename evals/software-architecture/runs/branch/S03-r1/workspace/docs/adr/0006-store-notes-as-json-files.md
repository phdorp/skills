# 6. Store notes as one JSON file per note

## Status

proposed

## Context

SQLite files are hard to diff and repair by hand; the architect wants notes stored as plain text that can be read and fixed in an editor. This ADR replaces [ADR-0001 Use SQLite for storage](0001-use-sqlite-for-storage.md). ADR-0001 stays accepted until this ADR is accepted.

Notes must survive crashes (R-2, QG-1, QS-1), the program may use only the Python standard library (R-3, QG-2), and the store must stay the only module that knows the storage (QG-3, QS-3). A server database is out, per the rejection of [ADR-0005](0005-add-postgresql-backend.md).

## Decision

We will store each note as one JSON file. Notes are kept in the directory `~/.notes/` (set `NOTES_DIR` to use another directory). Each note is one file named `<id>.json` holding the note's id, text, and creation time. Every write follows [ADR-0004](0004-write-notes-atomically.md). Only `notes/store.py` reads or writes these files ([ADR-0003](0003-cli-reaches-storage-only-through-store.md)).

## Consequences

Notes can be diffed, read, and repaired in a text editor. A damaged note affects only its own file.

Search has no index and must read every file, which is slower with many notes; this weighs against R-1 for users with large collections. Ids must be unique across files; the id scheme is not decided here and needs its own decision.

`NOTES_DB` and `~/.notes.db` are replaced by `NOTES_DIR` and `~/.notes/`. Existing databases are not migrated by this ADR.

[ADR-0004](0004-write-notes-atomically.md) says "besides the database". That wording is outdated: each note file is now a written file that the rule covers.

Once accepted, this ADR makes [ADR-0001](0001-use-sqlite-for-storage.md) `superseded`. The code (`notes/store.py`, its tests), the README, and arc42 section 2 and 5 still describe SQLite and must follow after acceptance.
