# 2. Blocks connect through the connectors in Interfaces

## Status

proposed

## Context

Found in the code, not decided: `System.mo` connects `room.T` to `thermostat.T` and
`thermostat.Q` to `room.Q_heat`, using the connector types of `Interfaces.mo`. The dependency
rule of ADR 0001 is not kept: `Thermostat.mo` reads `HeatingLib.roomHeatCapacity`
(see ADR 0003). Serves R-2, QG-2.

## Decision

Blocks exchange values through the connectors in `Interfaces`, as `System.mo` wires them.

## Consequences

`Thermostat` reads a package constant, so swapping the room is not free (R-2). Bringing
`Thermostat` into line with the rule is work that waits for this ADR and ADR 0003 to be accepted.
