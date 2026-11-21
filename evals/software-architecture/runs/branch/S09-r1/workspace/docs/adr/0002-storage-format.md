# 2. Store pantry items in an append-only JSON-lines file

## Status

proposed

## Context

Found in the code: `pantry/store.py:13-30` appends one JSON record per line and reads all records
back; `pantry/model.py:19-27` replays them into items. Serves R-2 (no item lost on a crash
mid-write) and R-3 (standard library only). The format does not meet R-2 as it stands: a line cut
short by a crash makes the next append unreadable, so an item that reported success is lost. See
arc42 section 11.

## Decision

We will keep pantry items in an append-only file with one JSON record per line, `add` or `remove`,
at `~/.pantry.jsonl` or the path in `PANTRY_FILE`. We will rebuild the items by replaying the
records in order, and fsync each append.

## Consequences

Whether this format can meet R-2 is the open storage decision; the fix waits for it. Any change
to the record shape or the file location is a change to this ADR's decision and to the data
files users already have.
