# 4. Tag notes in a comma-separated column

## Status

proposed

## Context

Users want to group notes and list one group (R-1: users add, list and search notes from the
command line). The change touches two decisions that ADR-0002 reserves for the architect: the
on-disk format (the `notes` table gains a column) and the CLI surface (`add` and `list` gain
options). Existing stores must keep opening without manual steps (QG-3: maintainability, and
the store stays the only block that knows the storage, ADR-0003). The program stays on the
standard library (R-3), so tags are held in the same SQLite file as ADR-0001 requires.

## Decision

We will add a `tags` column to the `notes` table: comma-separated text, default empty. An
existing table is migrated with `ALTER TABLE ... ADD COLUMN tags`. `Note` gains a `tags` field.

We will add `--tag` to `notes add`, repeatable, one tag per flag. We will add `--tag` to
`notes list`, which shows only notes carrying that tag. Command names and exit codes do not
change.

## Consequences

- A tag cannot contain a comma. `add --tag` rejects such a tag with the usual
  `notes: <message>` error and exit code 1 (arc42 section 8).
- Filtering matches whole tags, not substrings, so `work` does not match `homework`.
- Tags are stored as text inside the note row, so a separate `tags` table, which would allow
  listing all tags and renaming one, is not provided. Adding it later needs a new ADR that
  replaces this one.
- Stores created before this change are changed in place by the migration. Downgrading the
  program does not remove the column, and older builds ignore it.
- No other ADR is affected. The work that follows: the plan's Task 2 in
  `docs/plans/2026-11-22-search-and-tags.md` waits for this ADR to be accepted.
