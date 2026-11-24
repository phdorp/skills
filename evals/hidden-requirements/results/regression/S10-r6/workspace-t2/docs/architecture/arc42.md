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

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs are in [`../adr/`](../adr/). The rule for which decisions the architect makes centrally is in [0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md), written once the architect confirms its list.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a variant of `Room` or `Thermostat` with the same connectors is added to replace the existing block | development | only the new variant file is added; `System` and the other block are unchanged and `System` still checks | 0 existing files changed outside the variant file |
| QS-2 | QG-3 | a developer changes any model and runs `tests/check.mos` | development with OpenModelica | the check covers every model class and fails the run if any of them reports an error | 0 errors across all model classes |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
