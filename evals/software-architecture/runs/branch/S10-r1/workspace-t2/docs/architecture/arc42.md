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

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in `../adr/` (that is, `docs/adr/`). The ADR that records the line between central and local decisions is [0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md); it is `proposed` until the architect approves its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-2 | QG-2 | a Room or Thermostat variant with the same connectors replaces the original | a swap test in the project | only the variant's file changes; the other blocks behave as before | 0 files changed outside the swapped block in a swap test |
| QS-3 | QG-3 | `checkModel` is run on every model of HeatingLib | OpenModelica, the project's version | each model reports success with no error | 100% of models pass (4 of 4 today; `tests/check.mos` covers only `System`) |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
