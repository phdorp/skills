# 5. CLI commands and exit codes

## Status

proposed

## Context

Found in the code, not decided: `pantry/cli.py` (`main`). Serves R-1 (QG-4); users and scripts depend on these commands.

## Decision

We will provide `add NAME EXPIRES`, `list [--soon DAYS]` and `remove NAME`. We will exit 0 on success, 1 on a user error, and 2 on bad usage.

## Consequences

Changing a command, flag or exit code changes what users and scripts see, so it needs a new ADR. Date input is governed by ADR 0004.

Question for the architect: keep these commands and exit codes?
