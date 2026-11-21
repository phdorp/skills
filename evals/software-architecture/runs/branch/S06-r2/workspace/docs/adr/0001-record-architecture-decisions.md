# 1. Record architecture decisions

## Status

proposed

## Context

Sightings must survive crashes (R-2, QG-1) and work everywhere with only Python (R-3, QG-2), and the export must match eBird's CSV format (R-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format for sightings (decides the crash behaviour in R-2);
- export format: the eBird CSV columns and how each sighting field maps onto them (R-4);
- versioning of the CLI commands and of the on-disk format;
- crosscutting conventions: how sighting time is represented (time zone), the units of count, and error handling;
- third-party dependencies: the standard library only (R-3);
- interfaces between building blocks and the dependency rule between them (the blocks are decided later, in arc42 section 5).

Left to the building blocks (no ADR):

- internal helpers and code structure inside one block;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The storage ADR depends on R-2 and QG-1; the performance requirement R-5 has no measure yet, so no decision on it is recorded here.
