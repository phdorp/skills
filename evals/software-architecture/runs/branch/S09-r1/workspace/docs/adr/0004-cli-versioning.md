# 4. CLI command and date-form contract

## Status

proposed

## Context

Found in the code, not decided by anyone yet: `pantry/cli.py` (commands, flags, exit codes) and `pantry/dates.py` (date forms). It is a decision on the list in ADR 0001 (versioning of what users depend on). It serves the command-line requirement (R-1, QG-2).

## Decision

We will keep the command-line contract: `add NAME EXPIRES`, `list [--soon DAYS]` and `remove NAME`. `EXPIRES` takes an ISO date, `today`, `tomorrow`, `+Nd` or `+Nw`. Exit codes are 0 on success, 1 on a user error and 2 on bad usage.

## Consequences

Scripts and users depend on these names and codes, so a change to any of them needs a superseding ADR. Adding a new form of date input is a change to this contract as well.
