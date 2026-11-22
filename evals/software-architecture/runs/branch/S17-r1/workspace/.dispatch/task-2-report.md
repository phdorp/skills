# Task 2: Tags — report

**Status:** NEEDS_DECISION

## What I did

Checked the task against `docs/architecture/arc42.md` and the ADR "Record architecture decisions"
(ADR-0002). Its "decided centrally" list names the on-disk format and CLI interface. Task 2 changes
both: it adds a `tags` column to the `notes` table and adds `--tag` options to `add` and `list`.
No accepted ADR settles either. Per the brief rules, I did not write the tag code or its tests.

Drafted the decision as a **proposed** ADR:

- `docs/adr/0004-tags-storage-and-cli-option.md` (Status: `proposed`)
  Question for the architect to approve: *Store tags as a comma-separated `tags` column (migrated
  with `ALTER TABLE`), and add repeatable `--tag` to `add` and `list`?*

Also added one glossary term (`GLOSSARY.md`): **Tag**.

## Tests

Baseline before any change: `python3 -m unittest` → `Ran 3 tests … OK`.
No tag tests written (they depend on the unapproved format and option). No code changed.

## Slices

| Test | RED: command and failing line | GREEN: result | Commit |
|------|-------------------------------|---------------|--------|
| — | not started: blocked on ADR-0004 | — | — |

## Files changed (uncommitted)

- `docs/adr/0004-tags-storage-and-cli-option.md` (new, proposed)
- `GLOSSARY.md` (added Tag)

No commits created.

## Waiting for the architect

- **ADR-0004 — Store tags as a comma-separated column and add `--tag` options.**
  Question: approve the comma-separated `tags` column with `ALTER TABLE` migration, and the
  repeatable `--tag` on `add` and `list`? Or prefer a join table (see Consequences)?
  Once accepted, Task 2 can proceed exactly as the brief specifies.

## Concerns

- Comma-separated tags cannot contain commas; the ADR leaves reject-vs-escape open.
- Task 1 (search order) is independent and untouched.
