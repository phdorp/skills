# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No item is lost if the machine crashes mid-write. | 1 | active | A lost item cannot be recovered. |
| R-2 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | It is the product's core function. |
| R-3 | Runs with only the Python standard library. | 3 | active | A constraint on every choice, not a feature. |
| R-4 | A new command touches only `cli.py` and at most one new module. | 4 | active | Keeps later commands cheap to add. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-1 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-2 | QS-2 |
| QG-3 | Flexibility: installability | R-3 | QS-3 |
| QG-4 | Maintainability: modifiability | R-4 | QS-4 |

### Stakeholders

## 2. Constraints

- Runs with only the Python standard library: no third-party packages (R-3).

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs live in [`../adr/`](../adr/). The "Record architecture decisions" ADR is [ADR-0001](../adr/0001-record-architecture-decisions.md), proposed and waiting for the architect's approval.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed during `add` | normal operation, store on a local disk | every add that reported success is present afterwards, and the store opens | 0 acknowledged items lost in 100 kill trials |
| QS-2 | QG-2 | `list --soon N` runs over a generated set of items | normal operation | exactly the items expiring within N days are listed, sorted by expiry | 0 mismatches against a reference computation in 100 generated sets |
| QS-3 | QG-3 | a fresh Python install with no packages runs the tool | `python3 -m pantry` | the tool runs, and the source imports no non-standard package | 0 third-party imports in the source |
| QS-4 | QG-4 | a new command is added | normal development | the change touches `cli.py` and at most one new module, and no other file | 0 other files changed per new command |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
