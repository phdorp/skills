# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Storage must survive
crashes (R-2, QG-2) and the tool must run with only the Python standard library (R-3), and new
commands must stay within `cli.py` and at most one new module (R-4, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage: the pantry file format (one JSON record per line, `add` and `remove` operations) and
  the crash-safe write strategy.
- Dependency rule: `cli` may use `dates`, `store` and `model`; `store` may use `model`; no other
  edges between modules.
- Third-party dependencies: none; standard library only.
- CLI interface: command names, argument forms, exit codes (0 success, 1 user error, 2 bad usage),
  and error messages on stderr.

Left to the building blocks (no ADR):

- Helpers inside a module, the structure inside one block, test layout, internal names.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
