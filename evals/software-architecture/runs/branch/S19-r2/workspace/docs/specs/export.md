# Export notes as JSON

## Problem

Users cannot take their notes to other tools.

## Behaviour

`notes export` prints every note as one JSON line, oldest first:

```text
{"id": 1, "text": "Buy milk", "created": "2026-11-20T09:00:00+00:00"}
```

Each line holds the fields `id`, `text` and `created`. The command takes no arguments.

## Out of scope

Importing notes; other formats.
