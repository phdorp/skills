# shelf: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 1 | active | The product does nothing without add, list and find. |
| R-2 | The catalog survives a crash mid-write. | 2 | active | A corrupt catalog loses every book. Crash type: the process is killed (see QS-1). |
| R-3 | Runs with only the Python standard library. | 4 | active | A constraint every other decision respects; also in section 2. |
| R-4 | An ISBN is checked before a book is stored. | 3 | active | A wrong ISBN makes `find` miss the book later (ADR 0002). |
| R-5 | Adding a command touches only `cli.py` and one new module, unless it needs a catalog operation that does not exist yet. | 5 | active | A development-time rule; sharpened from the brief, and it conflicts with commands that need a new catalog operation. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-4, R-1 | QS-2 |
| QG-4 | Maintainability: modifiability | R-5 | QS-3 |

Ruled out by the architect (no reason given; the architect answered "nothing is missing" to the
check for these characteristics): Security: confidentiality; Performance efficiency: time
behaviour.

Open, without a measure: portability (adaptability) from R-3. Which Python version and platforms
it must run on is still to be measured. (QG-3 is held open for it.)

### Stakeholders

- **Reader**: the one person who owns the catalog, on one machine.
- **Maintainer**: one person, comfortable with Python's standard library.

## 2. Constraints

- Runs with only the Python standard library: no third-party dependencies (R-3).
- Python 3.10 or later, on Linux and macOS.

## 3. Context and scope

Out of scope for v1:

- online ISBN lookup and any network access (ADR 0002);
- several readers sharing one catalog, and sync between machines;
- editing and removing books (can wait past v1).

Figures: up to 2,000 books now, 10,000 in five years.

## 4. Solution strategy

## 5. Building block view

See [README › How it works](../../README.md#how-it-works) for the three parts (`cli`, `catalog`, `isbn`).

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs are in [docs/decisions/](../decisions/). The
[Record architecture decisions](../decisions/0003-record-architecture-decisions.md) ADR lists
which decisions are made centrally; it is `proposed`.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the catalog is either fully stored in its old or new state, and `list` still opens it | 0 unreadable catalogs in 100 injected kills |
| QS-2 | QG-2 | `add` receives an ISBN with a wrong check digit | normal operation | the book is rejected and nothing is stored | 0 of 1,000 wrong-check-digit ISBNs stored |
| QS-3 | QG-4 | a new command is added | normal operation | only `cli.py` and one new module change, unless the command needs a catalog operation that does not exist yet | the commit's changed-file list has 2 entries |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
