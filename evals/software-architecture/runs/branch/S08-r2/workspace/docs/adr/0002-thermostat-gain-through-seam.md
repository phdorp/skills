# 2. Give the Thermostat its gain through the seam

## Status

proposed

## Context

R-2 and QG-2 require that a modeller can swap `Room` for another variant without touching the
rest (QS-2: `Thermostat` works unchanged with a two-zone room). Today `Thermostat` computes its
gain `k = roomHeatCapacity / tau` from the package constant `HeatingLib.roomHeatCapacity`. It
reads that constant directly, not through its ports, and `Room` only uses the constant as a
default for `C`. Overriding `Room.C` therefore leaves the controller tuned to the old capacity,
with no error. This bypasses the block's interface, which ADR-0001 requires to hold the
block's dependencies. It is a seam problem, not a refactoring preference.

## Decision

We will give `Thermostat` the room's heat capacity as its own parameter, and `System` will
bind that parameter to `room.C`. `Thermostat` will no longer read `HeatingLib.roomHeatCapacity`.

## Consequences

- The dependency rule in ADR-0001 is unchanged: `System` → `Room` and `Thermostat`,
  `Thermostat` → `Interfaces`, and no block depends on another block.
- `Room` keeps the package constant as its default for `C`.
- `Interfaces` and the connector set are unchanged, so this ADR does not touch ADR-0001's
  central list for connectors.
- QS-2 holds for a room whose capacity differs from the default, which it does not today.
- arc42 section 5 (building block table) lists `Thermostat` as using `Interfaces` only. After
  the change it uses no package constant, and that table should be updated when this ADR is
  accepted.
- Follow-on work waits for acceptance: the code change in `Thermostat.mo` and `System.mo`, and
  a safety-net check for the wiring.
- Moving `roomHeatCapacity` into `Interfaces` is not part of this decision. It would change the
  central connector set and would need its own ADR.
