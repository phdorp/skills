# 2. Append-only JSON-lines store

## Status

proposed

## Context

Found in the code, not decided by the architect: `pantry/store.py` (`_append`, `_records`) and
`pantry/model.py` (`to_record`, `removal`, `replay`). It serves R-1 (items persist between
commands) and R-2 (QG-1: the file is never rewritten, only appended to). It also meets R-3: no
database library.

## Decision

Items are kept in one file, one JSON record per line, appended and never rewritten. Records are
`{"op": "add", "name", "expires"}` (expires as `YYYY-MM-DD`) and `{"op": "remove", "name"}`. The
current items are the result of replaying the records in order. The file is `PANTRY_FILE` or
`~/.pantry.jsonl`.

## Consequences

Easy: no database and no lock service; an append does not touch earlier records. Hard: the file
grows with every add and remove, nothing compacts it, and every command reads all of it. A new
kind of record changes `model.replay` (see ADR 0006 and the risks in arc42 section 11).
