# 1. Record architecture decisions

## Status

accepted 2026-11-24

## Context

The architect decides the architecture; contributors and agents build it. Crash safety (R-2, QG-1),
the standard-library-only rule (R-3) and the one-module rule for new commands (R-4, QG-2) depend on
the decisions below.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- The storage engine and data format: one JSON record per line, append-only, in the file named by
  `PANTRY_FILE` (default `~/.pantry.jsonl`), with `add` and `remove` records.
- The crash rule: how a line cut short by a crash is handled on the next write.
- The CLI as an interface: command names, flags, arguments, exit codes 0 (success), 1 (user error)
  and 2 (bad usage), and error messages on stderr.
- The date input formats the CLI accepts (`YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`, `+Nw`), and the
  meaning of "soon" in days counted from the local date.
- The dependency rule: `cli.py` may use `store` and `dates`; `store` uses `model`; `model` and
  `dates` do no file access.
- Third-party dependencies: none.
- Crosscutting conventions: dates are local calendar dates with no time and no zone.

Left to the building blocks (no ADR):

- The argparse layout inside `cli.py`.
- The parsing details inside `dates.py`.
- The internals of the replay of records.
- The test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
