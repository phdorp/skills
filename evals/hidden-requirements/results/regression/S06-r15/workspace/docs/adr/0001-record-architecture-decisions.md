# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive crashes (R-2, QG-1) and work everywhere with only Python (R-3, QG-2), and exports must match the eBird CSV format (R-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format (R-2, QG-1);
- the eBird CSV export format (R-4);
- interfaces between building blocks (CLI, core logic, storage) and the dependency rule between them;
- versioning of the CLI and of the data file;
- crosscutting conventions: naming, time zones, units of count, error handling;
- third-party dependencies: standard library only (R-3).

Left to the building blocks (no ADR):

- helper functions and module layout inside one block;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
