# 5. CLI interface and exit codes

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/cli.py` (module docstring and `main`). Serves R-1 (QG-1). The commands are `add NAME DATE`, `list [--soon DAYS]` and `remove NAME`. Exit codes: 0 success, 1 user error, 2 bad usage.

## Decision

We will expose the commands `add`, `list` and `remove` through `python3 -m pantry`, with the exit codes 0, 1 and 2 as listed above.

## Consequences

Scripts can depend on these exit codes, so changing them is a versioned change. `remove` also exists in the code, though R-1 does not name it; its place in R-1 is an open question.

Question for the architect: keep `remove` in the CLI interface, and keep the exit codes as they are?
