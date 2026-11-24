# 1. Record architecture decisions

## Status

accepted 2026-11-24

## Context

The architect decides the architecture; contributors and agents build it. Kit Tracker needs offline check-out that syncs (R-3, QG-3) and an export the treasurer can audit (R-6, QG-4), and it must be maintainable by a Python-only successor (R-7, QG-5).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage engine and data format for items and check-out history.
- Sync protocol and local data format on the phone (offline check-out, R-3).
- CSV export format and its versioning (R-6).
- Interfaces between building blocks, and the dependency rule between them.
- Crosscutting conventions: naming, units, error handling, logging, and handling of coach personal data.
- Third-party dependencies, which must fit a Python-only maintainer (R-7).

Left to the building blocks (no ADR):

- Internal helpers, structure inside one block, screen layout, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
