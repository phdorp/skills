# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive crashes (R-2, QG-1) and work everywhere with only Python (R-3, QG-2), and the export must match eBird's format (R-4, QG-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format, including the crash-safety mechanism (R-2);
- eBird CSV export: column layout and the mapping from a sighting (R-4);
- CLI interface: commands, options and output format, and how they are versioned (R-1);
- versioning of the on-disk data format, with a migration rule;
- third-party dependencies: none beyond the Python standard library (R-3);
- crosscutting conventions: time and time zone (local time stored with its UTC offset), error handling and exit codes, logging.

Left to the building blocks (no ADR):

- module layout inside a block, internal helpers, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
