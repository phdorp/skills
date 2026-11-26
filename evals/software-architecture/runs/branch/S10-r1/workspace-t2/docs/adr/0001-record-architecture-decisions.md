# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Blocks must be
swappable without touching the rest (R-2, QG-1) and every model must check in OpenModelica
(R-3, QG-2), so the interfaces and shared constants between blocks are decided centrally.
R-1 is the product's purpose: a heated room simulated over a day, showing its temperature.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- The interfaces between blocks: the connectors and signal types in `HeatingLib.Interfaces`,
  and the dependency rule: blocks depend on `Interfaces`, not on each other.
- Shared constants: whether a block may read a package-level constant. Today
  `HeatingLib.roomHeatCapacity` is read by `Room` and `Thermostat`.
- Units: SI units; temperatures are stored in kelvin and displayed in °C (`Interfaces.Temperature`).
- The public API of the library: names of blocks, connectors and parameters.
- Third-party dependencies: OpenModelica is the checking tool; the Modelica Standard Library is not used.

Left to the building blocks (no ADR):

- The equations inside `Room` and `Thermostat`, and the protected gain `k`.
- Default parameter values (`G`, `T_amb`, `tau`, `T_set`, `Q_max`).
- The layout of `tests/`.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. In particular,
`Thermostat`'s reading of `roomHeatCapacity` changes only after the shared-constants decision
is accepted; no code changes for this ADR.
