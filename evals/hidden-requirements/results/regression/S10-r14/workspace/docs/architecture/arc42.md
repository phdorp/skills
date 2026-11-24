# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | Core function; the other requirements are checked against it. |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | Sets the structure everything else builds on: interfaces between blocks and the dependency rule. |
| R-3 | Every model checks in OpenModelica without errors. | 3 | active | A gate on every change, so it applies throughout. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-2 | Maintainability: modularity | R-2 | QS-1 |
| QG-3 | Maintainability: testability | R-3 | QS-2 |

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- The library is written in Modelica and checked with OpenModelica (`README.md`,
  `tests/check.mos`).

## 3. Context and scope

*As found, unconfirmed.*

The boundary is the `HeatingLib` package. Outside it sit OpenModelica (`omc`), which checks and
simulates the models, and the result file a simulation writes. No other system is connected.

## 4. Solution strategy

*As found, unconfirmed.*

- A lumped model: one heat-capacity node for the room air, with heat loss through one
  conductance `G` to the outdoor temperature (R-1; QG-1 has no measure yet).
- Proportional heating control with a power limit (R-1).
- Blocks connected only through their connectors (R-2, QG-2; [ADR-0002](../adr/0002-interfaces-between-blocks.md)).
- One package constant read by two blocks (R-2, QG-2; [ADR-0003](../adr/0003-dependency-rule-shared-constants.md)).
- Every model checked by OpenModelica (R-3, QG-3; [ADR-0006](../adr/0006-openmodelica-as-only-tool.md)).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | in | out | may use |
|---|---|---|---|---|
| Interfaces | connectors and types: `Temperature` (K), `HeatFlowRate` (W), and four connectors | — | — | none |
| Room | lumped room air: stores heat, loses it through the walls | `Q_heat` (HeatFlowInput) | `T` (TemperatureOutput) | Interfaces; the shared constant `roomHeatCapacity` (default of `C`) |
| Thermostat | proportional heating controller with a set point and a power limit | `T` (TemperatureInput) | `Q` (HeatFlowOutput) | Interfaces; the shared constant `roomHeatCapacity` (in `k`) |
| System | one room and one thermostat, connected; stop time 86400 s | — | — | Room, Thermostat |

`HeatingLib.roomHeatCapacity` (`package.mo`, 5e5 J/K) is a shared constant: `Room` and `Thermostat`
both read it, and neither owns it ([ADR-0003](../adr/0003-dependency-rule-shared-constants.md)).

## 6. Runtime view

*As found, unconfirmed.*

A one-day simulation of `System` starts the room at 288.15 K. Each step, the thermostat sends a
heating power of `min(Q_max, max(0, k·(T_set − T)))` W into the room. In a scratch simulation run on
2026-11-24 (not stored in the project) the room ends near 286.1 K with about 1.9 kW of heating: the
set point of 293.15 K is not reached.

## 7. Deployment view

*As found, unconfirmed.*

No deployment: the library runs in OpenModelica on the developer's machine. The check runs from
the project root with `omc tests/check.mos` (`README.md`).

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Units:** SI throughout; temperatures in K, displayed in °C; heat flow in W; heat capacity in
  J/K; time in s ([ADR-0005](../adr/0005-si-units-with-kelvin.md)).
- **Naming:** Modelica class names in UpperCamelCase; short variable names (`T`, `Q`, `C`, `G`,
  `T_amb`, `T_start`, `T_set`, `tau`, `Q_max`).
- **Documentation:** every element has a description string.
- **Errors and logging:** none in the code.

## 9. Architecture decisions

ADRs live in `../adr/`. The list of decisions made centrally is the ADR
[0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md), accepted
2026-11-24.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a new room variant is added | normal development | only the new variant and the system composition change | 0 existing blocks edited |
| QS-2 | QG-3 | any model is changed | normal development | the full check runs over every model | 0 check errors across all models in one run |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Shared constant couples Room and Thermostat:** a room variant with another heat capacity
  silently changes the controller's gain `k = roomHeatCapacity / tau`. Threatens QG-2.
- **Fixed block types in System:** `System` names `Room` and `Thermostat` as concrete types, so
  swapping a block means editing `System`. Threatens R-2 and QG-2.
- **Proportional-only controller:** after a day the room settles about 7 K below the set point
  (286.1 K against 293.15 K). Threatens R-1; QG-1 has no measure yet.
- **Partial check script:** `tests/check.mos` checks only `HeatingLib.System`; `Room` and
  `Thermostat` are checked only when run by hand. Threatens QG-3.
- **No check of simulation results:** nothing tests the simulated temperature against an expected
  value. Threatens QG-1.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
