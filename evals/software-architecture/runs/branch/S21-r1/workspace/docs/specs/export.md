# Export notes to a file

## Problem

Users cannot take their notes to other tools.

## Behaviour

`notes export PATH` writes every note as one JSON line to `PATH`, oldest first:

```text
{"id": 1, "text": "Buy milk", "created": "2026-11-20T09:00:00+00:00"}
```

Each line holds the fields `id`, `text` and `created`. A crash during the export leaves either
the old file at `PATH` or the complete new one.

## Out of scope

Importing notes; other formats.
