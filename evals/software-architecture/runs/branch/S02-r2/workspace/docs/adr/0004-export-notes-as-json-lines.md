# 4. Export notes as JSON Lines through `notes export`

## Status

accepted 2026-11-21

## Context

Users ask to export their notes so they can back them up and move them to other tools. This
adds a requirement: proposed R-6, "Users export all their notes to a file they can keep as a
backup and import into other tools", not yet in arc42 section 1.

The export must:

- keep every note exactly: the text (which may contain any characters, including newlines,
  since `notes add` takes arbitrary text), the id, and the creation time (R-2, QS-1 spirit);
- use only the standard library (R-3);
- read notes only through `Store` (ADR-0003);
- use a format and command name that are decided centrally (ADR-0002).

## Decision

### Format: JSON Lines

The export is UTF-8 text with one note per line, in ascending `id` order. Each line is a JSON
object with exactly three keys:

- `id`: integer, the note id;
- `created`: string, the creation time as stored (ISO 8601, UTC);
- `text`: string, the note text.

Example:

```json
{"id": 1, "created": "2026-10-03T08:15:00+00:00", "text": "Buy milk"}
{"id": 2, "created": "2026-10-03T08:16:12+00:00", "text": "Line one\nLine two"}
```

Each record is written with `json.dumps(..., ensure_ascii=False)` and terminated by `\n`.
Newlines inside `text` are escaped by JSON, so every record is exactly one line. There is no
header line and no wrapping array, so each line parses on its own, and a damaged line does not
make the rest of the file unreadable.

Rejected alternatives:

- **CSV**: quoting and embedded-newline handling differ between tools, and it has no types.
  A CSV variant may be added later as an option; it is not part of this decision.
- **Plain text or Markdown**: lossy (ids and timestamps are easily lost) and not re-importable.
- **SQLite file copy**: a faithful backup of the database, but tied to our schema, and no
  other tool reads it as notes.
- **One JSON array**: the whole file is invalid if the write is interrupted, and it cannot be
  streamed.

### Command: `notes export [PATH]`

- `python3 -m notes export` writes the export to stdout. Nothing else is printed to stdout.
  Output is always UTF-8, independent of the terminal locale.
- `python3 -m notes export PATH` writes the export to a new file at `PATH`.
  - If `PATH` already exists, the command fails with `notes: <PATH> already exists` and exit
    code 1. It never overwrites a file. (`--force` is not part of this decision.)
  - The file is first written to a temporary file in the same directory, flushed and fsynced.
    It is then put in place without overwriting anything (for example `os.link`, not
    `os.replace`). A crash leaves either no file at `PATH` or a complete one.
  - Nothing is printed on success.
- Errors follow arc42 section 8: `notes: <message>` on stderr, exit code 1. Success is exit
  code 0.

### Code layout

- A new block `notes/export.py` formats records. It may use `model` only and takes notes and
  an output stream as arguments. It does not import `sqlite3` and does not open files itself.
- `notes/cli.py` gets the notes with `Store.all()`, passes them to `export.py`, and handles
  the output destination and the file-creation rules above.
- The dependency rule `cli → store → model` in ADR-0002 is unchanged. `export` is added as a
  block that uses only `model`.

Import is not decided here. It needs its own ADR when it is wanted.

## Consequences

- No storage change is needed. `Store.all()` already provides the data, and the store stays
  the only module that touches the database (ADR-0003).
- The export reads all notes into memory before writing, the same as `notes list` does today.
  That is fine for short notes. If the store grows large enough to matter, the export can
  stream rows instead; the output format stays the same.
- The export files are plain UTF-8 text. Users can open them in an editor, unlike the binary
  database (ADR-0001).
- Adding fields later is compatible with existing readers if the new keys are optional. Any
  change that alters or removes a key needs a new ADR.
- Acceptance tests the team should write before merging:
  - round trip: `add` notes with unicode, quotes, and embedded newlines; export; parse each
    line with `json.loads`; the texts, ids, and creation times match the store;
  - an empty store produces an empty output;
  - `export PATH` refuses an existing `PATH` with exit code 1 and leaves the file unchanged;
  - `export PATH` leaves no temporary file behind on success.
- When this ADR is accepted, arc42 needs two edits, which are not part of this ADR: add R-6 to
  the requirements table in section 1, and add the `export` block to the building block table
  in section 5.
