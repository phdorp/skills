# 2. Store items in an append-only JSON Lines file

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/store.py` appends one JSON record per line to the file
at `PANTRY_FILE` or `~/.pantry.jsonl`, and `store.items()` replays all records through
`pantry/model.py` (`replay`). It serves R-2 (its crash goal, QG-1, is still open and named here
in words) and R-3 (QG-3).

## Decision

We will keep the pantry file append-only: one JSON record per line, never rewritten, and
replayed in full on each read.

## Consequences

Removing an item appends a removal record; the file only grows (arc42 section 11). Crash
handling of the appends is decided in ADR-0003.
