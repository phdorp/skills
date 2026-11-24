# 0005. The command-line contract: commands, arguments and exit codes

## Status

proposed

## Context

As found in the code, not yet decided by the architect: `pantry/cli.py:10-43` defines `add NAME EXPIRES`, `list [--soon DAYS]` and `remove NAME`. It exits 0 on success, 1 on a user error (an unreadable date, an unknown item), and 2 on bad usage (`pantry/cli.py:23`). User errors go to stderr with the prefix `pantry:`. This serves R-1 (add and list from the command line). It is a central decision under ADR-0001.

## Decision

We keep the commands `add`, `list` and `remove`, with these arguments and exit codes 0, 1 and 2. User-facing errors go to stderr, prefixed `pantry:`. `--help` exits 0.

## Consequences

Scripts may rely on the exit codes. Changing an existing command, argument or exit code needs a new ADR that supersedes this one. Adding a command is a change to this contract and is recorded here when it is made.
