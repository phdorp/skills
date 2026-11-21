# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 1 | active | Defines the product; implemented in `cli.py`. |
| R-2 | A crash during a write leaves the previous or the new catalog, never a corrupt one. | 2 | active | A corrupt catalog is the costliest failure; see ADR 0001. |
| R-3 | Runs with only the Python standard library. | 4 | active | Consistent with ADR 0001; no third-party dependency. |
| R-4 | A book is stored only if its ISBN has a valid check digit. | 3 | active | Wrong ISBNs make `find` miss books later; see ADR 0002. |
| R-5 | Adding a command touches only `cli.py` and one new module. | 5 | active | Modifiability. Whether a storage change counts is still open. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional completeness | R-1 | QS-1 |
| QG-2 | Reliability: recoverability | R-2 | QS-2 |
| QG-3 | Functional suitability: functional correctness | R-4 | QS-3 |
| QG-4 | Flexibility: installability | R-3 | QS-4 |

R-5 has no quality goal yet: its measure depends on whether a storage change counts as one
of the two files, which the architect has not decided.

### Stakeholders

## 2. Constraints

## 3. Context and scope

The system boundary and the file it keeps outside itself are described in
[README › How it works](../../README.md#how-it-works).

## 4. Solution strategy

The catalog is one JSON file, written through a temporary file and renamed into place. See
[ADR 0001](../decisions/0001-store-books-in-one-json-file.md).

## 5. Building block view

The three parts (`cli`, `catalog`, `isbn`) are described in
[README › How it works](../../README.md#how-it-works).

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in [docs/decisions/](../decisions/). The ADR
[Record architecture decisions](../decisions/0003-record-architecture-decisions.md) (proposed)
lists which decisions are made centrally.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a reader runs `add`, `list`, `find` by title and `find` by ISBN | normal operation | each command returns the expected books | each passes its acceptance test |
| QS-2 | QG-2 | the process is killed with SIGKILL during `add` | normal operation | the catalog is readable and holds either the old or the new state | 0 unreadable catalogs in 100 trials |
| QS-3 | QG-3 | `add` is given an ISBN whose check digit is wrong | normal operation | the book is rejected and nothing is stored | 0 invalid ISBNs stored in the acceptance tests |
| QS-4 | QG-4 | the tool is installed and run on a clean Python | a Python installation with only the standard library | it runs without installing anything | 0 non-stdlib imports |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
