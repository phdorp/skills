# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive
crashes (R-1, QG-1) and the tool must work offline everywhere with only Python (R-2, QG-2), so
the storage design and the dependency rule are decided centrally. The eBird export is an external
format and is decided centrally too (R-4, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine, on-disk format of the sighting store, and its crash-safety mechanism (R-1);
- the eBird CSV export format and any other import or export format (R-4);
- interfaces between building blocks (CLI, store, export) and the dependency rule between them;
- versioning of the store format and of the CLI commands;
- crosscutting conventions: timestamps and time zone, error handling, exit codes;
- third-party dependencies: the Python standard library only (R-2).

Left to the building blocks (no ADR):

- internal helper functions and structure inside one block;
- argument parsing details inside the CLI block;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. Nothing in the
storage, dependency or export area is built before that.
