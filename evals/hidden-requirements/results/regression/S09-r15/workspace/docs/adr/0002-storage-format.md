# 2. Storage format: append-only JSON lines

## Status

proposed

## Context

Items must survive a crash mid-write (R-1, QG-1), and the storage engine and on-disk format are decided centrally (ADR 0001). Found in `pantry/store.py` and `pantry/model.py`.

## Decision

The pantry is a text file with one JSON object per line, at `PANTRY_FILE` or `~/.pantry.jsonl`. There are two record kinds: `{"op": "add", "name": ..., "expires": "YYYY-MM-DD"}` and `{"op": "remove", "name": ...}`. The current pantry is the result of replaying the records in order (`model.replay`), and a name appears at most once in it. Records carry no version field.

## Consequences

A new record kind, or a change to the format, touches `model.py` and `store.py`, which bears on R-3 (QG-3). Work that changes the format waits for a new ADR that supersedes this one.
