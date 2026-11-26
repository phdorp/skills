# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive crashes (R-2, QG-1), work everywhere with only Python (R-3, QG-2), and export to eBird CSV (R-4, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format (R-2, R-3, R-5)
- export format: eBird CSV and its column set (R-4)
- dependency rule: standard library only at runtime (R-3)
- versioning of the sightings store's format
- crosscutting conventions: time storage and time zones, error handling, the unit of count
- minimum Python version (R-3)

Left to the building blocks (no ADR):

- argument parsing details, internal helpers, test layout

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
