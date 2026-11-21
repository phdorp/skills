# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line, with or without hyphens in the ISBN. | 3 | active | Core interface and query path; the rest serves it. |
| R-2 | A crash during any write leaves the catalog either in its prior state or fully updated, never unreadable. | 2 | active | Losing the catalog loses all data. |
| R-3 | Runs with only the Python standard library. | 4 | active | Hard constraint; limits every choice rather than competing with them. Matches ADR 0001. |
| R-4 | Every book is checked for a valid ISBN check digit before it is stored, by any entry point. | 1 | active | A wrong ISBN makes `find` miss the book later (ADR 0002). |
| R-5 | Adding a command changes only `cli.py` and one new module. | 5 | active | Maintainability; cheap to defer, expensive to break later. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-4 | QS-2 |
| QG-3 | Maintainability: modifiability | R-5 | QS-3 |
| QG-4 | Functional suitability: functional completeness | R-1 | QS-4 |
| QG-5 | Flexibility: adaptability | R-3 | QS-5 |

### Stakeholders

## 2. Constraints

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

The three parts of shelf (`cli.py`, `catalog.py`, `isbn.py`) are described in the README: see
[README › How it works](../../README.md#how-it-works).

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs are in [docs/decisions/](../decisions/). The central decisions are recorded in
[0003 Record architecture decisions](../decisions/0003-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the catalog opens and holds either the prior or the new state | 0 unreadable catalogs in 100 kill trials |
| QS-2 | QG-2 | `add` is given an ISBN with a wrong check digit | normal operation | the book is rejected and nothing is stored | 0 stored books with an invalid check digit |
| QS-3 | QG-3 | a new command is added | normal development | only `cli.py` and one new module change | 2 files changed |
| QS-4 | QG-4 | `find` is given an ISBN with or without hyphens | catalog holding books added with hyphenated and plain ISBNs | every matching book is returned | 100% of matches returned in a test catalog |
| QS-5 | QG-5 | shelf is installed and run on Python 3 | fresh machine with no third-party packages | it runs | 0 third-party imports; 0 install steps beyond Python 3 |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
