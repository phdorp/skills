# 4. Store tags as a comma-separated column and add a repeatable --tag option

## Status

proposed 2026-11-22

## Context

Users want to group notes with tags and list one group (the planned feature "tag notes and filter
list by tag"; tagging is not among R-1 to R-5, so the architect should confirm it as a requirement).
Changing the on-disk format and adding CLI options are decisions the architect makes centrally
([ADR-0002](0002-record-architecture-decisions.md)). The store must keep opening existing databases
(QS-1, QG-1), the CLI must reach storage only through `Store` (ADR-0003, QS-3), and the
change must stay within the standard library (R-3).

## Decision

We will add a `tags` column to the `notes` table: comma-separated text, default empty. An
existing `notes` table is migrated in place with `ALTER TABLE` when the store opens. `Note` gains a
`tags` field. `add` takes `--tag` (repeatable), and `list` takes `--tag` to show only notes that
carry that tag.

## Consequences

- Existing databases keep working; no data is moved or lost (QS-1).
- Tags are stored in the database file, which stays a SQLite file (ADR-0001). Only
  `notes/store.py` touches the column (ADR-0003).
- A comma-separated column cannot hold a tag that contains a comma. The rule for rejecting or
  escaping such tags is open and needs a decision.
- Filtering by tag needs whole-tag matching, not a substring match, so `work` does not match
  `homework`. This is a constraint on the SQL in `store.py`.
- Older versions of the program still read `id, text, created` and are unaffected by the new column.
- Not decided here: whether `search` accepts `--tag`, and whether tags are listed in the output.
