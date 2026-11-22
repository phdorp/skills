# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must
survive crashes (R-1, QG-1) and work everywhere with only Python (R-3, QG-2), and must export
to eBird's format (R-4, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format;
- import and export formats (eBird CSV);
- interfaces between the command-line front end, the storage and the export code, and the
  dependency rule between them;
- versioning of the CLI command names and of the store's format;
- crosscutting conventions: time and time-zone representation, counts, error handling and exit
  codes, and how species names are matched to eBird's names;
- third-party dependencies (none: standard library only, per R-3).

Left to the building blocks (no ADR):

- internal helpers and the structure inside one block;
- argument parsing details and output formatting of `birdlog list`;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The storage
engine and the eBird column mapping are not decided here; each gets its own ADR once the
architect accepts this list.
