# 2. Keep the pantry in an append-only file

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/store.py` (`path`, `_append`). This decision is on the accepted list in ADR 0001 (storage engine and on-disk format). It serves R-2 and QG-1 (crash safety) and R-3 (no packages needed).

## Decision

We will keep the pantry in one append-only file at `PANTRY_FILE` (default `~/.pantry.jsonl`). Each change is appended as one record, and the file is flushed and fsynced before the command returns.

## Consequences

Reads replay the whole file, and the file grows with every change. The crash handling is incomplete: see arc42 section 11 (torn last line, directory not fsynced). Changes to how `store` writes or repairs the file wait for this ADR's approval.
