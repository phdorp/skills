# 4. Export notes as JSON Lines through an `export` command

## Status

proposed

## Context

Users want to back up their notes and move them to other tools. No existing requirement covers
export (R-1 covers add, list and search only). Users keep notes for years, so the export must not
lose or alter any note (in the spirit of R-2). The export must work with the
standard library only (R-3, QG-2) and must not weaken the storage rules: all reads go through
`Store` (ADR-0003, QG-3). The export format and the CLI command name are decided centrally
(ADR-0002). No requirement ID exists yet for export; see the report.

## Decision

We will export all notes in **JSON Lines**: UTF-8 text, one JSON object per note, one note per
line, ordered by `id`. Each object has exactly the three fields of the `Note` value:
`id` (integer), `text` (string), `created` (the stored ISO 8601 UTC string, unchanged).
JSON string escaping keeps every note on one line, even when its text contains newlines.

We will add a subcommand `export` to the CLI:

- `python3 -m notes export` writes the JSON Lines to stdout, so users can redirect it
  (`> backup.jsonl`).
- `python3 -m notes export -o PATH` writes to a file. If `PATH` already exists, the command fails
  with `notes: PATH already exists` and exit code 1; it never overwrites.
- A file export is written to a temporary file in the same directory and renamed to `PATH` only
  when complete, so a failed or interrupted export never leaves a partial file at `PATH`.

Serialization lives in a new block `notes/export.py`, which may use `model` only. `cli.py` calls
`Store.all()` and passes the notes to `export.py`. The export only reads; it never changes the
database. Errors follow arc42 section 8: `notes: <message>` on stderr, exit code 1.

Not in this decision: import, other formats (CSV, Markdown), encryption of the export, and sync
(R-4, deferred).

## Consequences

- Easier: any tool with a JSON parser can read a backup (`jq`, Python, spreadsheets via
  conversion). Shell redirection and the atomic file write give safe backups.
- Harder: JSON Lines is not a spreadsheet format; users who need CSV must convert it. The
  `id` and `created` values are not re-created on import, so a future import command has to decide
  whether to keep or reassign ids (that needs its own ADR).
- Other ADRs: ADR-0003 is respected (only `store.py` reads the database). The new block
  `notes/export.py` changes the dependency rule in arc42 section 5 (`cli` → `store` → `model`
  plus `cli` → `export` → `model`). That change is the architect's to accept, and arc42 is not
  edited by this ADR.
- Work that follows: a `notes export` implementation with tests for: empty store, newlines and
  non-ASCII text, existing `PATH` refused, and failed write leaves no file at `PATH`.
