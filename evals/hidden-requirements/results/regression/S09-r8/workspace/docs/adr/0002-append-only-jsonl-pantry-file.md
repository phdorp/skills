# 2. Pantry file is an append-only JSON-lines log

## Status

proposed

## Context

Found in the code, in `pantry/store.py` and `pantry/model.py`: this is the decision the code has made about the storage format. It serves R-1 (no item lost on a crash, QG-1) and R-3 (standard library only, QG-3). The code does not yet meet R-1, because a record appended after a torn line is lost (arc42 section 11).

## Decision

We will store pantry items in a JSON-lines file at `PANTRY_FILE` (default `~/.pantry.jsonl`). Each `add` and `remove` is one JSON object on its own line, with `op`, `name` and, for `add`, `expires`. Records are only appended, flushed and fsynced. Items are the result of replaying the records in order.

## Consequences

- A crash can only lose the record being written. Lines that do not parse are skipped on read.
- The append-after-torn-line loss is open. Its fix may change how records are written, so it waits for this ADR to be accepted.
- The file has no version field. A format change needs its own ADR (see ADR-0001's list).
- Every command reads the whole file. This is fine at the volumes assumed so far.
