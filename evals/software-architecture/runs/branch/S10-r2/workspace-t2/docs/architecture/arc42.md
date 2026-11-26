# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | A 24 h simulation of the heated room yields the room temperature over time, in a form a user can plot. | 1 | active | The purpose of the library; the rest serves it. |
| R-2 | A room or thermostat variant replaces another with the same connectors, and only that block and its instance declaration change. | 2 | active | Sets the block boundaries and the dependency rule; violated today by `Thermostat` reading `roomHeatCapacity`. |
| R-3 | `checkModel` reports no error for every model class in HeatingLib, run by `omc tests/check.mos`. | 3 | active | Already largely met; cheap to enforce for every model. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-2 | Maintainability: modularity | R-2 | QS-1 |
| QG-3 | Maintainability: testability | R-3 | QS-2 |

QG-1 (Functional suitability: functional correctness, from R-1) is open: no measure is confirmed yet.

### Stakeholders

### Gap review

Asked at setup whether anything is missing for performance efficiency (time behaviour),
compatibility (interoperability) and safety (fail safe). The architect answered no to each;
no requirement was added.

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

Architecture decisions are recorded as ADRs in [`docs/adr/`](../adr/). The rule for which decisions
need one is in [0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a developer replaces `Room` with a variant of another heat capacity | the current library | only the variant and its declaration in `System` change; `Thermostat` is unchanged | 0 edited lines in `Thermostat.mo` and `Interfaces.mo` |
| QS-2 | QG-3 | a developer runs `omc tests/check.mos` after a change | the current library; OpenModelica version open | every model class checks without error and the run exits 0 | 0 check errors across the model classes (3 today: `Room`, `Thermostat`, `System`) |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
