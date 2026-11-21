# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add an item with an expiry date and list the items expiring within N days, from the command line. | 1 | active | Defines the product; shapes the CLI and the store. |
| R-2 | No item whose add or remove succeeded is lost if the machine crashes during a write. | 2 | active | Sets how every write is made durable. |
| R-3 | The tool runs on the Python standard library alone, with no third-party packages. | 3 | active | Rules out third-party dependencies. |
| R-4 | Adding a new command changes only `cli.py` and at most one new module. | 4 | active | Sets the building-block boundaries and the dependency rule. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1 | QS-1 |
| QG-2 | Reliability: recoverability | R-2 | QS-2 |
| QG-3 | Flexibility: installability | R-3 | QS-3 |
| QG-4 | Maintainability: modifiability | R-4 | QS-4 |

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

The ADRs live in `../adr/`. The list of decisions made centrally is in
[0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | after `add` of items with valid dates, `list --soon N` is run | normal operation | the output lists exactly the items whose expiry is on or before today + N, sorted by expiry | 0 mismatches over a test set of items spread across the window |
| QS-2 | QG-2 | the process is killed with SIGKILL at random points during `add` or `remove` | normal operation | every command that exited 0 is present afterwards and no earlier item is lost; the store still opens | 0 lost acknowledged writes in 200 kill trials |
| QS-3 | QG-3 | the tool is run on a clean Python 3 install | normal operation | every command runs | runs every command with 0 non-stdlib packages installed |
| QS-4 | QG-4 | a developer adds a new command | normal operation | the change touches only `cli.py` and at most one new module | 100% of added commands within that limit, checked in review or a test |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
