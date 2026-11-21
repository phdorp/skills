# 1. Record architecture decisions

## Status

accepted 2026-11-21

## Context

The architect decides the architecture; contributors and agents build it. HeatingLib needs
the line drawn so that a room or a controller can be swapped without touching the rest (R-2,
QG-2) and so that every model passes OpenModelica checks (R-3, QG-3), while the one-day
simulation of a room stays in place (R-1).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Interfaces between blocks and the dependency rule: blocks communicate only through the
  connectors in `HeatingLib.Interfaces`; no block reads another block's constant
  (`Thermostat` currently reads `HeatingLib.roomHeatCapacity`, which this rule forbids).
- Units and quantities: SI, temperature in K internally, `displayUnit` for °C.
- Naming and package layout: the `HeatingLib` package, its model and block names, and
  `package.order`.
- Output and export format of the simulation result: open, no format chosen yet.
- Third-party dependencies: OpenModelica is the only tool; the Modelica Standard Library is
  not used.

Left to the building blocks (no ADR):

- Equations and parameter defaults inside one model.
- Test layout (`tests/check.mos`).

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. Changing the
`roomHeatCapacity` coupling in `Thermostat` waits for the interface rule to be accepted.
