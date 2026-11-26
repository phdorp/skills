# HeatingLib: architecture

Structured after arc42 (https://arc42.org).

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | core use |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | variants are compared |
| R-3 | Every model checks in OpenModelica without errors. | 3 | active | results feed design decisions |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Flexibility: replaceability | R-2 | QS-1 |
| QG-2 | Reliability: faultlessness | R-3 | QS-2 |


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

Decisions are recorded as ADRs in [docs/adr/](../adr/).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a modeller swaps in a second room model | current library | only System changes | 1 model changed |
| QS-2 | QG-2 | `omc tests/check.mos` runs | OpenModelica 1.27 | every model checks | 0 errors |


## 11. Risks and technical debt



## 12. Glossary

No glossary yet.
