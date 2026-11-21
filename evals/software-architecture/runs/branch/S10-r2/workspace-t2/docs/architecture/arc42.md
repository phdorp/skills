# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over 24 h and output its temperature trajectory. | 1 | active | Fixes the model structure and the simulation output; `System.mo` already does this. |
| R-2 | A room or a controller can be replaced by another variant with the same connectors, without editing `System` or the other block. | 2 | active | Sets the interfaces and the dependency rule. The current `Thermostat.mo` reads `HeatingLib.roomHeatCapacity` directly, which breaks this. |
| R-3 | Every model in HeatingLib passes OpenModelica `checkModel` with no errors. | 3 | active | Sets the testability bar. Room, Thermostat and System pass today; `tests/check.mos` checks only System. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-2 | Flexibility: replaceability | R-2 | QS-1 |
| QG-3 | Maintainability: testability | R-3 | QS-2 |

QG-1 (Functional suitability: functional correctness, from R-1) is open: no measure yet. The
architect has to name the tolerance against the expected temperature curve.

### Stakeholders

### Gap check

Asked about time behaviour, interoperability and safety. The architect left nothing out; no
new requirement came from it.

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

The architecture decisions are recorded as ADRs in [`../adr/`](../adr/). The ADR
"Record architecture decisions" is written once the architect confirms the setup proposal.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a room variant with a different heat capacity is swapped in | normal development | only the swapped block changes; `System` and the controller are untouched | 0 edits to `System` and to the controller |
| QS-2 | QG-3 | `checkModel` runs on every model in the package | normal development, OpenModelica | no errors reported for any model | 0 models with errors |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
