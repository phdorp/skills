# 2. Controller gain takes the room's heat capacity as a parameter

## Status

proposed

## Context

`Thermostat` derives its gain `k = C / tau` from the package constant
`HeatingLib.roomHeatCapacity`, which `Room` also reads as its default `C`. The controller's
interface does not show this dependency, and `arc42` section 5 allows `Thermostat` to use only
`Interfaces`. Overriding `room.C` in `System` leaves the controller gain unchanged, so the two
drift apart without any error (checked with OpenModelica 1.27.2).

Forces: QG-2 (replaceability, QS-2: a two-zone room replaces `Room` and `Thermostat` works
unchanged) and QG-1 (modifiability, QS-1: a wall-model change stays in `Room.mo`). R-2 asks for
swapping the room without touching the rest.

## Decision

We will give `Thermostat` the heat capacity as its own parameter `C`, with no default, and
`System` will wire it from the room: `Thermostat thermostat(C = room.C)`. `Thermostat` will no
longer read the package constant. `Room` keeps the package constant as its default.

## Consequences

- The controller gain follows the room it is wired to. Checked: `room(C = 1e6)` gives
  `k = 1e6 / tau`, and `checkModel` passes.
- The `Thermostat` interface now lists its dependency on the room. This is a one-time edit to
  `Thermostat.mo`; later room variants must expose `C` and need no controller edits.
- Trade-off: a room variant with no single heat capacity cannot drive this controller as it
  is. That case needs a new decision when QS-2 is built.
- No connector changes in `Interfaces`, so ADR-0001 is unaffected. `System` wires a parameter;
  blocks still do not depend on each other.
- The current code breaks the `arc42` section 5 rule that `Thermostat` may use only `Interfaces`;
  this decision restores it. No change to arc42 is needed.
