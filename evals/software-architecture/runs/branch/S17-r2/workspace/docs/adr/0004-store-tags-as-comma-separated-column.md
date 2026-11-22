# 4. Store note tags as a comma-separated column

## Status

proposed

## Context

Users want to group notes by tag (R-1: users add and list notes from the command line). Notes
must survive the change: an existing store must still open and keep every note (R-2, QG-1,
QS-1). Storage is decided centrally, and the on-disk format is one of those decisions. ADR-0001
fixes SQLite as the engine but not the table layout. ADR-0003 keeps all database access in
`notes/store.py` (QG-3, QS-3).

## Decision

We will add a `tags` column to the `notes` table: text, comma-separated, empty by default. A
store created before this change is migrated in place with `ALTER TABLE`, in one transaction, so
no note is lost and no note is unreadable if the process is killed during the migration.

## Consequences

- Tags need no second table and no join; filtering by tag is a single-table query.
- A tag cannot contain a comma. Whether `add --tag` must reject a comma, or whether tags are
  normalised some other way, is open and needs a decision before the CLI option is built.
- Tags are not normalised: `work` and `Work` are different tags unless the architect decides
  otherwise.
- Only `notes/store.py` changes its SQL for this (ADR-0003).
- The CLI option that sets and filters tags is decided separately: see ADR-0005.
