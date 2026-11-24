# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | The purpose of the library; the other requirements depend on it simulating. |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | Fixes how blocks connect; expensive to change later. |
| R-3 | Every model checks in OpenModelica without errors. | 3 | active | A gate that keeps the other two honest; cheap to keep green now. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-2 | Flexibility: replaceability | R-2 | QS-1 |
| QG-3 | Maintainability: testability | R-3 | QS-2 |

No characteristic is missing from the goals: the architect answered the characteristics check with "nothing is missing" (2026-11-24). QG-1 (functional correctness, from R-1) has no measure yet and stays open.

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- The language is Modelica and the tool is OpenModelica: the README and `tests/check.mos` run `omc`.

## 3. Context and scope

*As found, unconfirmed.*

Inside the boundary: the library in `HeatingLib/`. Outside it: OpenModelica (`omc`), which loads, checks, compiles and simulates the models, and the person who reads the simulation result. No other system is called.

## 4. Solution strategy

*As found, unconfirmed.*

- A lumped model: the room is one temperature node, C·dT/dt = Q − G·(T − T_amb). Serves R-1.
- A proportional controller whose gain comes from the heat capacity and the time constant: k = C/τ, Q = min(Q_max, max(0, k·(T_set − T))). Serves R-1.
- Blocks are composed through connectors, so `System` wires them without knowing their internals. Serves R-2, QG-2.
- Each model is checked by OpenModelica. Serves R-3, QG-3.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | in | out | may use |
|---|---|---|---|---|
| `HeatingLib.Interfaces` | connector and unit types shared by all blocks | — | — | — |
| `HeatingLib.Room` | lumped room air: stores heat, loses it through the walls | `Q_heat` (heat flow) | `T` (temperature) | `Interfaces`, `roomHeatCapacity` |
| `HeatingLib.Thermostat` | proportional heating controller with set point | `T` (temperature) | `Q` (heat flow) | `Interfaces`, `roomHeatCapacity` |
| `HeatingLib.System` | a room heated by a thermostat | — | — | `Room`, `Thermostat` |
| `tests/check.mos` | runs OpenModelica's check on `HeatingLib.System` | — | — | `HeatingLib` package, `System` |

`roomHeatCapacity` is a package constant in `HeatingLib/package.mo`. `Room` and `Thermostat` both read it. It is a shared parameter, not a connector.

## 6. Runtime view

*As found, unconfirmed.*

Simulating `HeatingLib.System` for 86400 s (the `experiment` annotation) starts the room at `T_start` = 288.15 K. At each step the thermostat turns the measured `T` into `Q`, and the room integrates C·dT/dt = Q − G·(T − T_amb). With the current parameters the room ends the day at 286.14 K, 7 K below the set point of 293.15 K (my simulation run).

## 7. Deployment view

*As found, unconfirmed.*

Runs on a developer's machine with OpenModelica installed. The check runs from the project root (`omc tests/check.mos`). A simulation writes its files into the working directory. Nothing is deployed.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- Units: SI, with a `unit` attribute on every Real. Temperatures are in K and displayed in °C through `displayUnit` (`Interfaces`).
- Naming: physical symbols for parameters and variables (`C`, `G`, `T_amb`, `T_start`, `T_set`, `tau`, `Q_max`). Connectors are named by their signal: `T` (temperature), `Q` (heat flow).
- Package layout: every file starts with `within HeatingLib;`, and `HeatingLib/package.order` sets the load order.
- Documentation: each parameter and connector has a description string.
- Error handling and logging: none in the code.

## 9. Architecture decisions

The ADRs are in [`../adr/`](../adr/). The rule for which decisions the architect makes centrally is in [0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md), written once the architect confirms its list.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a variant of `Room` or `Thermostat` with the same connectors is added to replace the existing block | development | only the new variant file is added; `System` and the other block are unchanged and `System` still checks | 0 existing files changed outside the variant file |
| QS-2 | QG-3 | a developer changes any model and runs `tests/check.mos` | development with OpenModelica | the check covers every model class and fails the run if any of them reports an error | 0 errors across all model classes |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Shared constant, not the room's C:** `Thermostat` reads `HeatingLib.roomHeatCapacity`, not `Room.C`. A variant room with another C keeps the old controller gain. Threatens R-2, QG-2.
- **Concrete wiring:** `System` names `Room` and `Thermostat` directly, so a swap edits `System`. Threatens R-2, QG-2.
- **Proportional-only control:** the room settles 7 K below the set point after one day. Threatens R-1 and the set-point behaviour the architect has not yet confirmed.
- **Check does not fail:** `tests/check.mos` checks only `System` and prints errors without failing the run. Threatens R-3, QG-3.
- **No defined output:** the code defines no plot or result file for the temperature; "show" depends on OpenModelica's defaults. Threatens R-1.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
