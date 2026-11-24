# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | — |
| R-2 | No item is lost if the machine crashes mid-write. | 2 | active | — |
| R-3 | Runs with only the Python standard library. | 3 | active | — |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | — |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-3 | Maintainability: modularity | R-4 | QS-1 |

Open, without a measure yet: R-1 (functional correctness) and R-2 (reliability: recoverability).

### Stakeholders

- The owner: one person, using one machine, who records and lists their own pantry.
- The maintainer: one person, comfortable with Python, with no budget constraint.

## 2. Constraints

- Standard library only; no third-party packages (R-3).
- Python 3.9 or newer.
- Linux and macOS.
- The data holds item names and dates only, kept on the user's machine until they remove the item. No law or contract applies.

## 3. Context and scope

Out of scope for v1: sync between machines, a GUI, reminders, barcode scanning, and data exchange with other systems.

Figures: up to about 1,000 items, now and in a few years.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in `../adr/`. The decision on what is made centrally is recorded in [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md) (status `proposed`, awaiting your approval).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-3 | a developer adds a new command (source: developer; artifact: the pantry package) | the current module layout: cli, dates, store, model | the change is confined to cli.py and at most one new module | 0 edits outside cli.py and one new module for a trial command |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
