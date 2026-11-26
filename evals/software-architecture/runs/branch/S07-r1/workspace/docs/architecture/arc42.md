# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 1 | active | Core product; fixes the CLI interface. |
| R-2 | A crash during `add` or save leaves the catalog readable, with every earlier book intact and no half-written book. | 2 | active | Lost data is the worst failure. |
| R-3 | Runs with only the Python standard library. | 4 | active | A constraint that holds regardless of other choices. |
| R-4 | A book is stored only if its ISBN passes the check-digit test, whichever command adds it. | 3 | active | Wrong ISBNs make `find` miss books. |
| R-5 | A new command is added by one new module and one registration in `cli.py`; no other file changes. | 5 | active | Maintainability. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-4 | QS-2 |
| QG-3 | Functional suitability: functional completeness | R-1 | QS-3 |
| QG-4 | Maintainability: modifiability | R-5 | QS-4 |
| QG-5 | Flexibility: installability | R-3 | QS-5 |

### Stakeholders

## 2. Constraints

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

See README › How it works: [../../README.md#how-it-works](../../README.md#how-it-works).

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs are in [docs/decisions/](../decisions/). The "Record architecture decisions" ADR is
[0003](../decisions/0003-record-architecture-decisions.md) (status `proposed`).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) during `add` or save | normal operation | the catalog stays readable; every earlier book is intact; the half-written book is absent | 0 unreadable catalogs in 100 SIGKILL trials |
| QS-2 | QG-2 | `add` with an ISBN whose check digit is wrong | normal operation | the command is rejected and nothing is stored | 0 invalid ISBNs stored over 1,000 generated inputs |
| QS-3 | QG-3 | `find` with a title fragment or an ISBN | a test fixture catalog | every matching book is listed | 100% of matches listed on the test fixture |
| QS-4 | QG-4 | a new command is added | normal development | only `cli.py` and one new module change | 2 files changed per new command |
| QS-5 | QG-5 | the tool is run on a clean Python 3 install with no extra packages | a machine with no pip packages | the tool runs with `python3 -m shelf` | 0 third-party imports |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
