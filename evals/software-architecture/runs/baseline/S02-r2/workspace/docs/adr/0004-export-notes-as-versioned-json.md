# 4. Export notes as one versioned JSON document through an `export` command

## Status

proposed 2026-11-21

Building waits until the architect accepts this ADR (ADR-0002).

## Context

Users want their notes for backup and to move them to other tools (R-6). Two decisions in
ADR-0002's central list are involved: the export format, and the CLI command name.

The notes are short text with an id and a creation time, and nothing else. A backup has to keep
every field exactly, including newlines, commas, quotes and non-ASCII text. The file must also
carry its own format version so that a later import or a format change can tell what it reads.

Options considered for the format:

- **CSV**: spreadsheets open it, but the header and quoting rules are fragile, and it has no
  version marker. Rejected as the backup format; a CSV export can come later as a separate format.
- **Markdown**: readable, but there is no reliable way to get the id and time back out.
  Rejected.
- **JSON Lines**: lossless and streamable, but it has no place for a version marker without a
  special first line.
- **One JSON document with a version envelope**: lossless, versioned, and readable with the
  standard library (`json`) or with `jq`. Chosen.

Options considered for the CLI: a separate `backup` command, or a `--export` flag on `list`.
Both were rejected, because `export` is the name users will look for and `list` already has a
fixed output format.

## Decision

Add an `export` command with this interface:

```
python3 -m notes export              # writes the JSON document to stdout
python3 -m notes export -o FILE      # writes to FILE
python3 -m notes export -o FILE --force   # replaces FILE if it exists
```

The document is UTF-8 JSON with `ensure_ascii` off. Its shape is:

```json
{
  "format": "notes-export",
  "version": 1,
  "exported": "2026-11-21T10:00:00+00:00",
  "notes": [
    {"id": 1, "text": "Buy milk", "created": "2026-10-01T08:00:00+00:00"}
  ]
}
```

- `format` is always `"notes-export"`. `version` is `1`. A later change to the shape increments
  `version`; readers reject versions they do not know.
- `exported` is the UTC time of the export, in the same ISO 8601 form the store uses for
  `created`.
- `notes` lists every note in ascending `id` order, with `id`, `text` and `created` copied
  exactly from the store. Empty stores export `"notes": []`.

Behaviour:

- Without `-o`, the document goes to stdout and nothing else is printed, so `export > backup.json`
  works.
- With `-o FILE`, the document is written to a temporary file in the same directory and then
  renamed to `FILE`, so an interrupted export never leaves a half-written file. If `FILE` exists
  and `--force` is not given, the command fails before writing anything.
- A file written by `export` is created with mode `0600`, because notes can be private.
- Errors go to stderr as `notes: <message>` with exit code 1, as in arc42 section 8. Success
  exits 0.

Layering: the export reads notes only through `Store.all()`. The serialisation may live in
`notes/cli.py` or in a helper module that imports only `notes.model`; it must not import
`sqlite3` (ADR-0003).

Not in this decision: importing (restoring) an export, and other formats such as CSV or
Markdown. Each needs its own ADR, and the `version` field is what allows them to be added.

## Consequences

- Backups are lossless for `id`, `text` and `created`. Ids are not guaranteed to be kept when an
  export is imported later, because an import may renumber notes.
- The format is plain JSON, so other tools can read it without this program.
- The `export` command is a new entry in the CLI command list that ADR-0002 keeps central.
  Future changes to the document shape need a new `version` and an ADR.
- Required tests before the feature is merged: an export round trip (store → document → parsed
  list equals the stored notes, including newlines, quotes and non-ASCII text); an empty store;
  refusal to overwrite without `--force`; and a check that a failed `-o` write leaves no file.
- Exporting a large store builds the whole document in memory. This is acceptable for the
  short-note scale in arc42 section 2; it should be revisited if notes grow large.
