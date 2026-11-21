# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | Core function; fixes the CLI surface. |
| R-2 | No item is lost if the machine crashes mid-write. | 2 | active | Data loss is the worst failure; fixes durable, append-only storage. |
| R-3 | Runs with only the Python standard library. | 3 | active | Dependency rule that bounds every other choice. |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | Change-locality rule; yields to R-2 if a crash-safety fix needs a second module. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-1 | QS-2 |
| QG-3 | Portability: installability | R-3 | QS-3 |
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

The ADRs live in [`docs/adr/`](../adr/). The list of decisions the architect makes centrally is in [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md) (proposed, awaiting approval; created when confirmed).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add`, and a further `add` then runs | normal operation | the earlier item is either fully stored or absent; the store still opens; the further add is not lost | 0 lost items in 100 kill-during-add trials followed by a further add |
| QS-2 | QG-2 | `list --soon N` is run over a corpus of items with varied expiry dates | normal operation | every item with expiry on or before today + N is listed, sorted by expiry | 0 misses in a test corpus |
| QS-3 | QG-3 | the tool is installed on a clean Python 3 with no pip step | fresh interpreter | every command runs | 0 non-standard-library imports |
| QS-4 | QG-4 | a new command is added | normal development | only `cli.py` and at most one new module change | 0 changes outside `cli.py` and one new module in the next added command |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
