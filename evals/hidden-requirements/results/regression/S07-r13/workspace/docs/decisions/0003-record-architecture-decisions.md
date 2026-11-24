# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Shelf must keep the
catalog intact across crashes (R-2, QG-1) and run with only the Python standard library (R-3,
QG-4), so the storage format, the ISBN rule and the command interface are decided centrally.

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the catalog's storage format and its write rule (ADR 0001);
- the ISBN rule: check digits locally, before a book is stored (ADR 0002);
- the interface between `cli` and `catalog`, and how a command plugs into `cli` (R-5);
- the CLI's command names, flags and output format, which readers and scripts depend on;
- error handling: messages to stderr and exit codes;
- third-party dependencies: none (R-3).

Left to the building blocks (no ADR):

- helpers inside `isbn.py` and `catalog.py`;
- argument parsing below the interface;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. This ADR changes
neither ADR 0001 nor ADR 0002; both stay accepted.
