# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | It is the product's purpose; it fixes the `System` model and its one-day run. |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | It fixes the interfaces between blocks and the dependency rule. Today `Thermostat` reads `Room`'s constant `roomHeatCapacity`, so R-2 is not met yet. |
| R-3 | Every model checks in OpenModelica without errors. | 3 | active | It applies to every block, so it constrains all of them. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: modularity | R-2 | QS-1 |
| QG-2 | Maintainability: testability | R-3 | QS-2 |

## 2. Constraints

*As found, unconfirmed.*

- Modelica is the modelling language: packages, models, blocks and connectors.
- OpenModelica (`omc`) is the tool the library is checked and simulated with (`README.md`,
  `tests/check.mos`). See ADR 0006.
- `HeatingLib/package.order` fixes the load order of the package's parts.

## 3. Context and scope

*As found, unconfirmed.*

The library ends at its models in `HeatingLib`. Outside it sits OpenModelica, which loads,
checks and simulates them (`tests/check.mos`, `README.md`). The outdoor temperature `T_amb`
is a constant parameter of `Room`, not an input from outside. The code references no other
external system.

## 4. Solution strategy

*As found, unconfirmed.*

- **Lumped room model.** The room is one temperature node: `C · dT/dt = Q_heat − G · (T − T_amb)`
  (`Room`). Serves R-1.
- **Proportional controller with saturation.** `Q = min(Q_max, max(0, k · (T_set − T)))`, with
  gain `k = C / tau` (`Thermostat`). Serves R-1.
- **Typed connectors.** Blocks are connected through the connectors in `HeatingLib.Interfaces`,
  and `System` wires them. Serves R-2. See ADR 0002.
- **One shared constant for the heat capacity.** Both `Room` and `Thermostat` read
  `HeatingLib.roomHeatCapacity`. Serves R-2 only in part; see section 11 and ADR 0003.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | in | out | may use |
|---|---|---|---|---|
| Interfaces | connectors and units shared by all blocks | — | — | — |
| Room | lumped room air: stores heat, loses it through the walls | `Q_heat` (`HeatFlowInput`) | `T` (`TemperatureOutput`) | Interfaces; `HeatingLib.roomHeatCapacity` |
| Thermostat | proportional heating controller with a set point and a power limit | `T` (`TemperatureInput`) | `Q` (`HeatFlowOutput`) | Interfaces; `HeatingLib.roomHeatCapacity` |
| System | a room heated by a thermostat-controlled heater; connects Room and Thermostat | — | — | Room; Thermostat |

`HeatingLib.roomHeatCapacity` (5e5 J/K) is a package constant, not a block. `Room` reads it as
its parameter `C`, and `Thermostat` reads it in its gain `k`. See ADR 0003.

## 6. Runtime view

*As found, unconfirmed.*

The one-day run of `System` (experiment `StopTime = 86400` s) starts with the room at 288.15 K
(15 °C). At each step `Thermostat` reads `room.T` and sets the heating power `Q`, and `Room`
integrates its heat balance.

Simulated with OpenModelica 1.27.2 from a scratch directory outside the repository:

| time | room temperature |
|---|---|
| 0 s | 288.15 K (15.0 °C) |
| 3600 s | 286.23 K (13.1 °C) |
| 86400 s | 286.14 K (13.0 °C) |

The heating power at 86400 s is 1948 W, below `Q_max` = 3000 W. The set point of 293.15 K
(20 °C) is not reached. See section 11.

## 7. Deployment view

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Units.** SI throughout. `Interfaces.Temperature` is in K and displays in °C; heat flow in W,
  `tau` in s, `C` in J/K, `G` in W/K. See ADR 0004.
- **Naming.** Blocks and packages are in PascalCase. Parameters and connectors are named after
  their quantity (`T_set`, `Q_max`, `T_amb`, `T_start`, `Q_heat`). Every block and parameter has
  a description string.
- **Errors.** The code has no error handling. The controller limits its output to `[0, Q_max]`
  instead of checking its inputs.
- **Shared constants.** A package-level constant is referenced by its qualified name,
  `HeatingLib.roomHeatCapacity`. See ADR 0003.

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The decision on what is decided centrally is
[0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a developer replaces `Room` with a variant that has a different heat capacity | development | only the variant's file changes; `Thermostat` and `System` are unchanged | 0 files outside the variant change |
| QS-2 | QG-2 | a developer runs the OpenModelica check on every model in `HeatingLib` | development | every model checks without errors | 0 check errors across all models |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **The controller depends on the room's constant.** `Thermostat`'s gain reads
  `roomHeatCapacity`, so a `Room` variant with another heat capacity changes the controller
  without touching it. Threatens R-2 and QG-1. See ADR 0003.
- **The room does not reach its set point.** The controller is proportional only. With the
  defaults, the room settles at 286.14 K (13.0 °C) against a set point of 293.15 K (20 °C),
  with the heater at 1948 W, below its limit. So the gap is not caused by saturation. Threatens
  R-1: the temperature shown is not the set point. Whether this is intended is the architect's
  decision.
- **The check covers one model.** `tests/check.mos` checks only `HeatingLib.System`. `Room` and
  `Thermostat` check cleanly when checked by hand, but nothing checks them automatically.
  Threatens R-3 and QG-2.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
