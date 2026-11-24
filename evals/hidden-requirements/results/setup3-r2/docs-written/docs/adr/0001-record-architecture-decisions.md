# 0001. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Kit records must work offline at the pitch and sync later (R-4, QG-4), coaches must check out in three taps with no training (R-3, QS-1), and only the kit manager may change records (R-6, QG-5). The yearly CSV export for the insurance audit (R-7) and a successor who knows Python only (R-8) constrain data and interfaces.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage: where records live, the check-out data format, and the phone-to-NAS sync protocol and conflict rules (R-4, R-2);
- import and export formats, including the yearly CSV export for the treasurer (R-7);
- interfaces between building blocks, and the dependency rule between them;
- crosscutting conventions: item identifiers and naming, units (counts), error handling, logging;
- third-party dependencies and hosting: the club's Synology NAS in Docker, and the club's existing mail account for the Monday report (R-5).

Left to the building blocks (no ADR):

- internal helpers, structure inside one block, test layout, screen layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
