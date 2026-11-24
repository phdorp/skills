# 3. Command interface and date syntax

## Status

proposed

## Context

*As found, unconfirmed.* Found in `pantry/cli.py` and `pantry/dates.py`. Serves R-2.

## Decision

We will provide the commands `add NAME EXPIRES`, `list [--soon DAYS]` and `remove NAME`. We will
accept dates as an ISO date, `today`, `tomorrow`, `+Nd` or `+Nw`. Exit code 0 means success, 1 a
user error, and 2 bad command-line usage.

## Consequences

Renaming a command, changing the date syntax, or changing an exit code is a change users see,
and needs a new ADR.
