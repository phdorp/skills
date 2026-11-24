# 0001. Record architecture decisions

## Status

accepted 2026-11-23

## Context

The architect decides the architecture; contributors and agents build it. Check-out records must be correct and attributable to a named coach (R-1, QG-1, QG-2), and checking out must take at most 3 taps and under 15 seconds (R-2, QG-3), so decisions that shape records and the coach-facing interface need a recorded owner.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk or wire data formats;
- import and export formats;
- interfaces between building blocks, and the dependency rule between them;
- versioning of anything other systems or users depend on (APIs, file formats, CLI);
- crosscutting conventions: naming, units, error handling, logging;
- third-party dependencies (framework, hosting, sign-in).

Left to the building blocks (no ADR):

- internal helpers, structure inside one block, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
