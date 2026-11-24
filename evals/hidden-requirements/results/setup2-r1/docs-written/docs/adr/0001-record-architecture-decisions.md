# 0001. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Offline check-outs must survive crashes and sync later (R-4, QG-3), and a successor who knows only Python must be able to change the system (QG-5).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and the format of stored records (items, holders, history);
- the yearly inventory export format (R-6), and any import format added later;
- interfaces between building blocks, and the dependency rule between them;
- versioning of the yearly CSV and the Monday report, which the treasurer and the kit manager depend on;
- crosscutting conventions: naming, dates and time zones, error handling, logging, and what is logged about personal data;
- third-party dependencies: libraries and base images.

Left to the building blocks (no ADR):

- internal helpers, structure inside one block, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. Hosting and language are decided in [ADR-0002](0002-host-on-nas-with-docker-in-python.md), which waits for the architect's approval of its text. The storage engine is decided later, in its own ADR, and must run on the NAS.
