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

## 3. Context and scope

- Out of scope for version 1: several rooms, humidity, real-time or hardware-in-the-loop operation, and a time-varying outdoor temperature (the outdoor temperature is constant at 0 °C).
- Outside the system: nothing. It keeps no data, exchanges nothing beyond its result files, and no law or contract applies.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Decisions are recorded as ADRs in [docs/adr/](../adr/). The line between centrally made and
local decisions is drawn in [0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md)
(status `proposed`, pending the architect's approval).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | `HeatingLib.System` is simulated for 86 400 s from a room at 15 °C, with the set point at 20 °C and the outdoor temperature constant at 0 °C | normal operation | the room temperature reaches the set point and stays within the tolerance | the room temperature after 24 h is within 0.5 K of 20 °C |
| QS-2 | QG-2 | a variant of `Room` or `Thermostat` replaces the original | normal development | only the variant's file and one line in `System` change; no other block changes | 1 model file and 1 `System` line changed; 0 lines changed in other blocks |
| QS-3 | QG-3 | the whole package is checked with one command | normal development | every model passes `checkModel` and `simulate` | 0 errors and 0 warnings across all models in the package |

## 11. Risks and technical debt

- QG-1 is not met by the current code: the room settles at about 13 °C against the 20 °C set point (proportional-only control leaves a steady-state offset of about 7 K).
- QG-2 is not met by the current code: `Room` and `Thermostat` both read `HeatingLib.roomHeatCapacity` from the package, and `System` names both parts concretely with no `replaceable`.
- QG-3 is not met by the current code: `tests/check.mos` checks only `System`, not every model.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
