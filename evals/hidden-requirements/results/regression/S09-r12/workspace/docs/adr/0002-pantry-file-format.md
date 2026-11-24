# 2. Pantry file format: JSON Lines event log

## Status

proposed

## Context

*As found, unconfirmed.* Found in `pantry/store.py` and `pantry/model.py`. Serves R-2 (QG-1): records are never rewritten, so an earlier state survives a failed write. Serves R-3 (QG-2): the file is plain text, read with the standard library.

## Decision

We will store the pantry as JSON Lines at `PANTRY_FILE`, or `~/.pantry.jsonl` when it is unset. Each line is one record: `{"op": "add", "name": ..., "expires": "YYYY-MM-DD"}` or `{"op": "remove", "name": ...}`. The current items are the result of replaying the records in order.

## Consequences

The file grows with every change, and every command replays all of it. Changing the format breaks existing files and needs a migration, decided in its own ADR. Writing the write rule is decided in ADR-0003.
