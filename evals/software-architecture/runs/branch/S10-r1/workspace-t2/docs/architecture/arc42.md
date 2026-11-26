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

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The decision on what is decided centrally is
[0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a developer replaces `Room` with a variant that has a different heat capacity | development | only the variant's file changes; `Thermostat` and `System` are unchanged | 0 files outside the variant change |
| QS-2 | QG-2 | a developer runs the OpenModelica check on every model in `HeatingLib` | development | every model checks without errors | 0 check errors across all models |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
