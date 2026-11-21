# 3. Units and quantities

## Status

proposed

## Context

Found in the code, not decided by the architect: `HeatingLib/Interfaces.mo` types temperature
and heat flow with quantity and unit annotations (`Temperature` in K, `displayUnit = "degC"`;
`HeatFlowRate` in W), and parameters carry units (`J/K`, `W/K`, `s`). This is on the accepted
list ("Units and quantities"). It serves R-1, whose output is a temperature trajectory. QG-1 is
still open, so it is not cited by ID.

## Decision

Quantities use SI: temperature in K internally, heat flow in W, and time in s. Each unit is
declared with a `unit` or `quantity` annotation; temperatures carry `displayUnit = "degC"` for
display.

## Consequences

Units checked by OpenModelica are only as strict as these annotations; `Real` parameters without
a unit annotation are not checked. Changing any unit waits for this ADR's acceptance.
