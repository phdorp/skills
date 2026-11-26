# 4. Export notes as JSON Lines through an `export` command

## Status

proposed

## Context

Users want to back up their notes and move them to other tools. No requirement R-n covers
export yet; the architect should confirm one. The export must not lose or corrupt notes
(R-2, QG-1), must add no dependency (R-3, QG-2), and must leave the store's internals
untouched (QG-3, QS-3, ADR-0003). Import and export formats and CLI command names are decided
centrally (ADR-0002). CSV was considered and rejected: quoting multi-line text is fragile and
it loses types. A single JSON array was rejected: a truncated file is not valid at all.

## Decision

We will add an `export` command. It writes every note as JSON Lines: UTF-8, one JSON object per
line, ordered by `id`. Each object has the keys `id` (integer), `text` (string), and `created`
(string, ISO 8601 UTC, as stored).

- `python3 -m notes export` writes to stdout.
- `python3 -m notes export PATH` writes to `PATH`. It writes a temporary file in the same
  directory and renames it into place only when complete. If `PATH` already exists, the command
  fails without touching it.
- Success exits 0. Errors go to stderr as `notes: <message>` with exit code 1 (arc42 section 8).

The export reads notes through `Store.all()` and serializes `Note` values with the standard
library `json` module. Only the `cli` block calls the export; no module other than `store`
imports `sqlite3`.

## Consequences

- Easier: no new dependency; each line is a complete note, so a truncated file is detectable
  and tools can stream it; the atomic rename means an interrupted export never leaves a
  partial file at `PATH`.
- Harder: spreadsheets do not open JSON Lines directly. The format has no version field; a
  change to the keys needs a new ADR.
- Import is not covered. An import command needs its own ADR, because the format is central.
- ADR-0001 is unaffected: the on-disk storage format does not change. ADR-0003 is kept:
  `Store.all()` already exists, so no new `Store` method is needed.
