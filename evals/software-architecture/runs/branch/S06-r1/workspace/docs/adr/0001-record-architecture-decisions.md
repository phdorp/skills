# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive crashes (R-2, QG-1) and work everywhere with only Python (R-3, QG-2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format (R-2, R-5);
- import and export formats: the eBird CSV export (R-4);
- interfaces between the CLI and the storage, and the dependency rule between them;
- versioning of the CLI and of the on-disk format;
- crosscutting conventions: timestamps and time zones, counts, error handling;
- third-party dependencies: the standard library only, per R-3.

Left to the building blocks (no ADR):

- internal helpers, the argument-parsing structure within the CLI, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
