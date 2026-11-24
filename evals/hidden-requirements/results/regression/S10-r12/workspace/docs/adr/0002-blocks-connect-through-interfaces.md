# 2. Blocks connect through Interfaces connectors

## Status

proposed

## Context

Found in the code (`System.mo`, `Interfaces.mo`), not decided by the architect. `System` connects
`Room` and `Thermostat` with `connect` statements on the four connectors declared in
`Interfaces.mo`. This serves R-2 (QG-2, modifiability) and the interface decision of ADR-0001.
The code departs from ADR-0001 in one point: `Room` and `Thermostat` also read the package
constant `HeatingLib.roomHeatCapacity`. That deviation is recorded in arc42 section 11.

## Decision

Blocks exchange signals only through the connectors in `Interfaces.mo`, and `System` connects them.

## Consequences

A variant that keeps the same connectors can replace a block without touching the other block
(R-2). The package-constant read stays a known deviation until the architect decides on it.
