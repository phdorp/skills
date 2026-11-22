# Task 2: Tags — report

Plan: docs/plans/2026-11-22-search-and-tags.md (Task 2)
Branch: master

## What I implemented

- `notes add --tag <tag>` (repeatable) stores the tags with the note.
- `notes list --tag <tag>` prints only notes whose tags include `<tag>` (exact membership, not substring).
- `notes` table gains `tags TEXT NOT NULL DEFAULT ''` (comma-separated). Stores created before this change are migrated on open with `ALTER TABLE notes ADD COLUMN tags ...`.
- `Note` gains `tags: tuple = ()`. The store parses the comma-separated column into a tuple, so `Note.tags` is `("work",)` or `()`.
- `Store.add(text, tags=())` and `Store.all(tag=None)` take the new parameters. `search` returns notes with tags but does not filter on them.

Interpretation choices (the brief did not specify them):
- `Note.tags` is a tuple of strings, not the raw comma-separated string.
- `list --tag` matches whole tags only. A note tagged `homework` does not match `--tag work`. The filter runs in Python, not SQL `LIKE`, because `LIKE` treats `_` and `%` as wildcards.
- `search` output format is unchanged; tags are not printed.

## Slices (TDD)

| Test | RED: command and failing line | GREEN: result | Commit |
|------|-------------------------------|---------------|--------|
| `CliTest.test_add_stores_tag` | `python3 -m unittest tests.test_notes.CliTest.test_add_stores_tag` → `notes: error: unrecognized arguments` / ERROR (argparse exits 2 on `--tag`) | 4/4 full suite OK | `9a0a276 feat: store tags given to notes add --tag` |
| `CliTest.test_list_filters_by_tag` | `python3 -m unittest tests.test_notes.CliTest.test_list_filters_by_tag` → `notes: error: unrecognized arguments: --tag work` / ERROR | 5/5 full suite OK | `ac0e3eb feat: filter notes list by tag` |
| `StoreTest.test_store_created_before_tags_still_opens` | `python3 -m unittest tests.test_notes.StoreTest.test_store_created_before_tags_still_opens` → `sqlite3.OperationalError: no such column: tags` / ERROR | 6/6 full suite OK | `b6176d9 feat: add tags column to stores created before tags` |

Slice 1 and 2 test RED runs were observed on the pre-rebuild commits (see "Commit history" below); the test code and implementation in the final commits are identical to what was run.

## Testing

- `python3 -m unittest` → `Ran 6 tests in 0.189s — OK` (run on the final tree, output pristine).
- Manual run against a scratch DB (`NOTES_DB`): `add --tag work`, `add --tag homework --tag urgent`, `add`; `list --tag work` printed only "Call Ann"; `list` printed all three; `search milk` printed "Buy milk".

## Files changed

- `notes/model.py` — `Note.tags`
- `notes/store.py` — tags column, migration, `add(tags=)`, `all(tag=)`, `_note` row helper
- `notes/cli.py` — `add --tag` (append), `list --tag`
- `tests/test_notes.py` — three tests above, plus `import sqlite3`

## Commit history

- Commits 79cc8c8 and 59154b2 were first made with `git add notes/ tests/`, which also committed tracked-looking `notes/__pycache__/*.pyc` and `tests/__pycache__/*.pyc`. I reset the branch to `d7bf255` (only my own unpushed commits) and recommitted the three slices with only `.py` files. The final three commits are the ones listed above.
- The brief's global constraint says "one commit per task", while the dispatch says "commit each green slice". I followed the slice rule. If you want one commit for Task 2, the three commits can be squashed into `feat: tag notes and filter list by tag`.

## Self-review findings

- **Commas in tags.** `add --tag "a,b"` stores `a,b` and reads back as two tags `("a", "b")`, so `list --tag "a,b"` matches nothing. Nothing in the spec covers this, and I did not add validation. Rejecting commas in `add` would be a small follow-up.
- **Untracked pycache.** `notes/__pycache__/` and `tests/__pycache__/` now show as untracked because the `.pyc` files are no longer committed. There is no `.gitignore`; I did not add one because it is outside this task.
- `notes/store.py` `search` SQL line is already over 100 characters from the original code; I left it as it was.

## Concerns

- None blocking. The comma-in-tag edge case is the main open question for the controller.
