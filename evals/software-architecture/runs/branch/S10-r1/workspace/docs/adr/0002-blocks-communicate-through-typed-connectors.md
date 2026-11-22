# 2. Blocks communicate through typed connectors

## Status

proposed

## Context

Found in the code, not decided by the architect: `HeatingLib/Interfaces.mo` defines the
connectors `TemperatureInput`, `TemperatureOutput`, `HeatFlowInput` and `HeatFlowOutput`;
`Room` and `Thermostat` use them; `System` wires them with `connect`. Serves R-2 and QG-1: a
swapped block must keep these connectors.

## Decision

We connect blocks only through the connectors defined in `HeatingLib.Interfaces`, and `System`
wires them with `connect`.

## Consequences

A variant of `Room` or `Thermostat` works in `System` as long as it keeps these connectors. This
rule does not cover shared constants, which are decided in ADR 0003.
