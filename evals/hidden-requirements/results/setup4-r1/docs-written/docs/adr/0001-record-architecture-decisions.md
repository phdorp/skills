# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Offline checkouts (R-4, QG-3) pull against keeping as little personal data on the phone (R-5, QG-4), and the Monday report (R-6) must keep data on the club's own hardware (arc42 section 2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage engine and on-disk data format for kit and coach records on the NAS, including what the phone keeps offline (R-4, R-5).
- Sync between phone and NAS: wire format and conflict rules (R-4).
- Yearly inventory export: CSV columns, encoding and versioning, read by the treasurer (R-1).
- Monday report: the channel it leaves the NAS by, with no third-party cloud, and what it contains, with no coach phone numbers (R-6).
- Interfaces between building blocks, and the dependency rule between them.
- Crosscutting conventions: naming, dates and units, error handling, logging.
- Third-party dependencies: framework, hosting product on the NAS, and any mail library (R-6, R-8). The language, Python, is a constraint from arc42 section 2.

Left to the building blocks (no ADR):

- Internal helpers, the structure inside one block, screen layout, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
