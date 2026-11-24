# 4. CLI commands, output and exit codes

## Status

proposed

## Context

Found in the code: `pantry/cli.py` (`main`, argparse subparsers) and `pantry/__main__.py`. It
serves R-1, the command-line requirement. The exit codes are documented in cli.py's docstring.

## Decision

The program runs as `python3 -m pantry` with three commands: `add NAME EXPIRES`,
`list [--soon DAYS]` and `remove NAME`. `list` prints one line per item, `YYYY-MM-DD  NAME`, sorted
by expiry date and then by name ignoring case. Exit codes: 0 on success; 1 on a user error (an
unreadable date, or removing an item that does not exist), with `pantry: <message>` on stderr; 2 on
bad usage, as argparse reports it.

## Consequences

Scripts can rely on the commands, the output line format and the exit codes. Changing any of them
is a change to an interface other programs may depend on, and needs a decision of its own.
