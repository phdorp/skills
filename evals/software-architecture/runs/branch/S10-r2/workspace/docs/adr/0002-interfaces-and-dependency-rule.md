# 2. Interfaces and dependency rule between blocks

## Status

proposed

## Context

Found in the code, not decided by the architect: `HeatingLib/Interfaces.mo` defines the
connectors that `Room`, `Thermostat` and `System` use. But `Room.mo` and `Thermostat.mo` also
read the package constant `HeatingLib.roomHeatCapacity` (`package.mo`), so the two blocks depend
on each other through a shared value, not only through connectors. This decision is on the
accepted list ("Interfaces between blocks and the dependency rule"), and the code's coupling
works against R-2 and QG-2.

## Decision

Blocks connect through the connectors in `HeatingLib.Interfaces`: the room exposes `T` and takes
`Q_heat`; the thermostat takes `T` and gives `Q`; `System` wires them. `Room` and `Thermostat` also
read the package constant `roomHeatCapacity`, which the code does today.

## Consequences

A room with another heat capacity changes the controller's gain (`k = roomHeatCapacity / tau`),
so swapping the room alone is not possible; QS-1 is not met. The architect decides whether the
shared constant stays, or moves into a connector or a parameter. Either choice supersedes this
ADR. Changing the `Thermostat` coupling waits for this ADR's acceptance.
