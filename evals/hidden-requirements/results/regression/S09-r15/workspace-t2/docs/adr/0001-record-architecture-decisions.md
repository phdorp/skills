# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Items must survive a crash mid-write (R-1, QG-1) and a new command must stay within cli.py and at most one new module (R-3, QG-3), and the program must run with only the Python standard library (section 2 of `docs/architecture/arc42.md`).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage engine and on-disk format of the pantry file (today: append-only JSON lines, replayed on read).
- The rule for making a change durable on disk (R-1).
- Interfaces between building blocks, and the dependency rule between them (R-3).
- Versioning of what users depend on: the commands and their flags, the `PANTRY_FILE` variable, and the file format.
- Crosscutting conventions: error handling (exit codes 0 for success, 1 for a user error, 2 for bad usage, messages on stderr) and the date input grammar.
- Third-party dependencies: none. The program uses only the Python standard library; any exception needs its own ADR.

Left to the building blocks (no ADR):

- Argparse structure inside cli.py, list sort order, message wording beyond the conventions above, internal helpers, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
