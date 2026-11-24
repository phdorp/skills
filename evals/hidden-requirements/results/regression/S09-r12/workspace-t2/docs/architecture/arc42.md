# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add a pantry item with an expiry date and list the items that expire within N days, from the command line. | 1 | active | The product's purpose; the CLI and the file store exist for it. |
| R-2 | An add or remove that the command acknowledged survives a crash at any point during the write, and the pantry file stays readable. | 2 | active | It decides how the store writes, which is costly to change later. |
| R-3 | The program runs with only the Python standard library; no third-party package is installed. | 3 | active | It limits every later technology choice. |
| R-4 | Adding a command changes only `cli.py` and at most one new module. | 4 | active | It sets the module boundaries. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Maintainability: modifiability | R-4 | QS-3 |
| QG-4 | Functional suitability: functional correctness | R-1 | QS-4 |

### Stakeholders

- The user: one person, using the pantry on one machine.
- The maintainer: one developer, comfortable with Python.

## 2. Constraints

- Only the Python standard library (R-3).
- Runs on Linux and macOS, with Python 3.9 and later.
- No law or contract governs the data. Items are kept until the user removes them.

## 3. Context and scope

Figures:

- One user, one machine, one pantry file (`~/.pantry.jsonl`, or the path in `PANTRY_FILE`).
- Under 1,000 items, with no growth planned beyond that.

Out of scope for the first version:

- Synchronisation between devices.
- Notifications.
- Several users.
- Import from or export to other systems, such as calendars.

Anything beyond R-1 to R-4 is deferred until it is raised as a requirement.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs are in [`../adr/`](../adr/). The decision on what is made centrally is in
[ADR-0001, "Record architecture decisions"](../adr/0001-record-architecture-decisions.md),
which is proposed and waits for the architect's approval.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL at a random point during `add` or `remove` | normal operation | every acknowledged change is present after restart, and the pantry file reads | 0 lost acknowledged changes and 0 unreadable files in 200 random kill points |
| QS-2 | QG-2 | a fresh checkout is run with no install step | Python 3.9+ on Linux and macOS | the program runs | 0 imports outside the standard library; the test suite passes with nothing installed |
| QS-3 | QG-3 | a developer adds a command | normal development | only `cli.py` and at most one new module change | at most 2 files changed; `store.py`, `model.py` and `dates.py` unchanged |
| QS-4 | QG-4 | the user runs `list --soon N` | normal operation | it shows exactly the items expiring on or before today + N, sorted by expiry | 0 mismatches in the list test cases |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
