# 3. Write rule: append, flush and fsync; skip damaged lines on read

## Status

proposed

## Context

*As found, unconfirmed.* Found in `pantry/store.py`, in `_append` and `_records`. Serves R-2 (QG-1): each record is durable before the command returns.

## Decision

We will write each record by appending one line to the pantry file, then flushing and fsyncing it. On read, a line that does not parse as JSON is skipped.

## Consequences

A torn last line is skipped on read, but the next append is written onto that same line, so the next record is lost too. This was reproduced in the session; see arc42 section 11. The rule does not yet meet R-2 after a crash. Changing it is a new ADR that replaces this one.
