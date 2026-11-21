# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive crashes (R-2, QG-1) and work everywhere with only Python (R-3, QG-2), and exports must be accepted by eBird (R-4, QG-3). Logging must be fast (R-5, performance goal open).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk format, including how a write becomes durable (R-2, R-5)
- eBird CSV export mapping: which sighting field goes to which eBird column (R-4)
- third-party dependencies: standard library only (R-3)
- interfaces between the CLI, log store, export and list blocks, and the dependency rule between them
- versioning of the CLI and of the on-disk format
- crosscutting conventions: timestamp and time-zone format, count as integer, species naming, error handling and exit codes

Left to the building blocks (no ADR):

- internal helpers and the structure inside one block
- parsing internals
- test layout

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
