# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Pantry items must
survive crashes (R-1, QG-1) and the program must run with only the Python 3.9+ standard library
(R-3, QG-3). New commands must be addable by changing only `cli.py` and at most one new module
(R-4, QG-2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage and on-disk format: an append-only JSON-lines log of add and remove events, one
  record per line, replayed on read. How a write is made durable, including the handling of a
  torn last line, belongs to this decision.
- Command interface: command names, date syntax (ISO date, `today`, `tomorrow`, `+Nd`, `+Nw`),
  and exit codes 0, 1 and 2.
- Dependency rule: `cli` may use `dates`, `store` and `model`; `store` and `model` never import
  `cli`; a new command uses the existing store API.
- Error handling: user errors go to stderr with exit code 1; how unreadable lines in the
  pantry file are reported.
- Third-party dependencies: none. Python 3.9 or later, standard library only.

Left to the building blocks (no ADR):

- Helper names and the argparse layout inside `cli.main`.
- The test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The torn-write
fix depends on the storage decision and waits for its acceptance.
