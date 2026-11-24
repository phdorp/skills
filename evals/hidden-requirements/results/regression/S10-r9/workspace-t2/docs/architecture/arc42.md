# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | The system simulates one room heated by a thermostat for 24 h and gives the room temperature over that time. | 1 | active | the function the library exists for |
| R-2 | A room model or a controller model can be replaced by another variant with the same connectors; only the wiring in `System` changes. | 3 | active | a design property; it can follow R-1 and R-3 |
| R-3 | Every model in `HeatingLib` passes an OpenModelica check with no errors. | 2 | active | the check every other requirement is verified against |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: modifiability | R-2 | QS-1 |
| QG-2 | Maintainability: testability | R-3 | QS-2 |

### Stakeholders

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

The ADRs are kept in [`docs/adr/`](../adr/). The "Record architecture decisions" ADR is
[ADR-0001](../adr/0001-record-architecture-decisions.md), status `proposed`: it waits for the
architect's approval of its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a developer adds a room variant with the same connectors as `Room` | normal development | only the variant file and the wiring in `System` change | 0 lines changed in `Thermostat` and `Interfaces` |
| QS-2 | QG-2 | a check runs over every model in `HeatingLib` | normal development | each model reports no error | 0 failing models out of every model in the package |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
