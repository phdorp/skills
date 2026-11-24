# 2. Append-only JSON Lines pantry file

## Status

proposed

## Context

Found in the code, not decided by the architect: `pantry/store.py` appends one JSON record per add or remove to `~/.pantry.jsonl` (or `PANTRY_FILE`) and calls `fsync` after each write; reads replay the records in order (`pantry/model.py`, `replay`). This serves R-2 (QG-1) and R-1 (QG-2). The format does not yet meet R-2: a torn last line breaks the next append (arc42 section 11).

## Decision

We store pantry items as an append-only JSON Lines file. Each add or remove is one record, `{"op": "add", ...}` or `{"op": "remove", ...}`, and the items are the result of replaying the records in order.

## Consequences

Appends are simple to reason about after a crash. The file grows with history and is never compacted. A change to the write path, such as a fix for a torn last line, changes this decision and needs its own ADR.
