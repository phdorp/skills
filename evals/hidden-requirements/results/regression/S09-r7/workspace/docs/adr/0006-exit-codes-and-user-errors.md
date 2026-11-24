# 6. Exit codes and user-error messages

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/cli.py` exits 0 on success, 1 on a user error (a date
that does not parse, or removing an item that does not exist), and 2 on bad usage. User errors
are printed to stderr with the prefix `pantry:`. It serves R-1 (QG-2 is still open).

## Decision

We will exit 0 on success, 1 on a user error, and 2 on bad usage, and we will print user errors
to stderr prefixed with `pantry:`.

## Consequences

Scripts may rely on these codes. A new command follows the same convention unless its own ADR
changes it.
