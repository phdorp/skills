# 0002. The pantry file is an append-only JSON Lines log

## Status

proposed

## Context

As found in the code, not yet decided by the architect: `pantry/store.py:13-17` appends each record as one JSON line and fsyncs it; `pantry/store.py:20-30` replays the file and skips lines that do not parse; `pantry/model.py:19-27` derives the current items from `add` and `remove` records. This serves R-2 (no item is lost if the machine crashes mid-write). It is a central decision under ADR-0001.

## Decision

We store the pantry as an append-only file of JSON Lines at `PANTRY_FILE`, or `~/.pantry.jsonl` when it is not set. Each change is one `add` or `remove` record, appended and fsynced. The items are the result of replaying the records in order.

## Consequences

A crash mid-append can leave a torn last line, which the reader skips. As found, the next append joins that line and is then lost, so R-2 is not met as written (arc42 section 11). Fixing this changes the write rule, which is a decision for the architect. Work on the write rule waits until this ADR is accepted.
