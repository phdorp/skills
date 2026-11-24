# 1. Record architecture decisions

## Status

accepted 2026-11-23

## Context

The architect decides the architecture; contributors and agents build it. Coaches must check kit out
and back in without training, within three taps and under 15 seconds, and the club must always know
who holds each item (R-1, R-2, R-3, QG-1, QG-2), while all data stays on the club's Synology NAS with
no paid services and the code stays Python (arc42 section 2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format for the holder, location and history records;
- import and export formats, starting with the yearly CSV inventory export for the treasurer;
- interfaces between building blocks, and the dependency rule between them;
- third-party dependencies, the runtime (Docker on the Synology NAS), and the implementation language (Python);
- crosscutting conventions: naming, dates and time zones, error handling.

Left to the building blocks (no ADR):

- internal helpers, structure inside one block, UI layout, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
