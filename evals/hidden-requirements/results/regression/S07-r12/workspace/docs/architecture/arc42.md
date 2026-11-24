# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 1 | active | system-level: the product's core; fixes the `cli` and `catalog` blocks |
| R-2 | The catalog survives a crash mid-write. | 2 | active | system-level: losing the catalog is the costliest failure; shapes storage (ADR-0001) |
| R-3 | Runs with only the Python standard library. | 5 | active | system-level: fixes the third-party dependency rule (ADR-0001) |
| R-4 | An ISBN is checked before a book is stored. | 3 | active | system-level: crosses `cli`, `isbn` and `catalog`; ADR-0002 |
| R-5 | Adding a command touches only cli.py and one new module. | 4 | active | system-level: fixes the module layout and the dependency rule |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-4 | QS-2 |
| QG-3 | Maintainability: modifiability | R-5 | QS-3 |
| QG-4 | Flexibility: installability | R-3 | QS-4 |

### Stakeholders

## 2. Constraints

- Runs with only the Python standard library (R-3).

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

See README › How it works: `../../README.md#how-it-works`.

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs are in `../decisions/`: `0001-store-books-in-one-json-file.md` and `0002-validate-isbn-locally.md`. The ADR "Record architecture decisions" is not written yet; it is proposed for number 0003 and waits for the architect's confirmation.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed during `add` | normal operation | the catalog opens and holds either its state before the write or its state after it | 0 unreadable catalogs in 100 kill trials |
| QS-2 | QG-2 | an `add` with an ISBN whose check digit fails | normal operation | the add is refused with exit code 1 and nothing is stored | 0 stored books with a failing check digit in 1,000 generated inputs |
| QS-3 | QG-3 | a developer adds one command | normal development | the change touches `cli.py` and one new module | 2 files changed |
| QS-4 | QG-4 | the tool runs on a fresh Python 3 with no packages installed | clean environment | all commands run | 0 third-party imports; tests pass in a clean environment |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
