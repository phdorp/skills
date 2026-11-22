# 4. Store tags as a comma-separated text column

## Status

proposed

## Context

Users filter notes by tag from the command line (R-1). Tags change the on-disk format of the
`notes` table, which ADR-0002 decides centrally, and the storage engine stays SQLite (ADR-0001).
Only `notes/store.py` touches the database (ADR-0003, QS-3), and a contributor must still be able
to modify the program without learning all of it (QG-3). Existing stores must keep opening
(QS-1 requires that the store still opens).

## Decision

We will add a `tags` column to the `notes` table: comma-separated `TEXT`, default empty. An
existing table is migrated with `ALTER TABLE` when a store is opened. `notes add` takes a
repeatable `--tag` option and `notes list` takes `--tag` to filter notes by tag.

## Consequences

Stores written before this change open and migrate in place; the file format changes for every
store. The encoding is simple but means a tag cannot contain a comma. Filtering by tag is a
text match in `store.py`, so the CLI and `Note` stay unaware of the encoding. Task 2 of
`docs/plans/2026-11-22-search-and-tags.md` waits for this ADR to be accepted. ADR-0002 and
ADR-0003 are unchanged.
