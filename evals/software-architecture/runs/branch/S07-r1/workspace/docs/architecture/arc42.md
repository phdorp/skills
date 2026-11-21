# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 1 | active | The core use; it defines the cli / catalog / isbn split. |
| R-2 | The catalog survives a crash mid-write. | 2 | active | Losing the catalog is the worst failure. |
| R-3 | Runs with only the Python standard library. | 4 | active | A constraint on how it is built; ADR 0001 relies on it. |
| R-4 | An ISBN is checked before a book is stored. | 3 | active | A wrong ISBN makes `find` miss the book later; ADR 0002. |
| R-5 | Adding a command touches only cli.py and one new module. | 5 | active | A constraint on extension (modifiability). |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional correctness | R-4 | QS-2 |
| QG-3 | Flexibility: installability | R-3 | QS-3 |
| QG-4 | Maintainability: modifiability | R-5 | QS-4 |

### Stakeholders

## 2. Constraints

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

See README › [How it works](../../README.md#how-it-works).

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs live in [docs/decisions/](../decisions/). The
[Record architecture decisions](../decisions/0003-record-architecture-decisions.md) ADR is
proposed and waits for the architect's approval of its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) during `add` | normal operation | the catalog either has the old or the new content, and still opens | 0 unreadable catalogs in 100 trials |
| QS-2 | QG-2 | `add` is given a malformed ISBN | normal operation | the add is refused with an error; nothing is stored | 0 invalid ISBNs stored in a fixed set of 100 malformed ISBNs |
| QS-3 | QG-3 | the tests and the CLI are run on a fresh Python 3 install | no third-party packages installed | the tests pass and the CLI runs | all tests pass with 0 third-party packages installed |
| QS-4 | QG-4 | a sample new command is added | normal development | the change touches only cli.py and one new module | the diff touches only cli.py and one new module |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
