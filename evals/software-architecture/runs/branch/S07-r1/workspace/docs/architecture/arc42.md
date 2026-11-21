# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 3 | active | The product's purpose; it fixes the building blocks (cli, catalog, isbn). |
| R-2 | The catalog survives a crash mid-write. | 1 | active | Lost data is irreversible; ADR 0001 writes a temporary file and renames it. |
| R-3 | Runs with only the Python standard library. | 5 | active | Mandated technology; checked by the import list. |
| R-4 | An ISBN is checked before a book is stored. | 2 | active | Wrong ISBNs make `find` miss books later; ADR 0002. |
| R-5 | Adding a command touches only cli.py and one new module. | 4 | active | Shapes the module structure. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-4 | QS-2 |
| QG-3 | Flexibility: installability | R-3 | QS-3 |
| QG-4 | Maintainability: modifiability | R-5 | QS-4 |

### Stakeholders

## 2. Constraints

Only the Python standard library may be used (R-3).

## 3. Context and scope

The command line and the catalog file (`~/.shelf.json`, or the path in `SHELF_FILE`) are described in [README › How it works](../../README.md#how-it-works).

## 4. Solution strategy

The catalog is one JSON file: [ADR 0001](../decisions/0001-store-books-in-one-json-file.md). ISBNs are checked locally: [ADR 0002](../decisions/0002-validate-isbn-locally.md).

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

The parts as they are today are described in [README › How it works](../../README.md#how-it-works).

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The decision records are in [docs/decisions/](../decisions/). The ADR [3. Record architecture decisions](../decisions/0003-record-architecture-decisions.md) (proposed) defines which decisions are made centrally.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the catalog loads with either the old or the new book list, never a partial one | 0 unreadable catalogs in 100 kill trials |
| QS-2 | QG-2 | `add` is given an ISBN with a wrong check digit | normal operation | the book is rejected with exit code 1 and nothing is stored | 0 stored from a fixed set of 1000 wrong-check-digit ISBNs |
| QS-3 | QG-3 | a clean Python 3 install with no pip packages runs `python3 -m shelf list` | clean environment | the command runs | 0 non-standard-library imports, 0 install steps |
| QS-4 | QG-4 | a dummy command is added | development | only cli.py and one new module change | 2 files changed |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
