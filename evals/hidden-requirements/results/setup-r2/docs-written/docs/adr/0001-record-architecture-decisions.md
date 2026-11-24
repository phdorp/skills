# 1. Record architecture decisions

## Status

accepted 2026-11-23

## Context

The architect decides the architecture; contributors and agents build it. Check-out records
must be correct and name the coach (R-2, QG-3), work on the sideline in at most 3 taps and
under 15 seconds (R-3, QG-1, QG-2), work without a mobile signal and sync later (R-5), and be
exportable as a yearly CSV inventory for the insurance audit (R-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and record format for kit items and check-out records, including what is
  kept offline on the phone;
- export format: the CSV of the yearly kit inventory (R-4);
- interfaces between building blocks, and the dependency rule between them;
- versioning of the record format and the CSV export once other tools read them;
- crosscutting conventions: naming, units (dates and times), error handling, logging;
- third-party dependencies.

Left to the building blocks (no ADR):

- internal helpers, structure inside one block, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
