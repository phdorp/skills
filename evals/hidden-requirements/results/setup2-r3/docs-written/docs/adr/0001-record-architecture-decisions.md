# 1. Record architecture decisions

## Status

accepted 2026-11-23

## Context

The architect decides the architecture; contributors and agents build it. Check-out must take at
most 3 taps and under 15 seconds (R-3, QG-2), and it must work without signal and sync later
(R-4, QG-3). Personal data stays on the club's NAS (arc42 section 2), so every decision that
moves data off the NAS needs an ADR.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format of the kit records on the NAS;
- the CSV export format for the treasurer (R-8), including its columns and how they change over time;
- the sync format between the phone and the NAS (R-4);
- interfaces between building blocks, and the dependency rule between them;
- crosscutting conventions: naming, units (dates, times and time zone), error handling, logging;
- third-party dependencies, including the mail library and the container base image.

Left to the building blocks (no ADR):

- internal helpers and the structure inside one block;
- screen layout;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
