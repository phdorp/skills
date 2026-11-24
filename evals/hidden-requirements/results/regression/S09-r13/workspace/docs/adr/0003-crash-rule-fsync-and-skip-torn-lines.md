# 3. Crash rule: fsync each record, skip torn lines on read

## Status

proposed

## Context

Found in the code: `pantry/store.py`. `_append` writes one record, flushes and fsyncs it.
`_records` skips any line that does not parse, commented as "a line cut short by a crash". It
serves R-2 (QG-1). This is the crash-rule item on ADR 0001's list.

## Decision

Each record is written with one append, followed by a flush and an fsync. On read, a line that is
not valid JSON is skipped without a warning. Nothing repairs or truncates the file on write: the
next append goes after the last line as it is.

## Consequences

A crash during a write loses at most the record being written, and the store still opens. But
because nothing ends a torn line before the next append, the next record is written onto the torn
line and is lost too. This was reproduced: after a crash, a later `add` made the earlier item
disappear. As written, this decision does not meet R-2. A fix changes this decision, so it needs a
new ADR that supersedes this one; work on the fix waits for that ADR.
