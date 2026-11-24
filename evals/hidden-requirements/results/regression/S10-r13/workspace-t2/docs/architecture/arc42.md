# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | Purpose of the library; shapes the simulation model. |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | Most architecture-shaping: fixes the connectors and what each block may depend on. |
| R-3 | Every model checks in OpenModelica without errors. | 3 | active | A gate every model must pass; a convention for all blocks. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: modifiability | R-2 | QS-1 |
| QG-2 | Maintainability: testability | R-3 | QS-2 |

Open, without a measure yet: Functional suitability: functional completeness (from R-1).
Open question: what would show R-1 is met (which temperature accuracy or range counts as
correct, and what "show" means).

### Stakeholders

- Modellers: the users of the library, a handful of people, who run OpenModelica.
- Maintainer: one person who knows Modelica and OpenModelica and builds and maintains the library.

## 2. Constraints

- Open-source tooling only; no commercial tools or licences.
- Runs wherever OpenModelica runs.

## 3. Context and scope

- First version: one room, one thermostat, a one-day simulation, and a plot of the temperature.
- No external systems in the first version: no FMU export, no data files, no exchange with other tools.
- Out of scope (non-goals): real-time and hardware-in-the-loop use; a custom GUI beyond what OpenModelica provides.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in `docs/adr/`. The "Record architecture decisions" ADR is [ADR-0001](../adr/0001-record-architecture-decisions.md), status `proposed`, waiting for the architect's approval of its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a new room or controller variant is added | the library as it is today | only the new variant's file is added; no existing block is changed | 0 existing files edited |
| QS-2 | QG-2 | any model in the library is changed | normal development | every model is checked with OpenModelica | 0 errors |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
