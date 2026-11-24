# 0001. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive crashes (R-2) and work everywhere with only Python (R-3, QG-1), and the export must match eBird's format (R-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format (R-2);
- import and export format: the eBird CSV (R-4);
- interfaces between building blocks, and the dependency rule between them;
- versioning of the data file and of the CLI;
- crosscutting conventions: time zone and units for sighting time, error handling;
- third-party dependencies: none beyond the standard library (R-3).

Left to the building blocks (no ADR):

- internal helpers, structure inside one block, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
