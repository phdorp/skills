# 4. Export notes as JSON Lines through `notes export`

## Status

accepted 2026-11-21

## Context

Users want to back up their notes and move them to other tools. A copy of the SQLite file
(ADR-0001) is a backup only for this program; other tools get no documented format from it.
Notes are free text and may contain newlines, quotes and non-ASCII characters, so the export
must be lossless for any note text. The program still uses only the standard library (R-3),
and notes are read only through `Store` (ADR-0003).

Formats considered:

- CSV: quoting rules differ between tools, and every field is text.
- One JSON array: not streamable; one damaged byte makes the whole file unreadable.
- Markdown: no clear structure for `id` and `created`; multi-line text is ambiguous.
- Raw SQLite copy: already exists as a backup, but is not portable.

## Decision

Export format: **JSON Lines**. One JSON object per note, one object per line, UTF-8 text,
ordered by ascending `id`. Each line ends with `\n`:

```json
{"id": 1, "text": "Buy milk", "created": "2026-11-21T10:00:00+00:00"}
{"id": 2, "text": "Call Ann\nabout the trip", "created": "2026-11-21T10:05:00+00:00"}
```

- Each object has exactly the keys `id` (integer), `text` (string) and `created` (string, as
  stored: ISO 8601, UTC, whole seconds).
- Written with Python's `json.dumps` using its default settings (non-ASCII escaped), so the
  output is ASCII-safe on any terminal or pipe.
- No header line and no wrapping array, so each line parses on its own.
- An empty store produces empty output and exit code 0.
- Readers must ignore keys they do not know. Adding a key is allowed without a new ADR.
  Renaming or removing a key, or changing its meaning, needs a new ADR.

CLI:

- `python3 -m notes export` writes to standard output.
- `python3 -m notes export -o FILE` writes to `FILE`.
- `--force` is required to replace an existing `FILE`. Without it, an existing `FILE` is an
  error and nothing is written.
- Writing to `FILE` is atomic: write a temporary file in the same directory, flush and fsync
  it, then rename it onto `FILE`. A failure leaves neither a partial `FILE` nor a temporary
  file behind. The temporary file is created with mode 0600, and `FILE` keeps that mode.

Exit codes for the CLI (this command and all existing ones):

- `0`: success.
- `1`: runtime error, reported on stderr as `notes: <message>` (arc42 section 8).
- `2`: invalid usage, as argparse reports it.

Building blocks (arc42 section 5):

- New block `export` (`notes/export.py`) turns notes into JSON Lines and may use only `model`.
- `cli` gets the notes from `Store.all()` and passes them to `export`. The dependency rule
  becomes `cli` → `store` → `model`, with `cli` → `export` → `model` alongside it.

Out of scope for v1: import or restore, other formats (CSV, Markdown), encryption, export
filtered by search term, and sync (R-4 is deferred).

## Consequences

- Build order for tomorrow:
  1. `notes/export.py` with a function that writes notes to a text stream.
  2. The `export` subcommand in `notes/cli.py`, with `-o`/`--force` and the atomic write.
  3. Tests: round trip of text with newlines, quotes and non-ASCII; empty store; existing
     `FILE` refused without `--force`; a failed write leaves no `FILE` and no temporary file.
  4. A usage line in `README.md` and the new block in arc42 section 5.
- `Store.all()` runs one `SELECT`, so the export is a consistent snapshot of the store.
- The export is a one-way copy. Until an import exists, this program cannot restore from it.
  The release notes must say so.
- The file is plain text. It can be read in an editor or with `jq`, unlike the SQLite file
  (ADR-0001). It also contains the note text unencrypted, so users must protect it.
- All notes are loaded into memory before writing. This is acceptable for short notes. Revisit
  it if stores grow large.
