# 5. The command-line interface

## Status

proposed

## Context

Found in the code, not decided: `pantry/cli.py` and its docstring. It serves R-1 (QG-1, QS-1),
the commands the user types, and the exit codes are part of the interface.

## Decision

We will provide the commands `add NAME DATE`, `list [--soon DAYS]` and `remove NAME`. Exit code
0 is success, 1 a user error, 2 bad usage. A user error prints `pantry: <message>` to stderr.
Dates accept `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd` and `+Nw`.

## Consequences

Changing a command name, an exit code or an accepted date form changes an interface users
depend on, so it is a versioning decision on the ADR 0001 list. Errors and exit codes apply to
every command.
