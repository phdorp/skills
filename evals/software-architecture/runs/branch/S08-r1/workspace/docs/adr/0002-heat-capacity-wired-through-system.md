# 2. Pass the room heat capacity to the controller through System

## Status

proposed

## Context

R-2 and QG-2 require swapping the room without touching the rest; QS-2 measures that a
two-zone room leaves `Thermostat.mo` unchanged. `Thermostat` currently reads
`HeatingLib.roomHeatCapacity`, a package constant also read by `Room`. That bypasses the
`Thermostat → Interfaces` dependency rule of ADR-0001 and the arc42 §5 "may use" table. Under
QS-2 the controller keeps the gain of the old room, while its design rule `k = C / tau` no
longer holds for the new room.

## Decision

We will remove `roomHeatCapacity` from the package. `Thermostat` will take its heat capacity
`C` as a parameter without a default. `System` will wire it with
`Thermostat thermostat(C = room.C)`. `Room` keeps its own `C` default.

## Consequences

- Blocks depend only as ADR-0001 allows: `System → Room`, `Thermostat → Interfaces`.
- The controller gain follows the room it is wired to; QS-2 holds without a hidden coupling.
- `Thermostat` no longer runs standalone without a `C` value. Its callers must wire it.
- Changes `Thermostat.mo`, `System.mo`, `package.mo` and `Room.mo`'s default source. Nothing is
  changed in code until this ADR is accepted.
- Does not contradict ADR-0001. It enforces the dependency rule that ADR records.
- `tests/check.mos` pins the current steady state (286.137 K after 24 h) before the change. It
  is the behaviour check for this decision, and the change must keep it passing.
