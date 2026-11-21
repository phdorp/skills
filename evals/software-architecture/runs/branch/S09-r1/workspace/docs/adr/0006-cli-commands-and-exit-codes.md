# 0006. Command-line interface and exit codes

## Status

proposed

## Context

Found in `pantry/cli.py`. Serves R-1 (add items and list what expires soon, from the command
line) and QG-2.

## Decision

We will provide three commands: `add NAME EXPIRES`, `list [--soon DAYS]` and `remove NAME`.
Exit codes are 0 on success, 1 on a user error (a date that does not parse, or removing an
unknown name), and 2 on bad usage. `list` prints one line per item: `YYYY-MM-DD  NAME`, sorted
by expiry and then by name, case-insensitively.

## Consequences

Scripts can rely on the exit codes and the line format. The code has no versioning mechanism for
the CLI. ADR-0001 says changes to these are versioned and need an ADR; whether that applies to
existing behaviour is the architect's decision.
