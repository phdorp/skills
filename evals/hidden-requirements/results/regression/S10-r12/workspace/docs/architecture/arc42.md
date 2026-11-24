# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulating `HeatingLib.System` over 86 400 s yields the room temperature as a result variable and a plot. | 1 | active | It is the product's purpose; all else serves it. Triage: shapes `System` and its outputs. |
| R-2 | Replacing `Room` or `Thermostat` by a variant changes one file and one `System` line. | 3 | active | Largest change; depends on R-1 and R-3. Triage: crosses block boundaries (variant interfaces, dependency rule). |
| R-3 | Every model in `HeatingLib` passes `checkModel` and `simulate` with no errors or warnings. | 2 | active | It gates every other change. Triage: crosscutting verification rule. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1 | QS-1 |
| QG-2 | Maintainability: modifiability | R-2 | QS-2 |
| QG-3 | Maintainability: testability | R-3 | QS-3 |

Not a goal: Performance efficiency: time behaviour. The architect needs no measure for it (nothing missing).

### Stakeholders

- Modelers who run the simulation on a desktop with OpenModelica 1.27 and no other tooling.

## 2. Constraints

- OpenModelica 1.27 is the only tool.
- The Modelica Standard Library is the only third-party dependency.
- No budget or licence limit beyond OpenModelica's own.

*As found, unconfirmed.*

- The code is plain Modelica, with no library imports.
- The check is run with `omc tests/check.mos` from the project root (README).

## 3. Context and scope

- Out of scope for version 1: several rooms, humidity, real-time or hardware-in-the-loop operation, and a time-varying outdoor temperature (the outdoor temperature is constant at 0 °C).
- Outside the system: nothing. It keeps no data, exchanges nothing beyond its result files, and no law or contract applies.

*As found, unconfirmed.*

- OpenModelica (`omc`) is the only external program the code runs under. The code itself reads no files and talks to no service.

## 4. Solution strategy

*As found, unconfirmed.*

- The room is one lumped heat-capacity state, `T`, that loses heat through the walls in proportion to `T - T_amb` (`Room.mo`).
- The heater is a proportional controller: its power is `k * (T_set - T)`, clamped to 0 and `Q_max`, with `k = C / tau` (`Thermostat.mo`). It has no integral term, so it leaves a steady-state offset from the set point (see QG-1 and section 11).
- Blocks are connected by connectors only (see ADR-0002).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | in | out | may use |
|---|---|---|---|---|
| Interfaces | Connector and signal types shared by all blocks | — | — | none |
| Room | Lumped room air: stores heat and loses it through the walls | `Q_heat` (heat flow in) | `T` (temperature out) | Interfaces; `HeatingLib.roomHeatCapacity` |
| Thermostat | Proportional controller: heating power from the set point and the measured temperature | `T` (temperature in) | `Q` (heat flow out) | Interfaces; `HeatingLib.roomHeatCapacity` |
| System | Connects one Room and one Thermostat into a heated room | — | — | Room, Thermostat |

`HeatingLib.roomHeatCapacity` (5e5 J/K, in `package.mo`) is a package constant. `Room` reads it
for its heat capacity `C`, and `Thermostat` reads it for its gain `k`. Both blocks couple through
it: a variant with a different heat capacity would detune the controller.

## 6. Runtime view

*As found, unconfirmed.*

Simulating `System` for 86 400 s, from the experiment annotation:

1. The room starts at `T_start` = 288.15 K (15 °C).
2. `Thermostat` reads the room temperature `T` and computes the heating power `Q` from the set point.
3. `Room` integrates `C * der(T) = Q_heat - G * (T - T_amb)`.
4. The room settles at about 286.1 K (12.99 °C) and stays there, because the controller's proportional offset means it never reaches the 293.15 K set point.

## 7. Deployment view

*As found, unconfirmed.*

The code runs on a developer desktop with OpenModelica: `omc tests/check.mos` from the project root. There is no deployment.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- Units: SI types with `final quantity` and `final unit` in `Interfaces.mo`; `Temperature` is in K and displays in degC (ADR-0003).
- Naming: the package is `HeatingLib`; classes are CamelCase; connectors are named `…Input` or `…Output` after their direction.
- Parameters carry a unit and a description string.
- Error handling and logging: none. The code has no asserts and writes no log.

## 9. Architecture decisions

Decisions are recorded as ADRs in [docs/adr/](../adr/). The line between centrally made and
local decisions is drawn in [0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md)
(accepted 2026-11-24).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | `HeatingLib.System` is simulated for 86 400 s from a room at 15 °C, with the set point at 20 °C and the outdoor temperature constant at 0 °C | normal operation | the room temperature reaches the set point and stays within the tolerance | the room temperature after 24 h is within 0.5 K of 20 °C |
| QS-2 | QG-2 | a variant of `Room` or `Thermostat` replaces the original | normal development | only the variant's file and one line in `System` change; no other block changes | 1 model file and 1 `System` line changed; 0 lines changed in other blocks |
| QS-3 | QG-3 | the whole package is checked with one command | normal development | every model passes `checkModel` and `simulate` | 0 errors and 0 warnings across all models in the package |

## 11. Risks and technical debt

*As found, unconfirmed.*

- QG-1 is not met by the current code: the room settles at about 13 °C against the 20 °C set point, because proportional-only control leaves a steady-state offset of about 7 K. Threatens: R-1.
- QG-2 is not met by the current code: `Room` and `Thermostat` both read `HeatingLib.roomHeatCapacity`, and `System` names both parts concretely with no `replaceable`. A variant with another heat capacity would detune the controller silently. Threatens: R-2, and ADR-0001's interface rule.
- QG-3 is not met by the current code: `tests/check.mos` checks only `System`, not every model, and the code has no asserts that would check behaviour. Threatens: R-3.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
