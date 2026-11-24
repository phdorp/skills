# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | The core job; every other requirement protects it. |
| R-2 | No item is lost if the machine crashes mid-write. | 2 | active | Losing data is the costliest failure for a tool that holds the owner's food stock. |
| R-3 | Runs with only the Python standard library. | 4 | active | A constraint more than a trade-off; standard-library durability is possible alongside R-2. |
| R-4 | A new command touches only cli.py and at most one new module. | 3 | active | Shapes the building-block structure and every later change. |

Tie-break R-2 vs R-4 (confirmed by the ranking): R-2 is kept when only one of the two can be
fully met.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-3 | Flexibility: installability | R-3 | QS-1 |
| QG-4 | Maintainability: modifiability | R-4 | QS-2 |

Open, without a measure yet: a goal for R-1 (functional correctness) and a goal for R-2
(recoverability). They are not written as goals until the architect gives a measure.

Ruled out: confidentiality beyond the operating system's default file permissions. The
architect's reason: the item file holds the owner's own food stock, and default permissions
are enough; no encryption.

### Stakeholders

- Owner and sole user: uses the command line on a personal computer, and maintains the code.

## 2. Constraints

- Runs on Linux and macOS with Python 3.9 or newer.
- Uses only the Python standard library; no third-party packages (R-3).
- No hosting and no cost beyond the owner's own machine.

## 3. Context and scope

Out of scope for the first version: synchronisation between devices, reminders or
notifications, quantities, categories, export, and exchange with other systems or people.

Figures: under 1,000 items; a file of a few hundred KB after five years of use; one person.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

Decisions are recorded as ADRs in [`../adr/`](../adr/). The list of decisions made centrally is in [Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-3 | a fresh checkout is run with Python 3.9 or newer | a machine with only the standard library available | the CLI runs with no install step beyond the checkout | 0 imports outside the standard library |
| QS-2 | QG-4 | a commit adds a new command | normal development | the commit changes `cli.py` and at most one new module | 0 commits that change more than `cli.py` plus one new module |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
