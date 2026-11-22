# 2. Pantry file: append-only JSON lines, replayed on read

## Status

proposed

## Context

Found in the code (`pantry/store.py`, `pantry/model.py`), not decided by the architect. The file is the storage and its format is on the list of decisions made centrally (ADR-0001). It serves R-1 (no item is lost if the machine crashes mid-write; QG-1 recoverability) and R-2 (add, list and remove).

## Decision

As found: the pantry file is `$PANTRY_FILE`, or `~/.pantry.jsonl` when that is unset. It holds one UTF-8 JSON object per line: `{"op": "add", "name": ..., "expires": "YYYY-MM-DD"}` or `{"op": "remove", "name": ...}`. Each command appends one record, flushes it and calls fsync before it returns; no record is rewritten. The pantry's state is the result of replaying the records in file order. A line that does not parse is skipped on read.

## Consequences

Easy: a crash can only affect the record being written. Hard: the whole file is read on every command and it is never compacted. Current code does not yet meet R-1, because a record cut short by a crash is followed by the next record on the same line, which loses that next record (arc42 section 11).
