# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | core use |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | building variants are compared side by side |
| R-3 | Every model checks and simulates in OpenModelica without errors. | 3 | active | results feed design decisions |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: modifiability | R-1 | QS-1 |
| QG-2 | Flexibility: replaceability | R-2 | QS-2 |
| QG-3 | Reliability: faultlessness | R-3 | QS-3 |

### Stakeholders

| role | expectation |
|---|---|
| Architect (project owner) | decides the architecture; accepts ADRs |
| Modellers | add a room or controller variant without learning the whole library |

## 2. Constraints

- OpenModelica 1.27 or later; no libraries beyond the Modelica language itself.

## 3. Context and scope

## 4. Solution strategy

Blocks exchange signals only through the connectors in `Interfaces`; `System` wires them.

## 5. Building block view

| block | responsibility | may use |
|---|---|---|
| `Interfaces` | connectors and units shared by all blocks | - |
| `Room` | heat balance of the room air | `Interfaces` |
| `Thermostat` | heating power from the measured temperature | `Interfaces` |
| `System` | instantiates and connects the blocks | `Room`, `Thermostat`, `Interfaces` |

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

- Units: SI, declared on every parameter and connector.

## 9. Architecture decisions

Decisions are recorded as ADRs in [docs/adr/](../adr/). What is decided centrally is listed in
[ADR-0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a modeller changes the room's wall model | development | only `Room.mo` changes | 0 other files changed |
| QS-2 | QG-2 | a modeller replaces `Room` with a two-zone room | development | `Thermostat` works unchanged with the new room | 0 changes to `Thermostat.mo` |
| QS-3 | QG-3 | `omc tests/check.mos` runs | any checkout | every model checks | 0 errors |

## 11. Risks and technical debt

## 12. Glossary
