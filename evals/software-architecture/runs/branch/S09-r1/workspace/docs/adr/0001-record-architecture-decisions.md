# 1. Record architecture decisions

## Status

accepted 2026-11-21

## Context

The architect decides the architecture; contributors and agents build it. Pantry's items must
survive a crash mid-write (R-2), the program must run with only the Python standard library
(R-3), and a new command must stay within cli.py and at most one new module (R-4, QG-1).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage format: the append-only JSON-lines file of add and remove records, at `~/.pantry.jsonl`
  or the path in `PANTRY_FILE`.
- Dependency rule: `cli` uses `store` and `dates`; `store` uses `model`; no other edges.
- Interfaces between blocks: the `store` functions `add`, `remove` and `items`, and the `Item`
  record.
- Versioning of the CLI: its subcommands and exit codes (0 success, 1 user error, 2 bad usage);
  and of the file format.
- Crosscutting conventions: user errors go to stderr with exit code 1; dates are stored as
  ISO 8601.
- Third-party dependencies: none (R-3).

Left to the building blocks (no ADR):

- argparse details, internal helpers, and the test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The fix for R-2
depends on the storage decision above, so it waits for this ADR and for the storage decision
it covers.
