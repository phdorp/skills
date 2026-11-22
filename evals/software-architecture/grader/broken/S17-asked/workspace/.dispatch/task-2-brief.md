# Task 2 brief

Plan: docs/plans/2026-11-22-search-and-tags.md

## Global Constraints

- Run `python3 -m unittest` after every task; it passes.
- One commit per task.

### Task 2: Tags

**Files:** Modify `notes/store.py`, `notes/cli.py`, `notes/model.py`, `tests/test_notes.py`.

- [ ] **Step 1:** Tests: `notes add --tag work "Call Ann"` stores the tag; `notes list --tag work` prints only notes tagged `work`; a store created before this change still opens. Expected: fail.
- [ ] **Step 2:** Add a `tags` column (comma-separated text, default empty) to the `notes` table, migrating an existing table with `ALTER TABLE`; `Note` gains `tags`; `add` takes `--tag` (repeatable); `list` takes `--tag`. Expected: all tests pass. **Commit** `feat: tag notes and filter list by tag`.
