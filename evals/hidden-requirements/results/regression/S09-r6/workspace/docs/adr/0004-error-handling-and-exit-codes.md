# 4. Error handling and exit codes

## Status

proposed

## Context

Found in the code, not decided by the architect: `pantry/cli.py` exits 0 on success, 1 on a user error (a date that does not parse, or removing an item that is not there), and 2 on bad usage (argparse), and prints each error as one line to stderr. This is a crosscutting convention under ADR-0001 and serves R-1 (QG-2).

## Decision

We exit 0 on success, 1 on a user error, and 2 on bad usage. Error messages go to stderr as one line, prefixed `pantry:`.

## Consequences

Scripts can rely on the exit codes. Changing a code or message format changes the CLI interface and needs its own ADR.
