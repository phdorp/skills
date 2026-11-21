# 0001. Record architecture decisions

## Status

proposed

## Context

Sightings must survive crashes (R-2, QG-1) and work everywhere with only Python (R-3, QG-2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format;
- the eBird CSV export format and the internal format it maps from;
- interfaces between the CLI, core and storage blocks, and the dependency rule between them;
- versioning of the CLI and of the data file;
- crosscutting conventions: timestamps and time zones, species naming, error handling, logging;
- third-party dependencies (standard library only, from R-3).

Left to the building blocks (no ADR):

- argument parsing details, output formatting, internal helpers, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
