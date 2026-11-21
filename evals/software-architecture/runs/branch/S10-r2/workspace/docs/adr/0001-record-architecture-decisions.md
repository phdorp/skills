# 1. Record architecture decisions

## Status

accepted 2026-11-21

## Context

The architect decides the architecture; contributors and agents build it. HeatingLib must
simulate a heated room over a day and show its temperature (R-1), let a room or controller
variant be swapped without touching the rest (R-2, QG-2), and have every model check in
OpenModelica without errors (R-3, QG-3). The line below decides what those depend on.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Dependency rule and interfaces: blocks connect only through the connectors in `Interfaces`;
  no block reads another block's parameters or constants. Today `Thermostat` reads
  `HeatingLib.roomHeatCapacity`.
- Ownership of the shared constant `HeatingLib.roomHeatCapacity`: who may read it.
- Units: SI; temperatures in K, power in W, heat capacity in J/K.
- Format of the simulated temperature output.
- Tooling dependency: OpenModelica for simulation and checks. Any added Modelica library is
  decided through this list.

Left to the building blocks (no ADR):

- Equations inside `Room` and `Thermostat`, parameter defaults, the internal structure of each
  block, and the layout of the check script.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. None of the
central items has its own ADR yet; each is written when work needs it. Among others, changing
how `Thermostat` gets the room's heat capacity, typed component declarations in `System` for
R-2, and the output format wait for those ADRs.
