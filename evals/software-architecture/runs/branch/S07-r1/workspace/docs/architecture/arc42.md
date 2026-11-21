# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 1 | active | The core use; the product does not exist without it. |
| R-2 | The catalog survives a crash mid-write. | 2 | active | Losing the catalog is the costliest failure. |
| R-3 | Runs with only the Python standard library. | 4 | active | A hard limit that rarely competes with the others. |
| R-4 | An ISBN is checked before a book is stored. | 3 | active | A wrong ISBN makes `find` miss the book later. |
| R-5 | Adding a command touches only `cli.py` and one new module. | 5 | active | A development convenience. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-4 | QS-2 |
| QG-3 | Portability: adaptability | R-3 | QS-3 |
| QG-4 | Maintainability: modifiability | R-5 | QS-4 |

R-1 has no quality goal yet: its measure is an open question for the architect.

### Stakeholders

## 2. Constraints

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

See README › How it works: [../../README.md#how-it-works](../../README.md#how-it-works)

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs live in [../decisions/](../decisions/). The "Record architecture decisions" ADR is
[0003, proposed](../decisions/0003-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the catalog file parses and holds either the old or the new list | 0 unreadable catalogs in 100 trials |
| QS-2 | QG-2 | `add` is given an ISBN whose check digit is wrong | normal operation | exit 1 with an error; the catalog file is unchanged | 100% of wrong ISBNs rejected |
| QS-3 | QG-3 | a fresh Python 3 with no packages installed runs `python3 -m shelf list` | a fresh environment | exits 0 | 0 pip installs needed |
| QS-4 | QG-4 | a developer adds a new command | normal development | the change touches only `cli.py` and one new module | at most 2 files changed |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
