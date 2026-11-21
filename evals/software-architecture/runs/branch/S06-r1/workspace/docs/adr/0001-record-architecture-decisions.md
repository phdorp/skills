# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive crashes (R-1, QG-1), work offline on Linux, macOS and Windows with only Python installed (R-3, QG-2), and export to the eBird CSV format (R-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format
- import and export formats (eBird CSV)
- interfaces between building blocks, and the dependency rule between them
- versioning of the CLI and of the on-disk format
- crosscutting conventions: time zone and units, error handling, logging
- third-party dependencies: standard library only (R-3)

Left to the building blocks (no ADR):

- internal helpers, structure inside one block, test layout

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
