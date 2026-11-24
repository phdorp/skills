# 4. CLI commands and exit codes

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/cli.py` (`main`) and the module docstring. This decision is on the accepted list in ADR 0001 (CLI interface). It serves R-1, the command-line use of adding and listing items.

## Decision

We will provide `add NAME EXPIRES`, `list [--soon DAYS]` and `remove NAME`. We will exit 0 on success, 1 on a user error (such as an unparseable date or an unknown item), and 2 on bad usage. User errors are printed to stderr as `pantry: <message>`.

## Consequences

Renaming a command or changing an exit code is a change to the interface that other scripts may depend on, and needs its own ADR. Command-level details, such as the sort order of `list`, stay with the building blocks.
