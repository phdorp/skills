# 4. Store note tags as comma-separated text and filter list with --tag

## Status

proposed

## Context

Users want to group notes under tags and list one group (R-1). Tags change the on-disk format
of the `notes` table, which ADR-0002 decides centrally, and add a CLI option, which ADR-0002
also decides centrally. Existing stores must keep opening with their notes intact (R-2,
QS-1), so the table is migrated in place rather than recreated. The program uses only the
standard library (R-3), so tags are kept in SQLite itself, not in a second file or table.
No ADR settles either choice yet.

## Decision

We will add a `tags` column to the `notes` table: comma-separated text, empty by default.
Existing tables are migrated with `ALTER TABLE notes ADD COLUMN tags TEXT NOT NULL DEFAULT ''`
when `Store` opens them. `notes add` takes `--tag` (repeatable) and `notes list` takes `--tag`
(repeatable), printing only notes that carry the given tag. `Note` gains a `tags` field.

## Consequences

- Stores written before this change keep opening and keep their notes; the migration runs
  once and needs no separate tool.
- A tag cannot contain a comma: `--tag` values with a comma must be rejected or escaped. The
  format decision is what sets this limit, so the architect should confirm it or ask for a
  separate tag table, which would replace this ADR.
- Filtering by tag matches whole tags, not substrings, so `work` does not match `homework`.
- Anyone reading the database by hand sees tags as one text field; this is consistent with
  ADR-0001, which already rules out text-editor access.
- The storage details stay inside `notes/store.py` (ADR-0003); `cli` only passes `--tag`
  values to `Store`.
- No effect on ADR-0001, ADR-0003 or the dependency rule in ADR-0002.
