# 1. Record architecture decisions

## Status

proposed

## Context

Sightings must survive crashes (R-2, QG-1) and work everywhere with only Python, offline (R-3,
QG-2). The architect decides the architecture; contributors and agents build it.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format (R-2, R-3);
- import and export formats: the eBird CSV layout (R-4);
- interfaces between the CLI, storage and export blocks, and the dependency rule between them;
- versioning of the CLI and of the data file format;
- crosscutting conventions: time zones for sightings, error handling and exit codes;
- third-party dependencies: none, standard library only (R-3).

Left to the building blocks (no ADR):

- internal helpers, module layout inside a block, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The storage
engine and data format ADR comes next, after this one is accepted, and gates the write path for
R-2 and the performance goal for R-5.
