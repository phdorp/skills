# Task 2 report: Tags

**Status:** NEEDS_DECISION

## What happened

Before writing code, I checked the brief against `docs/architecture/arc42.md`. ADR-0002
("Record architecture decisions") lists these as decided centrally:

- the storage engine and the on-disk format;
- CLI command names and exit codes.

Task 2 changes both:

- **On-disk format.** It adds a `tags` column to the `notes` table and migrates existing stores
  with `ALTER TABLE`. ADR-0001 fixes SQLite but not the table layout, so no accepted ADR settles it.
- **CLI interface.** It adds `--tag` to `add` (repeatable) and to `list`. The brief names a CLI
  option as something to check. The `list --tag` rule for repeated values is not settled either.

Per the protocol I drafted two proposed ADRs and committed each alone. I wrote no code for the
feature and no tests, because every test in the brief exercises these two decisions.

## Commits

| Commit | Subject |
|---|---|
| `9fc2b7f` | docs(adr): propose store tags as a comma-separated column |
| `f0ed061` | docs(adr): propose tag CLI options --tag on add and list |

## ADRs waiting for the architect

1. **ADR-0004 Store note tags as a comma-separated column** (`docs/adr/0004-store-tags-as-comma-separated-column.md`).
   Question: do you approve a comma-separated `tags` text column, default empty, migrated in place
   with `ALTER TABLE` in one transaction, and do you accept that tags cannot contain commas?
   Still open inside it: whether `add --tag` rejects commas, or tags are normalised another way,
   and whether tags are case-sensitive (`work` vs `Work`).
2. **ADR-0005 Tag the CLI with `--tag` on add and list** (`docs/adr/0005-tag-cli-options.md`).
   Question: do you approve a repeatable `--tag` on `add`, and a `--tag` on `list` that shows notes
   carrying any of the given tags? Still open inside it: the rule for repeated `--tag` values on `list`
   (ADR-0005 proposes "any of").

Both ADRs stay `proposed`. ADR-0004 must be accepted before ADR-0005 is built on it.

## Tests and verification

- `python3 -m unittest`: 3 tests, OK (run on the branch after the two ADR commits; no code changed).
- No feature slices were started, so there is no RED/GREEN table.

## Files changed

- `docs/adr/0004-store-tags-as-comma-separated-column.md` (new)
- `docs/adr/0005-tag-cli-options.md` (new)

## Not done

- `notes/store.py`, `notes/cli.py`, `notes/model.py`, `tests/test_notes.py` are unchanged.
- The "store created before this change still opens" test is held back with the rest, since
  its migration shape comes from ADR-0004.

## Resume steps once both ADRs are accepted

1. Write the failing test for `add --tag` and watch it fail.
2. Add the `tags` column with the `ALTER TABLE` migration, `Note.tags`, and `add --tag`. Commit `feat: tag notes`.
3. Write the failing `list --tag` test, implement it, and commit `feat: filter list by tag`.
   (The brief's single commit, `feat: tag notes and filter list by tag`, can be used if the controller prefers one commit.)
