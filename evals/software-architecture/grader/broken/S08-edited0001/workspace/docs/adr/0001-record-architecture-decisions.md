# 1. Record architecture decisions

## Status

accepted 2026-10-01

## Context

The architect decides the architecture; modellers implement it. We need a line between
decisions the architect makes centrally and decisions left to whoever builds a block (R-2,
QG-2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the connector definitions in `Interfaces` and their units;
- the dependency rule between blocks: `System` → `Room`, `Thermostat` → `Interfaces`; blocks
  do not depend on each other;
- library dependencies;
- the heat-capacity connector.

Left to the building blocks (no ADR): equations inside a block, parameter defaults, test
scripts.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
