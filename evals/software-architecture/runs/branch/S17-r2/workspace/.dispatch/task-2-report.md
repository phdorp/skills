# Task 2 report: Tags

## What was implemented

- `notes add --tag <name>` (repeatable) stores the tags on the note.
- `notes list --tag <name>` prints only notes carrying that tag.
- The `notes` table has a `tags` column (comma-separated text, default `''`). Stores created before
  this change are migrated on open with `ALTER TABLE notes ADD COLUMN tags ...`.
- `Note` gains `tags: tuple = ()`. `Store.add(text, tags=())` and `Store.all(tag=None)` take the new
  arguments. `Store.search` returns tags too.

## Testing

Command: `python3 -m unittest` (run in the foreground after each slice and at the end).
Final output:

```
Ran 6 tests in 0.156s
OK
```

Baseline before the task: 3 tests, OK. Smoke check with `python3 -m notes` against a scratch DB:
`add --tag work --tag urgent "Call Ann"`, `add "Buy milk"`, `list --tag work` printed only "Call Ann",
and `list` printed both.

## Slices

| Test | RED: command and failing line | GREEN: result | Commit |
|------|-------------------------------|---------------|--------|
| `CliTest.test_add_with_tag_stores_tag` (`add --tag work "Call Ann"` stores the tag) | `python3 -m unittest tests.test_notes.CliTest.test_add_with_tag_stores_tag` → `main(["add", "--tag", "work", "Call Ann"])`: argparse `SystemExit: 2` (unrecognized `--tag`) | OK, 4/4 | fd69147 `feat: add --tag to notes add` |
| `CliTest.test_list_with_tag_prints_only_tagged_notes` (`list --tag work` prints only tagged) | `python3 -m unittest tests.test_notes.CliTest.test_list_with_tag_prints_only_tagged_notes` → errors (argparse rejects `list --tag`) | OK, 5/5 | b23ed66 `feat: filter notes list by tag` |
| `LegacyStoreTest.test_store_created_before_tags_still_opens` | `python3 -m unittest tests.test_notes.LegacyStoreTest` → `sqlite3.OperationalError: no such column: tags` | OK, 6/6 | da5a515 `feat: migrate pre-tag stores to add the tags column` |

## Files changed

- `notes/model.py`: `Note.tags`.
- `notes/store.py`: schema, migration, `add`/`all`/`search`, `_note` row helper.
- `notes/cli.py`: `add --tag`, `list --tag`.
- `tests/test_notes.py`: three new tests (one class `LegacyStoreTest`).

## Self-review findings

- Tags are stored comma-joined. A tag containing a comma (`--tag "a,b"`) is silently read back as two
  tags. I did not add validation because the plan does not mention it. It is a concern, see below.
- The legacy test creates the old-schema file with the `sqlite3` module directly. ADR-0003 says only
  `notes/store.py` imports `sqlite3`. The test is the only other place that does, and it is needed to
  build a pre-change store. Flagging it for the architect.
- Adding `--tag` to `add` and `list` extends the CLI surface. ADR-0002 lists "CLI command names and
  exit codes" as centrally decided. No command was added or renamed, only options. Flagging in case
  the architect wants that covered by an ADR.

## Issues and concerns

1. **Commit count vs. plan.** The plan's global constraint says "one commit per task", and its Step 2
   names the commit `feat: tag notes and filter list by tag`. The dispatch asks for a commit per green
   slice. I followed the dispatch: three commits, listed above. If one commit is required, the three
   can be squashed into one with that message.
2. **Comma in tag names** (see self-review). Unvalidated.
3. Task 1 (search order) was not touched. Task 2 changed the `search` SELECT and row mapping, so the
   two tasks will touch the same `search` method and may conflict when merged.

Status: DONE_WITH_CONCERNS.
