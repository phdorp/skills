# Task 2 report: Tags

## What I implemented

- `notes add --tag <tag>` (repeatable) stores tags on a note. Tags are kept in a `tags` column,
  comma-separated, default empty.
- `Note` gained `tags: tuple = ()`. `Store.add(text, tags=())` and `Store.all(tag=None)` take the new arguments.
- `notes list --tag <tag>` prints only notes whose tag list contains that tag.
- A store created before this change is migrated on open: `Store.__init__` checks `PRAGMA table_info(notes)`
  and runs `ALTER TABLE notes ADD COLUMN tags TEXT NOT NULL DEFAULT ''` when the column is missing.

Design choices:
- The tag filter runs in Python on the tuple from `_note`, not in SQL with `LIKE`. An exact match means `work`
  does not match a note tagged `homework`.
- All SQL stays in `notes/store.py`, so the CLI only calls `Store` (ADR-0003).

## Slices (TDD)

| Test | RED: command and failing line | GREEN: result | Commit |
|------|-------------------------------|---------------|--------|
| `CliTest.test_add_with_tag_stores_tag` | `python3 -m unittest`: `SystemExit: 2`, argparse rejects `--tag` (ERROR, errors=1 of 4 tests) | 4/4 OK | `691e54e feat: add --tag to notes add` |
| `CliTest.test_list_with_tag_prints_only_tagged_notes` | `python3 -m unittest`: `SystemExit: 2`, argparse rejects `list --tag` (ERROR, 5 tests, errors=1) | 5/5 OK | `50254b2 feat: filter list by tag` |
| `MigrationTest.test_store_created_before_tags_still_opens` | `python3 -m unittest`: `sqlite3.OperationalError: no such column: tags` (ERROR, 6 tests, errors=1) | 6/6 OK | `e78a3f0 feat: migrate pre-tag stores to add the tags column` |

Each slice's RED was seen before its implementation was written.

## Commit history

The plan's global constraint says "one commit per task". The dispatch says "commit each green slice".
I followed the dispatch and made three commits. If you want the plan's single commit, squash the three
(`git reset --soft 87f5d7c` and recommit with `feat: tag notes and filter list by tag`).

The first attempt committed `notes/__pycache__/*.pyc` and `tests/__pycache__/*.pyc` in slice 1. I rebuilt the three
commits from their trees with the `__pycache__` paths removed, keeping the same messages and order. Verified:
`git ls-tree -r HEAD | grep pycache` returns nothing. The original SHAs were `4dd53de`, `223d036`, `32d25a8`;
they are no longer on the branch.

Commits were made with a Co-Authored-By trailer for Claude Haiku 5.5.

## Test results

Final tree, `python3 -m unittest -v`: 6/6 pass (3 existing, 3 new), output clean, no warnings.

## Files changed

- `notes/model.py`: `tags` field on `Note`.
- `notes/store.py`: `tags` column, migration, `_note` row helper, `add(text, tags=())`, `all(tag=None)`.
- `notes/cli.py`: `add --tag` (append), `list --tag`.
- `tests/test_notes.py`: three new tests, `sqlite3` import.

## Self-review findings

- Tags are stored comma-separated, so a tag containing a comma is split into two tags on read. I did not add
  validation, because the plan did not ask for it. Decide whether to reject `,` in `--tag` values.
- `search` line in `store.py` is about 105 characters and has no wrap. Task 1 edits the same `search` query
  (`ORDER BY id` to newest first). Expect a merge conflict on that line if both branches are merged.
- `notes/__pycache__/` and `tests/__pycache__/` are untracked in the working tree. The repo has no `.gitignore`.
  I did not add one, since it was out of scope.
- The migration runs on every `Store` open. The `PRAGMA` check is cheap, and an existing column makes it a no-op.

## Concerns

- The one-commit-per-task rule conflicts with the slice-commit rule (see Commit history). Three commits are on the branch.
