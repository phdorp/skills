# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive
crashes (R-2, QG-1), work offline with only Python (R-3, QG-2) and export to eBird (R-4, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format;
- export format: the eBird CSV layout and its version (R-4);
- interfaces between the CLI, storage and export blocks, and the dependency rule between them;
- versioning of the CLI and of the data format;
- crosscutting conventions: naming, time (local time with UTC offset), error handling, logging;
- third-party dependencies (none, per R-3).

Left to the building blocks (no ADR):

- internal helpers, structure inside one block, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
