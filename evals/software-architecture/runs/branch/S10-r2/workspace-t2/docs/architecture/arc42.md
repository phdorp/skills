# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | — |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 3 | active | — |
| R-3 | Every model checks in OpenModelica without errors. | 2 | active | — |

Gap check (confirmed by the architect): no further characteristics are missing.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-2 | Flexibility: replaceability | R-2 | QS-1 |
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

ADRs live in `../adr/`. The list of decisions made centrally is [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md) (status proposed, awaiting the architect's approval of its text).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a replacement `Room` or `Thermostat` variant is substituted in `System` | the rest of the library unchanged | `System` and the other block are unchanged | 0 changed lines outside the replaced block |
| QS-2 | QG-3 | the check script runs over all models in `HeatingLib` | normal project state | each model is reported, and the script exits non-zero on any error | 0 models with errors |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
