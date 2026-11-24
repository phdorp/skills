# 1. Record architecture decisions

## Status

accepted 2026-11-24

## Context

The architect decides the architecture; contributors and agents build it. Check-out must work with no mobile signal (R-5, QG-3) and be easy to use (R-3, QG-2), and only club members may see the data (R-4, QG-4), so these decisions shape the whole system.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- where check-out and loss records are stored, and their data format (R-5, R-9);
- the export format of the yearly inventory CSV (R-7);
- the interfaces between the screens and the records, and the dependency rule between them (R-5);
- versioning of the record format, once the CSV export depends on it (R-7);
- crosscutting conventions: names of items and coaches, times and time zone, error messages shown to coaches, logging;
- third-party dependencies (R-8).

Hosting (Synology NAS with Docker) and language (Python) are constraints in arc42 section 2, not decisions on this list.

Left to the building blocks (no ADR):

- internal helpers, structure inside one block, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
