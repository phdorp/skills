# 2. Append-only JSON Lines storage

## Status

proposed

## Context

Found in the code, not decided by anyone yet: `pantry/store.py` and `pantry/model.py`. It is a decision on the list in ADR 0001 (storage format). It serves crash-safe storage (R-2, QG-1) and the standard-library-only runtime (R-3).

## Decision

We will keep pantry items in an append-only JSON Lines file at `~/.pantry.jsonl`, overridable with `PANTRY_FILE`. Each line is an `add` or `remove` record, and the items are the result of replaying those records in order.

## Consequences

Each append is flushed and fsynced. A line cut short by a crash is skipped on read. But a partial line followed by a later append puts that append on the same line, so it is lost (arc42 section 11). Changing the format needs a superseding ADR and a migration of existing files.
