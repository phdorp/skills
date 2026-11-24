# 2. Append-only JSON-lines event log

## Status

proposed

## Context

*As found, unconfirmed.* Found in `pantry/store.py` and `pantry/model.py`: the pantry file is
only ever appended to, one JSON object per line, and the current items are replayed from it on
every read. Serves R-1 (QG-1): a write never rewrites existing data.

## Decision

We will keep the pantry as an append-only file of `add` and `remove` records, one JSON object
per line, and replay it to get the current items.

## Consequences

Removing an item appends a record and does not rewrite the file, so the file grows with use.
The torn-write and unreadable-line risks in arc42 section 11 are fixed inside this format or by
replacing it, and a replacement needs its own ADR.
