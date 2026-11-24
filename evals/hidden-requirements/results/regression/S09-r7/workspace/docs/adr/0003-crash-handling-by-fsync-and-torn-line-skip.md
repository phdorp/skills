# 3. Crash handling by fsync per record and skipping a torn last line

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/store.py` flushes and fsyncs after each appended
record, and on read skips any line that does not parse as JSON, as a line cut short by a
crash. This serves R-2; its crash goal (QG-1) is still open and named here in words.

## Decision

We will fsync each record as it is appended, and we will skip an unparsable line when reading
the pantry file.

## Consequences

The code does not yet meet R-2: after a torn last line, the next append joins that line, and
the new item is then skipped on read. Reproduced; recorded as a risk in arc42 section 11. A
decision that fixes this is a superseding ADR, which this one stays until it is accepted.
