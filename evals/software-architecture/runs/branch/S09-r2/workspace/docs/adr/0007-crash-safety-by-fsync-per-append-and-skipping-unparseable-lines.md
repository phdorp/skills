# 7. Crash safety: fsync per append, skipping unparseable lines

## Status

proposed

## Context

Found in the code, not decided: `pantry/store.py` (`_append` flushes and fsyncs each record; `_records` skips lines that do not parse). Serves R-2 (QG-1).

## Decision

We will fsync each appended record before the command returns, and skip any line that does not parse when the file is read.

## Consequences

An add that returned survives a crash after it returned. Skipping hides corrupt lines, as ADR 0001 records. It does not handle a partial line followed by a new append (arc42 section 11, risk 1), and the directory is not fsynced (risk 4).

Question for the architect: keep this crash-safety approach, or change it in a new ADR?
