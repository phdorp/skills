# 4. Export notes as one JSON document through an `export` command

## Status

proposed 2026-11-21

## Context

Users ask to export their notes to back them up and to move them to other tools. The export
must not lose any note (R-2, QG-1), must run with only the standard library (R-3, QG-2), and
must keep the storage behind `Store` (ADR-0003, QS-3). Import and export formats and CLI
command names and exit codes are decided centrally (ADR-0002). The architect has not yet
confirmed "export notes for backup and move to other tools" as a numbered requirement; this
ADR cites R-2 and R-3 until it is.

## Decision

We will export all notes as one UTF-8 JSON document:

```json
{
  "format": "notes-export",
  "version": 1,
  "notes": [
    {"id": 1, "text": "Buy milk", "created": "2026-11-21T09:00:00+00:00"}
  ]
}
```

`created` is the ISO 8601 UTC string the store already holds. The document is written with
two-space indentation.

We will add the command `python3 -m notes export`:

- with no option, it writes the document to standard output, so `notes export > backup.json`
  works;
- with `-o PATH`, it writes to `PATH`. It refuses to overwrite an existing file and writes to
  a temporary file in the same directory, then renames it into place, so a failed export never
  leaves a partial file;
- exit code 0 on success; exit code 1 on any error, reported on stderr as `notes: <message>`
  (arc42 section 8).

The serialisation lives in a new module `notes/export.py`. It takes `Note` values and returns
text; it does not touch SQLite. `cli` gets the notes from `Store.all()`.

We will not add a `--format` option now. CSV, Markdown, and a copy of the SQLite file were
considered and rejected: CSV has no version field and needs fragile escaping for multi-line
text; Markdown cannot be read back reliably; a copy of the SQLite file ties users to the
storage engine (ADR-0001), which is the opposite of moving to other tools.

## Consequences

Users get a plain-text, self-describing backup that any tool can read, and the `version` field
lets a later import command check what it reads.

`cli` gains a dependency on `export`, and `export` depends only on `model`. The dependency rule
in ADR-0002 (`cli` → `store` → `model`) becomes `cli` → `export` → `model` alongside it. arc42
section 5 needs a row for `export` once this ADR is accepted.

The export loads all notes into memory. That is fine for short notes; it would need revisiting
at a much larger scale.

Import is not part of this decision. A new ADR will cover it, and it must check `version`.

No accepted ADR is changed. ADR-0001 and ADR-0003 are unaffected because the export never
opens the database file.
