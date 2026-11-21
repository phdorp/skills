# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 1 | active | Core function; the product has no purpose without it. |
| R-2 | The catalog survives a crash mid-write. | 2 | active | Losing or corrupting the catalog is the worst failure. |
| R-3 | An ISBN is checked before a book is stored. | 3 | active | A wrong ISBN makes `find` miss the book later (ADR 0002). |
| R-4 | Adding a command touches only `cli.py` and one new module. | 4 | active | Keeps new commands cheap to add. |
| R-5 | Runs with only the Python standard library. | 5 | active | A mandated technology choice; a constraint more than a priority. |

Conflicts under the confirmed order: R-3 vs R-4 (where the ISBN check lives) and R-2 vs R-4
(whether a new command may write the file itself). Read from the rank, R-2 and R-3 come before
R-4 in both pairs; the architect has not answered the pairwise tie-breaker questions in words.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional completeness | R-1 | QS-1 |
| QG-2 | Reliability: recoverability | R-2 | QS-2 |
| QG-3 | Functional suitability: functional correctness | R-3 | QS-3 |
| QG-4 | Maintainability: modifiability | R-4 | QS-4 |
| QG-5 | Flexibility: installability | R-5 | QS-5 |

### Stakeholders

## 2. Constraints

## 3. Context and scope

See [README › How it works](../../README.md#how-it-works).

## 4. Solution strategy

See [ADR 0001: Store books in one JSON file](../decisions/0001-store-books-in-one-json-file.md) and
[ADR 0002: Validate ISBNs locally](../decisions/0002-validate-isbn-locally.md).

## 5. Building block view

See [README › How it works](../../README.md#how-it-works).

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in [docs/decisions/](../decisions/). The list of
decisions made centrally is in
[ADR 0003: Record architecture decisions](../decisions/0003-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a reader runs `add`, `list` or `find` with a title or an ISBN | normal operation | the book is listed, or found by its title (case-insensitive substring) or its ISBN | 100% of books in the test set are found by title and by ISBN |
| QS-2 | QG-2 | the process is killed with SIGKILL during `add` | normal operation | the book is either fully stored or absent; the catalog still loads | 0 unreadable catalog files in 100 trials |
| QS-3 | QG-3 | a reader adds a book with an ISBN whose check digit is wrong | normal operation | the book is not stored and the reader is told the ISBN is invalid | 0 stored books with a failing check digit, across all entry points |
| QS-4 | QG-4 | a developer adds a command | normal operation | only `cli.py` and one new module change | at most 2 files changed per new command |
| QS-5 | QG-5 | the test suite runs on a clean Python 3 install | normal operation | the suite runs without installing any package | 0 failing tests; 0 packages installed beyond the standard library |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
