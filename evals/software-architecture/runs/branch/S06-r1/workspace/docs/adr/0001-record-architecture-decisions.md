# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must
survive crashes (R-2, QG-1) and work everywhere with only Python installed (R-3, QG-3), so
the storage format and the dependency rule are decided centrally, while exports must match
eBird's format (R-4, QG-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk format (R-2, R-5);
- import and export format: eBird CSV (R-4);
- third-party dependencies: standard library only (R-3);
- CLI interface and versioning: command names, flags, output format (R-1, R-6);
- crosscutting conventions: time zone and time format, error handling.

Left to the building blocks (no ADR):

- internal module structure inside one block;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
