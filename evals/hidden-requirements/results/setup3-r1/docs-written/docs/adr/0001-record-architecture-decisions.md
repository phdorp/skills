# 0001. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Kit data must sync from
phones without signal (R-7, QG-3), keep two years of history (R-6), export as CSV (R-5), run on
the club's NAS with no paid service (C-1, C-2), and stay maintainable by a Python-only successor
(R-8, QG-5).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format, including check-out and lost-item records (R-6, QG-3);
- offline sync: the data exchanged between phone and NAS, and the conflict rule (R-7, QG-3);
- the CSV export format and its versioning (R-5);
- the QR code payload printed on each bag (R-3);
- interfaces between building blocks, and the dependency rule between them;
- third-party dependencies, including Python packages and the Docker base image (C-1, C-5);
- crosscutting conventions: naming, units, error handling, logging.

Left to the building blocks (no ADR):

- internal helpers and the structure inside one block;
- screen layout, within the 3-tap limit of R-3;
- test layout and tooling inside one block.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
