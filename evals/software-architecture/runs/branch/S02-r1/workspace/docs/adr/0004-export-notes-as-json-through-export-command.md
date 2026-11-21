# 4. Export notes as versioned JSON through an `export` command

## Status

proposed

## Context

Users want to back up their notes and move them to other tools. Notes must not be lost (R-2,
QG-1, QS-1), and the program stays on the standard library (R-3, QG-2). The export need is not
yet a requirement in arc42 section 1; the architect should decide whether to add it. ADR-0002
puts import and export formats and CLI command names on the central list, so this decision needs
an accepted ADR. Reads must go through `Store` (ADR-0003). `json` is in the standard library.

## Decision

We will export all notes as one UTF-8 JSON document, indented two spaces, of this shape:

```json
{"format": "notes-export", "version": 1,
 "notes": [{"id": 1, "text": "Buy milk", "created": "2026-10-01T09:00:00+00:00"}]}
```

Notes appear in id order. `id`, `text` and `created` carry the values `Store` returns, unchanged.

We will add the subcommand `python3 -m notes export [PATH]`:

- without `PATH`, the document goes to stdout;
- with `PATH`, the document is written to a temporary file in the same directory and renamed to
  `PATH` only when complete, so a failed export never leaves a truncated file;
- if `PATH` already exists, the command fails and writes nothing (no overwrite flag in this
  decision);
- it exits 0 on success and 1 on error, reporting errors as `notes: <message>` on stderr (arc42
  section 8);
- it only reads the store and uses the same location as the other commands (`NOTES_DB` or
  `~/.notes.db`).

Notes are read with `Store.all()`. The JSON is produced in the `cli` block, which already uses
`Note`; no new building block or dependency is added.

Importing a file is not decided here. A later import decision must read this format.

## Consequences

Backups are plain text, readable with any JSON tool, and carry the `version` field so future
formats can be told apart. Refusing to overwrite protects existing backups at the cost of one
extra step when re-exporting to the same name. Keeping the serializer in `cli` makes `cli` the
only place that knows the export format; if the format grows, that module will be the place to
split out, which needs its own ADR. Storage (ADR-0001, ADR-0003) is unchanged. Work on the
`export` command waits until this ADR is accepted (ADR-0002). A later import ADR must accept
the same format and its `version` field.
