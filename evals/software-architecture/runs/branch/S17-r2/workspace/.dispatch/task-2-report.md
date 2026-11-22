# Task 2 report: Tags

**Status:** NEEDS_DECISION

## What happened

The brief asks for a `tags` column (comma-separated text) in the `notes` table, an
`ALTER TABLE` migration of existing stores, a `--tag` option on `add` and `list`, and a
`tags` field on `Note`. Per docs/architecture/arc42.md section 9 and ADR-0002, the on-disk
format and CLI options are decided centrally, and no accepted ADR settles them. The brief is
not an accepted ADR, so I did not write the tag code or its tests.

## Done

- Drafted `docs/adr/0004-tags-as-comma-separated-text.md` with status `proposed`, covering
  the tag storage format, the migration, and the `--tag` option on `add` and `list`.
- Committed alone: `a66917b docs(adr): propose storing tags as comma-separated text and --tag filter`.

## Not done (waiting on ADR-0004)

- Step 1 tests (`notes add --tag`, `notes list --tag`, old store still opens).
- Step 2 implementation in `notes/store.py`, `notes/cli.py`, `notes/model.py`.
- Commit `feat: tag notes and filter list by tag`.

## Test run

`python3 -m unittest`: Ran 3 tests, OK (unchanged code).

## Open decision for the architect

- **ADR-0004, "Store note tags as comma-separated text and filter list with --tag"**: approve
  as written? Main question: is a comma-separated text column acceptable, given that a tag
  cannot contain a comma, or should tags get a separate table (which would replace ADR-0004)?
