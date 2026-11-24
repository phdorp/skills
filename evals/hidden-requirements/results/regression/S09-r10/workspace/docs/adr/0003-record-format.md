# 3. Record each change as an add or remove record

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/model.py` (`Item.to_record`, `removal`, `replay`). This decision is on the accepted list in ADR 0001 (record format). It serves R-1 (the items it lists) and R-2 (the log is what survives a crash).

## Decision

We will write each change as one JSON object per line. An add record has the keys `op` (`"add"`), `name` and `expires` (an ISO 8601 date). A remove record has `op` (`"remove"`) and `name`. Replay applies the records in order; a later record for a name overrides an earlier one.

## Consequences

Files already written must stay readable, so any change to these keys is a change to the file format and needs its own ADR. Records with an unknown `op` are ignored on replay. Adding a new kind of record touches `model.py` and `store.py` (see ADR 0005).
