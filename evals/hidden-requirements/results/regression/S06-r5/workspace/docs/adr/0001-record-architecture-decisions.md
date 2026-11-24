# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive crashes (R-1, QG-1) and work everywhere with only Python (R-3, QG-2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format
- the eBird CSV export format and its column mapping (R-4)
- interfaces between building blocks, and the dependency rule between them
- versioning of the CLI and the on-disk data format
- crosscutting conventions: error handling, time representation, naming
- third-party dependencies: standard library only (R-3)

Left to the building blocks (no ADR):

- argument-parser details
- test layout
- internal helpers and structure inside one block

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The storage work waits for the storage ADR, and the export work waits for the export-format ADR.
