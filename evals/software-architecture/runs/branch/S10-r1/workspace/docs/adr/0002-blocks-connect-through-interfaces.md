# 2. Blocks connect only through the Interfaces connectors

## Status

proposed

## Context

Found in the code, not decided by the architect: `Room.mo`, `Thermostat.mo` and `System.mo`
connect only through the connector types in `Interfaces.mo`, and `System` is the only class that
instantiates `Room` and `Thermostat`. This is the first item of the accepted ADR 0001 list. It
serves replaceability (R-3, QG-2).

## Decision

We connect blocks only through the connectors in `Interfaces`, and only `System` names concrete
blocks.

## Consequences

The read of `HeatingLib.roomHeatCapacity` in `Room.mo` and `Thermostat.mo` bypasses the connectors.
It contradicts the second item of ADR 0001 and is recorded as a risk in arc42 section 11. A block
can be swapped inside `System.mo` alone only once that read is removed.
