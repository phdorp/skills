# 2. Pass the room's heat capacity through the controller's port

## Status

proposed

## Context

The controller's gain depends on the room's heat capacity. Today both `Room` and `Thermostat`
read the package constant `HeatingLib.roomHeatCapacity`, so the controller is tuned to a value
that a room parameter override does not change. Verified with OpenModelica: with `room.C`
overridden to 1e6, the controller output at t = 0 stays at 1388.89 W; a gain that followed the
room would give 2777.78 W. The check still passes.

This serves QG-2 (replaceability, QS-2: replacing `Room` must leave `Thermostat` correct) and
QG-1 (modifiability, QS-1: a wall-model change stays in `Room.mo`).

It contradicts the arc42 §5 "may use" table (`Room` and `Thermostat` may use only `Interfaces`)
and the dependency rule decided centrally in ADR-0001.

## Decision

We will remove the package constant `roomHeatCapacity`. `Room` owns its heat capacity `C`.
`Thermostat` takes `C` as a parameter with no default, and `System` binds it:
`Thermostat thermostat(C = room.C)`.

## Consequences

- The controller follows the room's capacity through the parameter binding, so a changed room
  no longer leaves the controller mistuned.
- `Thermostat`'s interface gains one parameter, which `System` must bind. Any other system that
  uses `Thermostat` must bind it too.
- The arc42 §5 "may use" table must be updated if this is accepted: `Thermostat` uses only
  `Interfaces`, and `Room` no longer reads the package.
- ADR-0001's dependency rule is affected: `Thermostat` gets its capacity from `System`, not from
  the library package. No block depends on another block.
- A safety-net test (see the improve-codebase-architecture report, candidate 3) follows this ADR
  once accepted; it is not part of this decision.
- The replaceable-room candidate (report candidate 2) waits for this ADR, since a two-zone room
  with another capacity would otherwise leave the controller mistuned.
