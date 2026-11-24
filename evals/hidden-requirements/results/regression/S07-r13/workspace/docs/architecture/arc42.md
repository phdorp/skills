# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 3 | active | the core function |
| R-2 | The catalog survives a crash mid-write. | 1 | active | data loss cannot be undone |
| R-3 | Runs with only the Python standard library. | 5 | active | no third-party dependencies |
| R-4 | An ISBN is checked before a book is stored. | 2 | active | already decided in ADR 0002 |
| R-5 | Adding a command touches only cli.py and one new module. | 4 | active | keeps command additions contained |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-4 | QS-2 |
| QG-3 | Maintainability: modifiability | R-5 | QS-3 |
| QG-4 | Flexibility: installability | R-3 | QS-4 |

Open, without a measure yet (not goals): functional completeness of find (R-1), and whether a power cut counts as a crash for R-2.

### Stakeholders

- Readers: the people who add, list and find books (R-1).

## 2. Constraints

- Runs with only the Python standard library (R-3).

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

The parts as they are today are described in [README › How it works](../../README.md#how-it-works).

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The decisions made so far are in [docs/decisions/](../decisions/). The "Record architecture decisions" ADR is [0003](../decisions/0003-record-architecture-decisions.md), proposed and awaiting the architect's approval.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the catalog is either the old or the new list, and it opens | 0 unreadable catalogs in 100 kill trials |
| QS-2 | QG-2 | `add` is given an ISBN with a wrong check digit | normal operation | the book is refused and nothing is stored | 0 bad-check-digit ISBNs stored across the test set |
| QS-3 | QG-3 | a developer adds a command | normal operation | the change is confined to cli.py and one new module | 0 files changed outside those two |
| QS-4 | QG-4 | the tool is run on a fresh Python 3 install | normal operation | it runs with no package installation | 0 third-party imports |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
