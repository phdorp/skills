# 0001. Record architecture decisions

## Status

accepted 2026-11-24

## Context

The architect decides the architecture; contributors and agents build it. A simulation must give the room temperature (R-1), a block must be swappable without touching the rest (R-2, QG-2), and every model must check without errors (R-3, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Interfaces between building blocks: the connectors in `HeatingLib.Interfaces`, and `System` wires blocks only through them.
- The variant mechanism: how a `Room` or `Thermostat` variant replaces the existing block.
- The dependency rule: whether a block may read another block's package constant (`Thermostat` reads `HeatingLib.roomHeatCapacity` today).
- Units: SI, temperatures in K internally, shown in °C.
- Result format: the `simulate()` output (CSV) is the one exchange format.
- Third-party dependencies: whether the Modelica Standard Library may be used (none today).
- Versioning of the library (none today).

Left to the building blocks (no ADR):

- The equations inside a model.
- Parameter defaults.
- The layout of `tests/check.mos`.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
