# Task 2 report: Tags

**Status:** NEEDS_DECISION

## Why no code was written

`docs/architecture/arc42.md` exists, so I checked the task against it before writing code.
ADR-0002 ("Record architecture decisions") lists these as decided centrally:

- the storage engine and the on-disk format;
- CLI command names and exit codes;
- (and, under the general test, any CLI option or interface).

Task 2 makes two such choices, and no accepted ADR settles either:

1. **On-disk format:** a new `tags` column (comma-separated text) on the `notes` table,
   migrated with `ALTER TABLE`.
2. **CLI option:** `--tag` (repeatable) on `notes add`, and `--tag` on `notes list`.

The brief spelling these out is not an accepted ADR. Per ADR-0002, work that depends on an
undecided item waits for its ADR. Every Task 2 test and code change depends on these two choices,
so I did not write the failing tests or the implementation. Nothing else in Task 2 is separable.

## What I did

- Drafted a proposed ADR covering both choices:
  `docs/adr/0004-tag-notes-in-a-comma-separated-column.md` (Status: `proposed`).
- Committed it alone: `15ebdf3 docs(adr): propose tag notes in a comma-separated column`.
- Ran the baseline suite: `python3 -m unittest` → `Ran 3 tests ... OK`.

## Slices

| Test | RED: command and failing line | GREEN: result | Commit |
|------|-------------------------------|---------------|--------|
| (none; blocked on ADR) | not run | not run | — |

## Files changed

- `docs/adr/0004-tag-notes-in-a-comma-separated-column.md` (new)
- `.dispatch/task-2-report.md` (new, untracked by commit)

## For the architect: ADRs waiting for approval

- **ADR-0004, Tag notes in a comma-separated column.** Question: do you accept a comma-separated
  `tags` column with an `ALTER TABLE` migration, and `--tag` options on `add` and `list`?
  Open point to settle with it: tags cannot contain commas (the ADR says `add` must reject or
  escape them). Approving it, or rejecting it with a reason, unblocks Task 2.

## Concerns

- The ADR's QS-1 citation is a judgement: I cited it for "existing stores must still open after
  a crash". Please confirm that is the intended quality scenario.
- Task 1 (search order) is independent and was not touched here.
