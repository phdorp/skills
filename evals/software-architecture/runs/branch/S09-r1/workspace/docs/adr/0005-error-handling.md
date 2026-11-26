# 5. Error handling convention

## Status

proposed

## Context

Found in the code, not decided by anyone yet: `pantry/cli.py` (messages and exit codes) and `pantry/store.py` (lines that do not parse). It is a decision on the list in ADR 0001 (crosscutting conventions: error handling). It serves the reliability requirement (R-2, QG-1).

## Decision

We will print user errors to stderr and exit 1: an input that is not a date, and a `remove` of an item that does not exist. Bad command-line usage exits 2 through argparse. A stored line that does not parse as JSON is skipped without a message.

## Consequences

Callers can tell user errors (1) from usage errors (2). The silent skip of unparsable lines hides corruption anywhere in the file, not only a crash at its end (arc42 section 11). A stored record that parses as JSON but has the wrong shape is not handled: it raises an exception in every command. Changing the convention needs a superseding ADR.
