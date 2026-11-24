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

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in `../adr/`. The list of decisions made centrally is the ADR
[0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md), proposed
and waiting for the architect's approval of its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a new room variant is added | normal development | only the new variant and the system composition change | 0 existing blocks edited |
| QS-2 | QG-3 | any model is changed | normal development | the full check runs over every model | 0 check errors across all models in one run |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
