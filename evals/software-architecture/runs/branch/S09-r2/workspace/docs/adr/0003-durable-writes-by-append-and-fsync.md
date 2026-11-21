# 3. Durable writes by append and fsync

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/store.py` (`_append`, `_records`). Serves R-2 (QG-2). Each record is written with one `write` in append mode, followed by `flush` and `os.fsync` on the file. Reads skip lines that do not parse. The torn-line defect is recorded in arc42 section 11 and is not decided here.

## Decision

We will make each write durable by appending one record and calling fsync on the file before the command reports success.

## Consequences

An acknowledged record is on disk when the command exits 0. A crash mid-write can still leave a partial line, and the next append lands on it (arc42 section 11). Any fix to that defect changes this decision, and the change needs a new ADR.

Question for the architect: keep append plus fsync as the write-durability decision, given the open defect?
