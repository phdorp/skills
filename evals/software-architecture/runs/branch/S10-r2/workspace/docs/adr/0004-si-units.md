# 4. Quantities use SI units; temperatures are shown in degC

## Status

proposed

## Context

Found in the code, not decided: `Interfaces.mo` types temperatures in K with `displayUnit = "degC"`
and heat flow in W; parameters in `Room.mo` and `Thermostat.mo` carry `unit` attributes (J/K, W/K,
s). Serves R-1, whose temperature output the units make readable.

## Decision

Quantities use SI units. Temperatures are stored in K and displayed in degC.

## Consequences

Every new quantity needs an SI unit attribute. Changing a unit is a change to `Interfaces`
and every block that uses it.
