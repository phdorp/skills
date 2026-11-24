# 1. Record architecture decisions

## Status

accepted 2026-11-23

## Context

The architect decides the architecture; contributors and agents build it. Check-outs must work offline and must never be lost (R-3, R-5, QG-3), volunteers must use the tool without training (R-2, QG-2), and coach names and phone numbers must not leave club hardware or be stored on a phone (R-4, QG-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the storage engine and the data format of the check-out records, including what is kept on the phone;
- the interfaces between the building blocks (phone app, NAS service, reports), and the dependency rule between them;
- crosscutting conventions: naming, dates and times, error handling, and the German interface texts;
- third-party dependencies, including the mail sender and the Python packages.

Left to the building blocks (no ADR):

- internal helpers, the structure inside one block, and the test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
