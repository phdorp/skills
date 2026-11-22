# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 1 | active | core use; fixes the split into `cli`, `catalog` and `isbn` |
| R-2 | The catalog survives a crash mid-write. | 2 | active | storage write strategy; ADR-0001 relies on temp file and rename |
| R-3 | Runs with only the Python standard library. | 4 | active | third-party dependency rule |
| R-4 | An ISBN is checked before a book is stored. | 3 | active | data integrity; decided by ADR-0002 |
| R-5 | Adding a command touches only cli.py and one new module. | 5 | active | modifiability and interface rule |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Functional suitability: functional correctness | R-4 | QS-3 |
| QG-5 | Maintainability: modifiability | R-5 | QS-4 |

### Stakeholders

## 2. Constraints

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

The parts of the system are described in [README › How it works](../../README.md#how-it-works).

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs are in [docs/decisions/](../decisions/). The "Record architecture decisions" ADR, which
draws the line between central and block-level decisions, is
[ADR 0003](../decisions/0003-record-architecture-decisions.md) (proposed).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the book is either fully stored or absent; the catalog still loads | 0 unreadable catalogs in 100 trials |
| QS-2 | QG-2 | the program is run on a clean Python 3 install | no packages installed beyond the standard library | it runs with `python3 -m shelf` with no install step | 0 third-party packages required |
| QS-3 | QG-3 | `add` is called with an ISBN whose check digit is wrong | normal operation | the book is rejected before it is stored; nothing is written | 100% of wrong check digits rejected in the test set |
| QS-4 | QG-5 | a new command is added | normal operation | the change touches only `cli.py` and one new module | 0 files changed besides `cli.py` and one new module |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
