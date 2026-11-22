# 4. Store tags as a comma-separated column and add `--tag` options

## Status

proposed

## Context

Users need to group notes so that `list` can show one group (R-1, QG-3). Tags change the on-disk
format of the `notes` table, which is decided centrally (ADR-0002) and rests on the SQLite file
of ADR-0001. Existing stores must keep opening without loss, as crash safety requires (R-2, QS-1).
The `--tag` option adds to the CLI surface, which ADR-0002 also keeps central. Only `notes/store.py`
touches the database (ADR-0003).

## Decision

We will add a `tags` column to the `notes` table: comma-separated text, default empty. An existing
table is migrated with `ALTER TABLE notes ADD COLUMN tags`. `add` takes `--tag` (repeatable) and
`list` takes `--tag` to show only notes carrying that tag.

## Consequences

- Stores created before this change still open and read as untagged.
- Tags are plain text, so a tag cannot contain a comma; the CLI or store must reject or escape one.
  Filtering by tag matches whole tags, not substrings of the column.
- A comma-separated column makes per-tag queries and a tag list harder than a join table would.
  A join table is the alternative if tags grow beyond simple filtering.
- Only `notes/store.py` changes for the storage part (QS-3); `cli.py` gains the two options.
- ADR-0001 and ADR-0003 are unchanged.
