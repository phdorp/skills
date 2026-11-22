# Task 2 report: Tags

**Status:** NEEDS_DECISION

## Why this is blocked

The brief changes two things that `docs/adr/0002-record-architecture-decisions.md` lists as
decided centrally:

- the on-disk format: a new `tags` column on the `notes` table;
- CLI options: `add --tag` and `list --tag`.

No accepted ADR settles either. The brief is not an accepted ADR, so the architect has to
decide. I did not write the code, the tests, or the migration.

## What I did

- Drafted a proposed ADR: `docs/adr/0004-tag-notes-in-a-comma-separated-column.md`
  (status `proposed`). It records the comma-separated column with `ALTER TABLE` migration,
  and repeatable `--tag` on `add` and `list`.
- Committed it alone: `c8088e8 docs(adr): propose tag notes in a comma-separated column`.

## Question for the architect

Approve ADR-0004 as written, or change it? Points that need a decision:

1. Comma-separated text in the `notes` row (the brief's choice), or a separate `tags` table?
   The ADR picks the column and rejects the table for now. A table would allow listing and
   renaming tags.
2. Tags may not contain commas. `add` rejects such a tag with exit code 1.
3. `list --tag` matches whole tags only.

## Tests

- Baseline `python3 -m unittest`: 3 tests, OK (no code changed).
- No TDD slices were written. No failing test was produced, because the behaviour depends on
  the unaccepted decision.

## Slices

| Test | RED | GREEN | Commit |
|------|-----|-------|--------|
| (none: blocked on ADR-0004) | - | - | - |

## Files changed

- `docs/adr/0004-tag-notes-in-a-comma-separated-column.md` (new, in commit c8088e8)
- `.dispatch/task-2-report.md` (this file, not committed)

## Concerns

- Task 1 (`docs/plans/...` search order) is independent and was not touched here.
- Once ADR-0004 is accepted, Task 2 can proceed with the brief's steps as written.
