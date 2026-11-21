# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | The library simulates one room heated by a thermostat over 24 h (86400 s) and makes the room temperature trace available as a result. | 1 | active | Shapes `System`, `Room` and `Thermostat` and the run length. |
| R-2 | Every class in HeatingLib passes `checkModel` in OpenModelica with no errors. | 2 | active | A library-wide quality bar on every change. |
| R-3 | A room or a controller can be replaced by another model with the same connectors, and only the `System` declaration that names it changes. | 3 | active | Extensibility the code only partly supports today: `Thermostat` reads `HeatingLib.roomHeatCapacity` directly. |

Gap check at setup: time behaviour, interoperability of the output format, and functional
completeness were asked about. The architect named no further requirement.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: testability | R-2 | QS-1 |
| QG-2 | Flexibility: replaceability | R-3 | QS-2 |

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

ADRs live in `docs/adr/`. The [Record architecture decisions](../adr/0001-record-architecture-decisions.md)
ADR (`0001`, status `proposed`) lists the decisions made centrally.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a change to any class is submitted | normal development, before merge | every class in HeatingLib is checked with `checkModel`; a class that fails is reported | 100% of the library's classes pass `checkModel` with no errors |
| QS-2 | QG-2 | a room variant with a different heat capacity replaces `Room` | normal development | only `System.mo` changes; the controller gain follows the replaced room's capacity | 0 lines changed outside `System.mo`; controller gain equals the replaced room's C / tau |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
