# 3. CLI commands, arguments and exit codes

## Status

proposed

## Context

Found in the code (`pantry/cli.py`), not decided by the architect. The command names, arguments and exit codes are the user-facing contract (R-2), and error handling is a crosscutting convention on the list of decisions made centrally (ADR-0001).

## Decision

As found: the commands are `add NAME EXPIRES`, `list [--soon DAYS]` and `remove NAME`. Exit code 0 means success; 1 means a user error (a date that does not parse, or removing an item that does not exist), with a message `pantry: <message>` on stderr; 2 means bad usage, with argparse's message.

## Consequences

Changing a command name, an argument or an exit code changes what users and scripts see. Adding a command follows ADR-0005.
