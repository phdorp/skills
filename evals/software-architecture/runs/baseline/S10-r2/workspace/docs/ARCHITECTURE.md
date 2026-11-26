# HeatingLib architecture

HeatingLib is a Modelica library that simulates the temperature of one room heated by a
proportional thermostat over one day (86 400 s).

This document describes the structure of the library, the requirements it is held to, how
it currently measures up against them, and the design that meets requirement 2. Section
[Status against requirements](#status-against-requirements) records what was verified and when.

## Requirements

1. Simulate a heated room over a day and show its temperature.
2. Swap the room or the controller for another variant without touching the rest.
3. Every model checks in OpenModelica without errors.

## Status against requirements

Verified 2026-11-21 with OpenModelica 1.27.2 (`omc`), by running `checkModel` on each model
and `simulate(HeatingLib.System, stopTime=86400)`.

| # | Status | Evidence |
|---|--------|----------|
| 1 | **Partly met.** The day simulates, but nothing shows the temperature. | The run succeeds. `room.T` falls from 288.15 K to 286.14 K within about an hour and stays there. It never reaches the 293.15 K set point. No plotting or reporting script exists. |
| 2 | **Not met.** | `System` hard-codes `Room room` and `Thermostat thermostat` with no `replaceable`. `Thermostat` reads the package constant `HeatingLib.roomHeatCapacity`, so a room variant with a different heat capacity leaves the controller tuned for the wrong room. See [Coupling problems](#coupling-problems). |
| 3 | **Met, not enforced.** | `checkModel` passes with no errors or warnings for `Room`, `Thermostat` and `System`. `tests/check.mos` checks only `System`, so the other two are not guarded. |

## Package structure

```
HeatingLib (package.mo)        package constant roomHeatCapacity = 5e5 J/K
├── Interfaces                 unit types and signal connectors
├── Room                       lumped room air mass          (uses Interfaces)
├── Thermostat                 proportional controller        (uses Interfaces, HeatingLib.roomHeatCapacity)
└── System                     Room + Thermostat wired together (uses Room, Thermostat)

tests/check.mos                OpenModelica check script (run from the project root)
package.order                  load order of the package members
```

### Interfaces (`HeatingLib/Interfaces.mo`)

- `Temperature`: `Real` in K, minimum 0, displayed in °C.
- `HeatFlowRate`: `Real` in W.
- Connectors: `TemperatureInput`, `TemperatureOutput`, `HeatFlowInput`, `HeatFlowOutput`.
  They are typed `input`/`output` signals, not physical connectors.

### Room (`HeatingLib/Room.mo`)

A single heat-storage node for the room air.

- Equations: `C * der(T) = Q_heat - G * (T - T_amb)`; initial equation `T = T_start`.
- Parameters: `C` (heat capacity, defaults to the package constant), `G` (wall conductance,
  150 W/K), `T_amb` (273.15 K), `T_start` (288.15 K).
- Ports: input `Q_heat`, output `T`.

### Thermostat (`HeatingLib/Thermostat.mo`)

A proportional controller with saturation.

- Equation: `Q = min(Q_max, max(0, k * (T_set - T)))`.
- Parameters: `T_set` (293.15 K), `tau` (1800 s), `Q_max` (3000 W).
- Derived (protected): `k = HeatingLib.roomHeatCapacity / tau` (W/K), the controller gain.
- Ports: input `T`, output `Q`.

### System (`HeatingLib/System.mo`)

- Components: `room`, `thermostat`.
- Connections: `room.T → thermostat.T`, `thermostat.Q → room.Q_heat`.
- Experiment: `StopTime = 86400`.

### Signal flow

```
           +-----------+   T (output)    +--------------+
           |   Room    |---------------->|  Thermostat  |
           |           |                 |              |
           |  C dT/dt  |<----------------|  Q = clamp(  |
           |  = Q - G  |   Q_heat (input)|  k(Tset - T))|
           |   (Tamb)  |   Q (output)    |              |
           +-----------+                 +--------------+
```

## Coupling problems

These block requirement 2.

1. **The controller depends on a package constant.** `Thermostat.k` is computed from
   `HeatingLib.roomHeatCapacity`, not from the room it controls. Replacing the room with one
   whose `C` differs leaves `k` unchanged, so the controller's tuning no longer matches the
   plant.
2. **Two sources of truth for `C`.** `Room.C` defaults to the same constant. The two only agree
   by convention. Nothing enforces it.
3. **`System` names concrete classes.** Without `replaceable` declarations, swapping a
   component means editing `System`, which breaks the "without touching the rest" rule.

## Behaviour issues

These do not break the requirements as written, but they will surprise anyone using the
library.

- **Steady-state offset.** Proportional-only control with `G = 150 W/K` settles at

  `T_eq = (k * T_set + G * T_amb) / (k + G) = 286.14 K` (13.0 °C), with the heater at 1948 W.

  The set point is 20 °C, a 7 K offset. The simulation reproduces this value to six digits.
  Removing it needs integral action, which a replaceable controller variant can provide.
- **`tau` does not mean what its description says.** The description reads "time to close the
  gap to the set point". The closed-loop time constant is actually `C / (k + G)`, which is
  about 1169 s here, not 1800 s.
- **`package.order` lists `roomHeatCapacity`,** which is a constant, not a class. Loading is
  unaffected, but the entry is misleading.

## Target design for requirement 2

The goal is that a room or controller variant lives in its own file and is selected by
redeclaration, with `System`'s connections unchanged.

1. **Partial base classes** define the contracts.
   ```modelica
   partial model PartialRoom
     Interfaces.HeatFlowInput Q_heat "Heating power into the room";
     Interfaces.TemperatureOutput T "Room temperature";
   end PartialRoom;

   partial block PartialThermostat
     Interfaces.TemperatureInput T "Measured room temperature";
     Interfaces.HeatFlowOutput Q "Heating power demand";
   end PartialThermostat;
   ```
2. **Concrete classes extend the partials.** `Room` and `Thermostat` add `extends PartialRoom`
   and `extends PartialThermostat`, and each keeps its own parameters. They drop their own
   copies of the port declarations, which the partial now supplies.
3. **Controller tuning stays local.** `Thermostat` takes its gain as its own parameter
   (in W/K) rather than deriving it from a package constant. Tuning then does not depend on
   the room, and a new room needs no change to the controller.
4. **`System` uses `replaceable`.**
   ```modelica
   replaceable HeatingLib.Room room constrainedby HeatingLib.PartialRoom;
   replaceable HeatingLib.Thermostat thermostat constrainedby HeatingLib.PartialThermostat;
   ```
   Its `connect` statements do not change.
5. **Variants are subclasses.** A variant is a model that redeclares one slot:
   ```modelica
   model SlowRoomSystem
     extends HeatingLib.System(redeclare HeatingLib.Room room(C = 1e6));
   end SlowRoomSystem;
   ```
   A new controller is a new file that extends `PartialThermostat`; the room and `System`
   are not edited.
6. **Dependency rule.** `Room` and `Thermostat` may import only `Interfaces`. Only `System`
   and the variants name both. The package constant `roomHeatCapacity` is removed, or kept
   only as a default inside `Room`.

Items 1 to 6 are the design, not current code. The `replaceable` change is the only part that
touches `System`.

The partial classes, the `replaceable` declarations and the `SlowRoomSystem` variant were
checked with `checkModel` in a scratch copy of the library (`/tmp/hl-target`), not in the
repository. The scratch check passed, with one warning: `package.order` must list the new
partial files (item 1 needs `PartialRoom` and `PartialThermostat` added to it).

## Checking and simulating

Check every model before merging. The current script covers only `System`, so extend it to
cover every model, not just the top-level one.

```sh
omc tests/check.mos          # from the project root
```

To simulate the day and read the temperature, run from a scratch directory, because `omc`
writes its build output into the current directory:

```sh
cd "$(mktemp -d)"
cat > run.mos <<'EOF'
loadFile("<project>/HeatingLib/package.mo");
simulate(HeatingLib.System, stopTime=86400, numberOfIntervals=24, outputFormat="csv");
EOF
omc run.mos                  # writes HeatingLib.System_res.csv with room.T
```

Replace `<project>` with the absolute path to the repository.

## Open items

- Add a plotting or reporting step for requirement 1.
- Make `tests/check.mos` check `Room`, `Thermostat`, and any variant as well as `System`.
- Decide the controller design: keep proportional control and document the offset, or add
  integral action via a new `PartialThermostat` variant.
- Fix the `tau` description or change the parameter to a gain.
- Remove `roomHeatCapacity` from `package.order` and list the partial files in it.
