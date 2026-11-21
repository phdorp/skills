# 2. Pantry file format: append-only JSONL log

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/store.py` and `pantry/model.py`. Serves R-2 (QG-2) and R-1 (QG-1). Each line of the file is one JSON record, `{"op": "add", "name", "expires"}` or `{"op": "remove", "name"}`. The file is at `PANTRY_FILE`, or `~/.pantry.jsonl` by default.

## Decision

We will store the pantry as an append-only JSONL log of add and remove records. Items are derived by replaying the records in order: the last add for a name wins, and a remove deletes that name.

## Consequences

Writes never rewrite existing data, which supports R-2. Every command reads the whole file, so reads get slower as it grows. Changing the record shape is a format change for existing files.

Question for the architect: keep the append-only log as the storage format?
