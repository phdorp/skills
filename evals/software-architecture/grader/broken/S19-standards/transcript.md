### user

Review the last commit.

### assistant

# Review of HEAD~1..HEAD

## Standards

- Critical (ADR-0003): `notes/cli.py` imports `sqlite3` and opens the database itself:
  `db = sqlite3.connect(default_path())`. Fix: add `Store.export()` and call it.
- Important (QS-3): a contributor swapping the storage engine now has to change `notes/cli.py`
  too, so the measure "0 other files changed" no longer holds.
- Important (arc42 §8: errors go to stderr as `notes: <message>`, exit 1): a missing table ends
  in a Python traceback. Fix: wrap the export in the same try/except.
- Important (traceability): ADR-0004 is accepted but its Context names no R-, QG- or QS-ID.
  Fix: name the requirement it serves (R-1).

## Spec

- No findings: `notes export` prints one JSON line per note with `id`, `text` and `created`, oldest first.

Worst: Critical (ADR-0003).

### result (success)
