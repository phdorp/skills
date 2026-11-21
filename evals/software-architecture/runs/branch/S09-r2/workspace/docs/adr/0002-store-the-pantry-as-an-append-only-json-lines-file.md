# 2. Store the pantry as an append-only JSON Lines file

## Status

proposed

## Context

Found in the code, not decided: `pantry/store.py` (`path`, `_append`, `_records`) writes each add or remove as one line and never rewrites the file. Serves R-2 (QG-1) and R-3 (QG-3, no database).

## Decision

We will keep the pantry in one JSON Lines file, `~/.pantry.jsonl` or the path in `PANTRY_FILE`, and only ever append to it.

## Consequences

A crash can leave a partial last line, and the next append is glued onto it (arc42 section 11, risk 1). The file grows without bound; there is no compaction. Corrupt lines are handled under ADR 0007.

Question for the architect: keep the append-only file?
