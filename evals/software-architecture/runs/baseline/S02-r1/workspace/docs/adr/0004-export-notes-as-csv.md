# 4. Export notes as CSV through `notes export`

## Status

proposed 2026-11-21. Building the export waits until the architect accepts this ADR (ADR-0002).

## Context

Users keep asking for a way to back up their notes and move them to other tools. The export
must not lose or truncate notes (R-2, QS-1), must use only the standard library (R-3, QG-2),
and must not give the CLI direct access to the database (ADR-0003).

Options considered:

- JSON Lines: lossless and typed, but few note and spreadsheet tools import it directly.
- Markdown: readable, but has no reliable way to read back the id and creation time.
- Copying `~/.notes.db`: a complete backup, but SQLite is binary and other tools do not read it.

## Decision

**Format.** CSV as defined by RFC 4180: UTF-8 without byte-order mark, CRLF line endings (the
default of Python's `csv` module), header row `id,created,text`, one row per note, ordered by
id. `created` is written exactly as stored (ISO 8601, UTC, seconds precision). `text` is written
unchanged; the `csv` module quotes fields as RFC 4180 requires.

**Command.** `python3 -m notes export PATH`. The name follows the existing verbs `add`, `list`
and `search`.

- `PATH` is required. `-` writes to standard output.
- If `PATH` already exists, the command exits with code 1 and writes nothing, unless `--force`
  is given.
- For a file `PATH`, the export is written to a temporary file in the same directory, flushed
  and fsynced, then moved over `PATH` with `os.replace`. A crash never leaves a truncated file
  at `PATH`.
- Notes come from the database at `default_path()`, so `NOTES_DB` is respected.
- Success exits 0 and prints nothing on stdout (when `PATH` is a file). Errors follow arc42
  section 8: `notes: <message>` on stderr, exit code 1. Argparse usage errors keep exit code 2.

**Structure.**

- `notes/cli.py` adds the `export` subcommand and reads the notes with `Store.all()`. No new
  `Store` method is needed.
- The CSV writing lives in a new module `notes/export.py`. It imports only `notes.model` and
  the standard library, and takes notes and a text stream as arguments. It does not touch the
  database.

Import is out of scope. A future import command, and any other export format, needs its own
ADR.

## Consequences

- An export is a logical copy. It does not replace copying the SQLite file, which remains the
  complete copy. The README should say so.
- Spreadsheets may read a `text` value that starts with `=`, `+`, `-` or `@` as a formula. The
  export does not escape such values, so the data stays unchanged. Users should import the file
  as text.
- All values are text in the file, so `id` must be parsed as an integer by the importing tool.
- The header and column order are part of the format. Changing them later breaks users' scripts
  and is a new ADR.
- Tests should cover: commas, quotes, newlines and non-ASCII text round-tripping through
  `csv.reader`; refusal to overwrite without `--force`; `-` writing to stdout; and an empty store
  producing only the header row.
- Work for the building team: add `export.py` to the building-block table in arc42 section 5,
  add an export requirement to arc42 section 1, and add an export example to the README.
