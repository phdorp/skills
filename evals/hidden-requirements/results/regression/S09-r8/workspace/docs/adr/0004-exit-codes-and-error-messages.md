# 4. Exit codes and error messages

## Status

proposed

## Context

Found in `pantry/cli.py`: the module docstring and the `main` function define the exit codes and the messages. This is an error-handling convention, one of the crosscutting conventions ADR-0001 lists as decided centrally. It serves R-2 (add and list from the command line).

## Decision

We will exit with 0 on success, 1 on a user error (a date that does not parse, an unknown item), and 2 on bad usage (unknown command or arguments). We will print errors to stderr, prefixed with `pantry:`.

## Consequences

Scripts can rely on the exit codes. Any new command follows the same convention. A change to the codes is a change users depend on, so it needs a new ADR.
