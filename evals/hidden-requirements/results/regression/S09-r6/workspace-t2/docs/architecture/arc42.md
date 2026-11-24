# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | Core use of the product. |
| R-2 | No item is lost if the machine crashes mid-write. | 1 | active | Decides how data is stored and written; the other rows depend on the data being trustworthy. |
| R-3 | A new command touches only `cli.py` and at most one new module. | 3 | active | Sets the module boundary and the dependency rule. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-1 | QS-2 |
| QG-3 | Maintainability: modifiability | R-3 | QS-3 |

### Stakeholders

- The pantry owner: the one person who adds, lists and removes items, on one machine from a terminal.
- The architect: owns the requirements, goals and architecture decisions.

## 2. Constraints

- Python standard library only; no third-party packages.
- Runs on Linux and macOS with Python 3.10 or newer.
- No network access.
- Items are kept in a local file: `~/.pantry.jsonl`, overridable with `PANTRY_FILE`.

## 3. Context and scope

Out of scope:

- network access, accounts and cloud sync;
- editing items, quantities, and reminders or notifications (may come later; not part of the first version).

Figures: a few hundred items, one user, one machine.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs are in [`../adr/`](../adr/). The "Record architecture decisions" ADR is [`0001-record-architecture-decisions.md`](../adr/0001-record-architecture-decisions.md), proposed and waiting for the architect's approval.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` or `remove` | normal operation | every add that returned success is still listed and the file reads without error | 0 lost acknowledged adds and 0 unreadable files in 100 kill trials |
| QS-2 | QG-2 | `list --soon N` runs on generated item sets | normal operation | it shows exactly the items expiring within N days from today, sorted by expiry | 0 mismatches over 1000 generated item sets |
| QS-3 | QG-3 | a new command is added | normal operation | the change touches only `cli.py` and at most one new module | 0 changed files outside `cli.py` and one new module |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
