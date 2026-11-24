# 2. Store the pantry as an append-only JSON-lines file

## Status

proposed

## Context

Found in the code, not decided: `pantry/store.py` and `pantry/model.py`. The write strategy
serves R-2 (QG-2, QS-2), which the code does not fully meet (arc42 section 11, risks 1 and 2).

## Decision

We will keep the pantry as an append-only file, one JSON record per line, at `PANTRY_FILE` or
`~/.pantry.jsonl`. Each change is appended and fsynced, and the items are the result of
replaying the records in order.

## Consequences

Earlier lines are never rewritten, so a crash can damage only the line being written. That
damaged line is still able to take the next append with it (arc42 section 11, risk 1); a fix
changes this write strategy and needs its own decision. The file grows without compaction (risk
4). Changing the record format is a file-format change on the ADR 0001 list.
