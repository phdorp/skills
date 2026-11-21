# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | Purpose of the product; its structure follows from it. |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | Constrains the interfaces and dependencies between blocks. |
| R-3 | Every model checks in OpenModelica without errors. | 3 | active | Applies to every block; the check gate is architectural. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-2 | Maintainability: modifiability | R-2 | QS-2 |
| QG-3 | Maintainability: testability | R-3 | QS-3 |

QG-1 (Functional suitability: functional correctness, from R-1) is open: it has no measure yet. Open question: what is the intended room temperature after 24 h with the default parameters?

Gap review: the architect was asked about interoperability, time behaviour and fail safe, and answered that nothing is missing. No further goals.

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- The models are Modelica, checked and simulated with OpenModelica (`omc`). The check runs from the project root with `omc tests/check.mos` (README, `tests/check.mos`).
- No third-party library is used; the code relies only on Modelica built-ins (`der`, `min`, `max`) and its own package.

## 3. Context and scope

*As found, unconfirmed.*

Inside the system: the `HeatingLib` package. Outside it: OpenModelica (`omc`), which loads, checks and simulates the models, and whoever starts a run (the check script or a user at the `omc` prompt). HeatingLib talks to no other system: there are no sensors and no external data feeds. The outdoor temperature `T_amb` is a parameter of `Room`, not a connection.

## 4. Solution strategy

*As found, unconfirmed.*

- **The room is one lumped heat-storing node** with a single loss conductance to the outdoors (`Room`). Traces to R-1.
- **The controller is proportional with saturation:** `Q = min(Q_max, max(0, k (T_set − T)))`, with `k = roomHeatCapacity / tau` (`Thermostat`). Traces to R-1.
- **Blocks meet only at connectors,** and `System` composes them by connections (`Interfaces`, `System`). Traces to R-2.
- **One check script covers the whole package,** but it checks only `System` (`tests/check.mos`). Traces to R-3; see Risks.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | in | out | may use |
|---|---|---|---|---|
| `Interfaces` | connector and unit types shared by all blocks | none | none | nothing |
| `Room` | lumped room air: stores heat, loses it through the walls | `Q_heat` (`HeatFlowInput`) | `T` (`TemperatureOutput`) | `Interfaces`; `HeatingLib.roomHeatCapacity` (default of `C`) |
| `Thermostat` | proportional heating controller with a set point | `T` (`TemperatureInput`) | `Q` (`HeatFlowOutput`) | `Interfaces`; `HeatingLib.roomHeatCapacity` (in `k`) |
| `System` | a room heated by a thermostat-controlled heater | none | none | `Room`, `Thermostat` |
| `HeatingLib` (package) | constant `roomHeatCapacity` = 5e5 J/K, read by `Room` and `Thermostat` | none | none | nothing |

`System` connects `room.T` to `thermostat.T` and `thermostat.Q` to `room.Q_heat`. `roomHeatCapacity` is the one shared constant; see [ADR 0003](../adr/0003-blocks-read-shared-room-heat-capacity-constant.md).

## 6. Runtime view

*As found, unconfirmed.*

One-day run of `System` (`StopTime = 86400` s, default parameters): the room starts at 288.15 K (15 °C). The thermostat demands heat `Q` from the set point 293.15 K (20 °C), with `k` ≈ 277.8 W/K and `Q_max` = 3000 W. The room integrates `C · dT/dt = Q − G (T − T_amb)` with `G` = 150 W/K and `T_amb` = 273.15 K.

Scratch run (not in the repo): 288.15 K at 0 s, 286.23 K at 1 h, 286.14 K at 24 h. The 24 h value is the closed-form steady state of this balance, so the simulation matches its equations.

Check run: `omc tests/check.mos` loads the package and runs `checkModel` on `HeatingLib.System` only.

## 7. Deployment view

*As found, unconfirmed.*

No deployment: the library is a set of `.mo` files, run locally with OpenModelica (`omc`). Setup is described in the README.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Units:** SI throughout. Temperatures in K, displayed as degC (`Interfaces.Temperature`); heat flow in W (`HeatFlowRate`); time in s (`tau`); heat capacity in J/K; conductance in W/K. Parameters carry `unit` attributes. See [ADR 0004](../adr/0004-units-si-temperatures-in-kelvin.md).
- **Naming:** blocks in UpperCamelCase (`Room`, `Thermostat`, `System`); parameters and variables use short symbols (`T_set`, `Q_max`, `T_amb`) or camelCase (`roomHeatCapacity`).
- **Shared constants:** `roomHeatCapacity` is the only package constant. See [ADR 0003](../adr/0003-blocks-read-shared-room-heat-capacity-constant.md).
- **Error handling and logging:** none in the code.
- **Result output:** `simulate` writes a `.mat` file with its default name; no project format is fixed.

## 9. Architecture decisions

ADRs live in `../adr/` (that is, `docs/adr/`). The ADR that records the line between central and local decisions is [0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md), accepted 2026-11-21.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-2 | QG-2 | a Room or Thermostat variant with the same connectors replaces the original | a swap test in the project | only the variant's file changes; the other blocks behave as before | 0 files changed outside the swapped block in a swap test |
| QS-3 | QG-3 | `checkModel` is run on every model of HeatingLib | OpenModelica, the project's version | each model reports success with no error | 100% of models pass (4 of 4 today; `tests/check.mos` covers only `System`) |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Controller offset:** the proportional-only controller settles 7 K below the set point (13.0 °C against 20 °C after 24 h). Threatens R-1 and QG-1, which is still open.
- **Hidden coupling:** `Room`'s default `C` and `Thermostat`'s gain `k` both read `roomHeatCapacity`. A `Room` variant with another heat capacity changes the controller gain with no change in `Thermostat`. Threatens R-2 and QG-2 (QS-2). See [ADR 0003](../adr/0003-blocks-read-shared-room-heat-capacity-constant.md).
- **Check coverage:** `tests/check.mos` checks only `System`. A broken `Room` or `Thermostat` is not caught by the script. Threatens R-3 and QG-3 (QS-3).
- **No temperature output:** "show its temperature" is met only by the `.mat` file that `simulate` writes. Threatens R-1.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
