# Task 2: Tags — report

**Status:** NEEDS_DECISION

## Why no code was written

docs/architecture/arc42.md section 9 points to ADR-0002 "Record architecture decisions", which
says the following are decided centrally and need an accepted ADR:
- the on-disk format (Task 2 adds a `tags` column to the `notes` table);
- CLI options and command names (Task 2 adds `--tag` to `add` and `list`).

No accepted ADR covers tags. The brief is not an ADR. Per the controller's instructions, I drafted
the decision as a proposed ADR and left the code behind it unwritten. Tests and code for the
slices (`add --tag`, `list --tag`, the `tags` column and its `ALTER TABLE` migration) depend on
that decision, so nothing else in Task 2 can proceed independently.

## ADR drafted

- Path: `docs/adr/0004-tags-as-comma-separated-column.md`
- Status: `proposed 2026-11-22`
- Title: "Store tags as a comma-separated column and add a repeatable --tag option"
- Cites: ADR-0001, ADR-0002, ADR-0003, QS-1, QG-1, QS-3, QG-3, R-3.

## Waiting for the architect

1. **ADR-0004, "Store tags as a comma-separated column and add a repeatable --tag option".**
   Question: do you approve a `tags` TEXT column (comma-separated, default empty), migrated in place
   with `ALTER TABLE`, plus `--tag` (repeatable) on `add` and `list`?
2. **Open points inside the ADR** (decide when approving or amending):
   - Tags containing a comma: reject, or escape?
   - Tag filter must match whole tags (so `work` does not match `homework`); confirm.
   - Whether `search` gets `--tag` (not in the brief; left out).
3. **Requirement not in arc42 section 1:** tagging is not among R-1 to R-5. Confirm whether to add it
   as a requirement; I have not added it, since requirements are the architect's.

## Tests and verification

- Baseline before any change: `python3 -m unittest` → `Ran 3 tests in 0.073s — OK`.
- No tests were written for Task 2 and no RED/GREEN slices exist, since the behaviour depends on the
  unaccepted decision.

## Slices

| Test | RED | GREEN | Commit |
|------|-----|-------|--------|
| (none: blocked on ADR-0004) | — | — | — |

## Files changed

- `docs/adr/0004-tags-as-comma-separated-column.md` (new, uncommitted)
- `.dispatch/task-2-report.md` (new, uncommitted)

## Concerns

- Task 1 (search order) is unaffected and independent; I did not touch it.
- The ADR is uncommitted; I did not commit it, since it is a proposal awaiting approval.
