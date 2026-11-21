# 4. Export notes as one JSON document via `notes export`

## Status

proposed

## Context

Users want to back up their notes and move them to other tools. This is a new need; it is not yet a requirement in arc42 section 1. The architect must confirm it and give it an R-n ID. The SQLite file is binary and cannot be read by other tools (ADR-0001), so the export must be a separate plain-text copy. The format and the command name are decided centrally (ADR-0002). The export may use only the standard library (R-3, QG-2), and it may reach notes only through `Store` (ADR-0003, QS-3).

## Decision

We will add a `notes export` command that writes every note as one UTF-8 JSON document:

```json
{
  "format": "notes-export",
  "version": 1,
  "notes": [
    {"id": 1, "text": "Buy milk", "created": "2026-10-01T09:00:00+00:00"}
  ]
}
```

- Notes appear in ascending `id` order, as `Store.all()` returns them. `created` is copied unchanged from the store.
- `notes export` writes to stdout. `notes export -o FILE` writes to FILE.
- If FILE already exists, the command fails with exit code 1 unless `--force` is given.
- Success exits with 0. Errors go to stderr as `notes: <message>` with exit code 1 (arc42 section 8).
- The command reads notes only through `Store.all()`. It adds no storage access.

Import is not decided here. A restore path needs its own ADR.

## Consequences

Any tool with a JSON parser can read the export. The `version` field lets a later format change be recognised. The export is a snapshot, not incremental.

The export holds note text in plain form, so the backup is unencrypted. Anyone with access to the file can read it. Writing the file with restricted permissions is not decided here.

Because `Store.all()` loads every note into memory, a very large store produces a large export in memory. This is acceptable for short notes, and the limit should be revisited if stores grow large.

ADR-0001 and ADR-0003 are unchanged. Store needs no new method.

Work that depends on this ADR waits until it is accepted (ADR-0002): the serialiser, the `export` subcommand, and their tests. Import, incremental export, and encryption are out of scope.
