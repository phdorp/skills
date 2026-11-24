# 2. Connect blocks only through the connectors in Interfaces

## Status

proposed

## Context

Found in the code: `HeatingLib/System.mo` wires `Room` and `Thermostat` only through `connect(room.T, thermostat.T)` and `connect(thermostat.Q, room.Q_heat)`, using the connectors of `HeatingLib/Interfaces.mo`. This serves R-2 and QG-2: a block can be replaced if it keeps the same connectors.

## Decision

We connect blocks only through the connectors in `HeatingLib.Interfaces`.

## Consequences

A replacement block must offer the same connectors. This does not yet settle how a block is replaced; that is the variant mechanism, a separate decision on the central list.

Question for the architect: is this the rule we keep?
