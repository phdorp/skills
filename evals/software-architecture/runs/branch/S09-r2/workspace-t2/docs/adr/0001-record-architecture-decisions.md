# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Items must survive crashes (R-1, QG-1) and the product must run with only Python's standard library (R-3, QG-2), while a new command stays confined to `cli.py` and at most one new module (R-4, QG-3). The command surface (R-2) is part of the user-facing contract.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the pantry file's data format (JSON lines, append-only, replayed on read) and its crash-safety rule: a record is durable once its command returns;
- the CLI command names, arguments and exit codes (`add`, `list --soon`, `remove`; 0 success, 1 user error, 2 bad usage);
- the dependency rule: only the Python standard library;
- the dependency rule between `cli`, `store`, `model` and `dates`, and that a new command touches only `cli.py` and at most one new module.

Left to the building blocks (no ADR):

- internal helper names and module internals;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. Current code does not yet meet R-1: a record cut short by a crash is followed by the next record on the same line, which loses that next record. That fix is work that waits for this ADR's approval, and the list of known risks is recorded in arc42 section 11 once the architecture is recovered.
