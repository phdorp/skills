# 0002. Store pantry items in an append-only JSON Lines file

## Status

proposed

## Context

Found in `pantry/store.py` and `pantry/model.py`. Items must survive a crash mid-write (R-2,
QG-1), with only the standard library (R-3, QG-3).

## Decision

We will keep pantry items in an append-only JSON Lines file, one record per line. Records are
`add` (name, expiry as an ISO date) and `remove` (name). The current items are the result of
replaying the records in order: the last `add` for a name sets its expiry, and `remove` drops
the name. The default path is `~/.pantry.jsonl`; `PANTRY_FILE` overrides it.

## Consequences

Writes never rewrite earlier lines, so a crash can damage only the last one. The file grows
with every command and is read in full each time (section 11). The torn-line defect in
section 11 is not fixed by this ADR. A fix that changes the record format needs its own ADR.
