# 2. Interfaces between blocks

## Status

proposed

## Context

Found in the code, not decided by the architect: the blocks exchange signals only through the
connectors and signal types in `HeatingLib.Interfaces` (`Interfaces.mo`, `Room.mo`,
`Thermostat.mo`, `System.mo`). It serves R-2 and QG-1: a variant that keeps the connectors
replaces a block without changes to the others. This is the "Interfaces between blocks" item
of ADR-0001.

## Decision

We will exchange signals between blocks only through the connectors in `HeatingLib.Interfaces`
(`TemperatureInput`, `TemperatureOutput`, `HeatFlowInput`, `HeatFlowOutput`), and wire them in
`System`.

## Consequences

A variant with the same connectors replaces a block without changes to the other blocks. The
dependency rule of ADR-0001 is not yet covered by an ADR of its own, and the code breaks it:
`Room` and `Thermostat` both read the package constant `roomHeatCapacity` (see arc42 section 11).
