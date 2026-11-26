# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Block boundaries and
shared constants are expensive to change once blocks depend on them, and the library must stay
checkable for every model (R-2, QG-2; R-3, QG-3). `Thermostat` already reads a package constant
that `Room` also uses, which breaks the rule below (R-2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Interfaces between blocks and the dependency rule: blocks connect only through the connectors
  in `Interfaces`; no block reads another block's parameters or package constants.
- Shared package constants, such as `roomHeatCapacity`: whether blocks may read them, and where
  the value lives.
- Units: SI, temperatures in K with `displayUnit` degC, as `Interfaces.Temperature` does.
- Simulation output format: OpenModelica's default result file, or another.
- Names of public packages, components and connectors, since variants depend on them.
- Third-party dependencies: OpenModelica as the tool; no Modelica Standard Library today.

Left to the building blocks (no ADR):

- Equations inside a block, parameter default values, and the test layout beyond the check script.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. Fixing the
`Thermostat` read of `roomHeatCapacity` is such work.
