# shelf: architecture

Structured after arc42 (https://arc42.org).

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Readers add, list and find books by title or ISBN from the command line. | 1 | active | core use |
| R-2 | The catalog survives a crash mid-write. | 2 | active | the list is irreplaceable |
| R-3 | Runs with only the Python standard library. | 3 | active | easy install |
| R-4 | An ISBN is checked before a book is stored. | 4 | active | wrong ISBNs break find |
| R-5 | Adding a command touches only cli.py and one new module. | 5 | active | easy to extend |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-2 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Maintainability: modifiability | R-5 | QS-3 |


## 2. Constraints



## 3. Context and scope



## 4. Solution strategy



## 5. Building block view

The building blocks are described in [README › How it works](../../README.md#how-it-works).

## 6. Runtime view



## 7. Deployment view



## 8. Crosscutting concepts



## 9. Architecture decisions

Decisions are ADRs in [docs/decisions/](../decisions/); what is decided centrally is in ADR-0003.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed during `add` | normal operation | the catalog is old or new, never torn | 0 unreadable catalogs in 100 trials |
| QS-2 | QG-2 | a reader runs `python3 -m shelf list` | Python 3.11, nothing installed | it works | 0 install steps |
| QS-3 | QG-3 | a contributor adds a command | development | only cli.py and one new module change | 0 other files changed |


## 11. Risks and technical debt



## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
