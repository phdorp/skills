# 4. Store note tags as a comma-separated column in the notes table

## Status

proposed

## Context

Users want to tag notes and filter `list` by tag (plan `docs/plans/2026-11-22-search-and-tags.md`,
Task 2). No requirement in arc42 section 1 covers tags yet: this ADR names the need in words, and
the architect should confirm or add a requirement (suggest running `add-requirements`).

The change alters the on-disk format of the SQLite file that ADR-0001 chose, and ADR-0002 reserves
"the storage engine and the on-disk format" for central decision. Existing stores must still open
(a migration with `ALTER TABLE`), and the change must keep crash safety (R-2, QG-1, QS-1), so the
migration runs in a transaction. Storage details stay inside `notes/store.py` (QG-3, QS-3, ADR-0003); `notes/cli.py` gains only the
`--tag` flags and `notes/model.py` gains the `tags` field.

Options the plan implies:

- **A. Comma-separated `tags` column on `notes`** (the plan's choice). One column, one migration,
  no new table. Cannot hold a tag that contains a comma; filtering by tag needs string matching.
- **B. Separate `tags` table** with `(note_id, tag)` rows. Exact tag matching and indexing, at the
  cost of a second table and a join in `Store`.

## Decision

Proposed: We will use option A, a `tags` column (comma-separated text, default empty) on the
`notes` table, added to existing stores by an `ALTER TABLE` migration inside a transaction.
Option B is the alternative if the architect rules that tags may contain commas or need indexed lookup.

## Consequences

If A is accepted, Task 2 proceeds as planned, and tags containing commas are rejected at `add`.
If B is chosen, Task 2's plan changes (new table, join in `Store.all`/`search`), and this ADR is
superseded by a new one. Task 1 (newest-first search) is unaffected either way. The `Note` value
gains a `tags` field; the CLI and `Store` are the only callers.
