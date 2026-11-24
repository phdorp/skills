# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 2 | active | The purpose of the tool. |
| R-2 | The catalog survives a crash mid-write. | 1 | active | Losing the catalog is the costliest failure; it sets the write path (ADR-0001). |
| R-3 | Runs with only the Python standard library. | 4 | active | Fixed constraint; see section 2. |
| R-4 | An ISBN is checked before a book is stored. | 3 | active | Keeps `find` trustworthy; decided in ADR-0002. |
| R-5 | Adding a command touches only cli.py and one new module. | 5 | active | Maintainability; sets the module boundaries. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-1, R-4 | QS-2 |
| QG-3 | Maintainability: modifiability | R-5 | QS-3 |

No further ISO/IEC 25010 characteristic is required: asked whether the architect had left one out, they answered that nothing is missing.

### Stakeholders

- Readers: the people who add, list and find books (R-1).

## 2. Constraints

- Standard library only: no third-party packages (R-3).

## 3. Context and scope

- In scope: the command line, and the catalog file (`~/.shelf.json`, or the path in `SHELF_FILE`), as described in the README.
- Out of scope: online ISBN lookup (ADR-0002).

## 4. Solution strategy

## 5. Building block view

See README › How it works: [../../README.md#how-it-works](../../README.md#how-it-works)

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs are in [../decisions/](../decisions/). The decision list is [ADR 0003, Record architecture decisions](../decisions/0003-record-architecture-decisions.md), proposed and awaiting the architect's approval of its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) during `add` | normal operation | the catalog loads with the old books, plus the new one only if the write finished | 0 unreadable catalogs in 100 kill trials |
| QS-2 | QG-2 | `add` is given an invalid ISBN; then each stored book is searched by title and by ISBN | normal operation | the invalid ISBN is refused and not stored; every stored book is found | 0 invalid ISBNs stored; 100% of stored books found in the test set |
| QS-3 | QG-3 | a developer adds a sample subcommand | the current code | only `cli.py` and one new module change | 2 files changed, 0 in `catalog.py` and `isbn.py` |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
