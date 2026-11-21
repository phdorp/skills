# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Sightings must survive a crash mid-write (R-2, QG-1, QS-1) and the product must work offline with only Python installed (R-3, QG-2, QS-2), so the storage and the dependency rule are decided centrally.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage engine and on-disk data format (serves R-2, QG-1). The choice itself is not yet made and gets its own ADR.
- Export format: the mapping from sightings to eBird CSV columns (serves R-4).
- Interfaces between building blocks and the dependency rule: standard library only (serves R-3, QG-2).
- Versioning of the CLI commands and the stored file format.
- Crosscutting conventions: how time and time zones are stored, and error handling.
- Third-party dependencies: none.

Left to the building blocks (no ADR):

- Internal helpers, structure inside one block, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The storage engine choice waits for its own ADR; the export mapping waits for the export format decision. No code for storage or export is written before then.
