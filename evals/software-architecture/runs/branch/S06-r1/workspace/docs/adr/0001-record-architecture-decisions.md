# 1. Record architecture decisions

## Status

proposed

## Context

Sightings must survive crashes (R-1, QG-1) and work everywhere with only Python (R-3, QG-4). Exported files must be accepted by eBird (R-4, QG-3), and logging and listing must be fast (R-5, goal open).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format (serves R-1; not yet chosen, own ADR);
- import/export format: eBird CSV (R-4), including which eBird checklist fields are captured (open);
- interfaces between building blocks (CLI, core logic, storage) and the dependency rule between them;
- versioning of the CLI and of the stored data format;
- crosscutting conventions: time zone and units for sighting times (open), error handling and exit codes, logging;
- third-party dependencies: none beyond the Python standard library (R-3).

Left to the building blocks (no ADR):

- internal helpers, module layout inside one block, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. In particular, no storage or export code is written until the storage and export decisions are accepted. This ADR stays `proposed` until the architect approves its text.
