# Task 2 report: Tags

## What I implemented
- `notes add --tag <tag>` (repeatable) stores tags on the note.
- `notes list --tag <tag>` prints only notes whose tags contain that exact tag (`homework` does not match `work`).
- `Note` gains `tags: tuple = ()`.
- `notes` table gains `tags TEXT NOT NULL DEFAULT ''` (comma-separated). A store created before this change is migrated in `Store.__init__` with `ALTER TABLE notes ADD COLUMN tags ...` when the column is missing.
- Only `notes/store.py` touches sqlite (ADR-0003 holds; cli uses `Store.add(text, tags)` and `Store.all(tag)`).

## Slices (TDD)

| Test | RED: command and failing line | GREEN: result | Commit |
|------|-------------------------------|---------------|--------|
| `CliTest.test_add_with_tag_stores_it` | `python3 -m unittest tests.test_notes.CliTest.test_add_with_tag_stores_it` → `error: unrecognized arguments: --tag work` (argparse SystemExit 2) | 4/4 OK | 4605451 `feat: tag notes on add` |
| `CliTest.test_list_filters_by_tag` | `python3 -m unittest tests.test_notes.CliTest.test_list_filters_by_tag` → `error: unrecognized arguments: --tag work` | 5/5 OK | 7e18f59 `feat: filter list by tag` |
| `StoreTest.test_store_created_before_tags_still_opens` | `python3 -m unittest tests.test_notes.StoreTest.test_store_created_before_tags_still_opens` → `sqlite3.OperationalError: no such column: tags` | 6/6 OK | d576120 `feat: migrate pre-tag stores to add the tags column` |

## Tests
- Full suite: `python3 -m unittest` → `Ran 6 tests in 0.162s` / `OK`, output pristine.
- Manual smoke (temp DB via NOTES_DB): `add --tag work --tag urgent "Call Ann"`, `add "Buy milk"`, `list --tag work` prints only "Call Ann"; `list` prints both.

## Files changed
- notes/model.py: `Note.tags`
- notes/store.py: schema, migration, `add(text, tags=())`, `all(tag=None)`, `_note` row helper
- notes/cli.py: `add --tag` (append), `list --tag`
- tests/test_notes.py: three tests above; `import sqlite3`

## Deviations / concerns
- **Commit count:** the brief's global constraint says one commit per task, with message `feat: tag notes and filter list by tag`. The dispatch says commit each green slice. I followed the dispatch: three commits, each with its test and code. If you want one commit, squash the three before merge (`git reset --soft d7bf255 && git commit`), which I did not do.
- **Commas in tags:** tags are stored comma-joined and split on read, with no validation. A tag containing a comma (e.g. `--tag "a,b"`) is read back as two tags. Not covered by the plan; I did not add validation.
- **Task 1 not on this branch:** Task 1 (newest-first search) is not in this branch. It edits `Store.search` (`ORDER BY id`), and my change also touches the `search` SQL line, so a merge may conflict there.
- `search` output does not show tags; the plan did not ask for it.
- Self-review: renamed `_note`'s unpacked `id` to `note_id` to avoid shadowing the builtin. Otherwise no further findings.

## Repo hygiene note
My first three commits accidentally included `__pycache__/*.pyc` files. I rewrote only my three commits (`filter-branch` on `d7bf255..master`) to drop them, so the SHAs above are the rewritten ones. Suite re-run after the rewrite: `Ran 6 tests` / `OK`.
