# 4. Command-line interface: commands, arguments, exit codes

## Status

proposed

## Context

*As found, unconfirmed.* Found in `pantry/cli.py`. Serves R-1 (QG-4): the add and list commands. Serves R-4 (QG-3): commands are entries in one dispatch in `cli.py`.

## Decision

We will provide three commands: `add NAME EXPIRES`, `list [--soon DAYS]`, and `remove NAME`. Exit code 0 means success, 1 a user error (an unparseable date, an unknown item), and 2 bad usage. `list` prints one line per item, `YYYY-MM-DD  name`, sorted by expiry date and then by lower-cased name.

## Consequences

Scripts that call the CLI depend on these names, arguments and exit codes, so changing them is a versioned change. A new command is added as one branch in `cli.py` and, if it needs its own logic, one new module.
