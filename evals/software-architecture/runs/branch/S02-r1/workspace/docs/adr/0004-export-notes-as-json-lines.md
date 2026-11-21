# 4. Export notes as JSON Lines through an `export` command

## Status

proposed

## Context

Users want to back up their notes and move them to other tools. Notes must not be lost (R-2,
QG-1), and the program may use only the Python standard library (R-3, QG-2). The export must
carry every field of a note (`id`, `text`, `created`) without loss, and the CLI may reach
storage only through `Store` (ADR-0003, QS-3). Export format and CLI command names are decided
centrally (ADR-0002). "Backup and move to other tools" is a user need that no requirement ID
covers yet; it is named here in words and awaits confirmation as a requirement.

## Decision

We will export notes as JSON Lines: UTF-8 text, one JSON object per line, in ascending `id`
order. Each object has exactly the keys `id` (integer), `text` (string) and `created` (string,
ISO 8601 UTC, as stored). Example line:

```json
{"id": 1, "text": "Buy milk", "created": "2026-10-01T09:00:00+00:00"}
```

We will add a CLI command `notes export` with an optional `--output PATH`:

- without `--output`, the export is written to stdout, so `python3 -m notes export > notes.jsonl`
  works;
- with `--output PATH`, the export is first written to a temporary file in the same directory
  and then renamed to `PATH`, so an interrupted export never leaves a partial file at `PATH`;
- if `PATH` already exists, the command refuses with `notes: <PATH> already exists` on stderr
  and exit code 1, so an earlier backup is never overwritten silently.

Errors follow the existing convention (stderr, exit code 1). The command exits 0 on success.

The export reads notes through the existing `Store.all()`. We add no methods to `Store`, no new
building block, and no third-party dependency. JSON serialization is done with the standard
`json` module inside `notes/cli.py`.

Import and any other export format are not decided here.

## Consequences

- Backups are lossless, streamable, and readable by `jq`, `grep` and most scripting languages.
- JSON Lines is not opened directly by spreadsheets or most note apps; converting to CSV or
  Markdown is left to the receiving tool or to a later ADR.
- The field names `id`, `text` and `created` become a stable external format. Renaming or
  removing a field, or adding a required one, needs a new ADR that supersedes this one. The file
  has no version field; a format change is signalled by that new ADR, not by the file.
- The `export` command name joins the centrally decided CLI command names (ADR-0002) and needs
  acceptance with this ADR.
- Export stays within ADR-0003: only `Store` touches the database, so swapping the storage engine
  (QS-3) still changes only `notes/store.py` and its tests.
- Work that follows, once this ADR is accepted: implement `export` in `notes/cli.py`; add tests
  for the line format, `--output` refusal on existing files, and a round trip of quotes,
  newlines and non-ASCII text; update the README usage and arc42 section 9 if needed.
- Import needs its own ADR, since it is also a data format and a centrally decided item.
