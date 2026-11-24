# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | Shapes the command surface and the item model. |
| R-2 | An item that `add` or `remove` reported as done is still there after a crash at any point during the write, and the store still opens. | 2 | active | Shapes storage; the write strategy is a central decision (ADR 0001). |
| R-3 | Runs with only the Python standard library. | 3 | active | Forbids third-party dependencies, a central decision (ADR 0001); also a constraint in section 2. |
| R-4 | Adding a command changes `cli.py` and at most one new module; no existing module changes. | 4 | active | Fixes the building-block boundaries and the dependency rule. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1 | QS-1 |
| QG-2 | Reliability: recoverability | R-2 | QS-2 |
| QG-3 | Maintainability: modifiability | R-4 | QS-3 |

Open, no measure yet (R-3, Portability: installability): the minimum Python version the
measure needs is not confirmed.

Round 1: the architect reports no quality characteristic missing beyond these goals.

### Stakeholders

| name or role | interest |
|---|---|

## 2. Constraints

- Runs with only the Python standard library (R-3).

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The list of decisions the architect makes centrally is the ADR
"Record architecture decisions": [`../adr/0001-record-architecture-decisions.md`](../adr/0001-record-architecture-decisions.md)
(proposed; waiting for the architect's approval of its text).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | `list --soon N` is run on a fixed set of items | normal operation | it shows exactly the items whose expiry is within N days of today | 100 % match on the fixed test set |
| QS-2 | QG-2 | the process is killed with SIGKILL during `add` or `remove` | normal operation | every change reported as done is still there, and the store still opens | 0 lost changes and 0 unreadable stores in 100 kill trials |
| QS-3 | QG-3 | a developer adds a command | normal development | only `cli.py` and at most one new module change | at most 2 files changed per new command; 0 existing modules changed |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
