# 4. Export notes as CSV through an `export` command

## Status

proposed

## Context

Users keep their notes for years (R-2, QG-1) and want to back them up and move them to other
tools. Export is a data format and a CLI command name, both decided centrally (ADR-0002). The
program may use only the standard library (R-3, QG-2), and the store is the only block that
reads notes (ADR-0003). Each note has three fields: an id, a UTC timestamp, and text that may
contain commas, quotes, and line breaks. Export is a copy: it must not risk the stored notes
(QS-1).

## Decision

We will add a command `python3 -m notes export [--output PATH]`.

- The output is CSV, UTF-8, with a header row `id,created,text`, written by Python's `csv`
  module (RFC 4180 quoting). CSV is read by spreadsheets and most note and database tools.
- `created` is the timestamp as stored (ISO 8601, UTC). `id` is kept, not renumbered.
- All notes are written, ordered by `id`. The command reads through `Store.all()`; the store
  gets no new method for it.
- Without `--output` the CSV goes to stdout, so `> backup.csv` works.
- With `--output PATH` the file is written to a temporary file in the same directory and then
  renamed to `PATH`, so a failed export never leaves a partial file. If `PATH` already exists,
  the command fails and leaves it untouched; it never overwrites.
- Errors follow arc42 section 8: message on stderr as `notes: <message>`, exit code 1. Success
  exits 0.
- Import is not part of this decision. It needs its own ADR.

## Consequences

Backups and moves to other tools work without new dependencies. Each note's text is stored as
a single CSV field, so the header and quoting rules must be kept stable; changing the columns
is a new ADR. The `cli` block does the CSV writing, since it only prints results; no new
building block is added, so arc42 section 5 stays unchanged. Because the export never
overwrites, users must delete an old file before exporting to the same name. The command adds
a fourth name to the CLI command list in README.md, which must be updated when this is
accepted and implemented.
