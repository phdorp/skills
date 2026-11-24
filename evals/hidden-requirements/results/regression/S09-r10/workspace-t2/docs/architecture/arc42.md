# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | The core job; the record format and the CLI follow from it. |
| R-2 | No item is lost if the machine crashes mid-write. | 2 | active | Dictates how writes are made durable; costly to change later. |
| R-3 | Runs with only the Python standard library. | 3 | active | A dependency rule for the whole build. |
| R-4 | A new command touches only `cli.py` and at most one new module. | 4 | active | Fixes the module boundaries. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-2 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Maintainability: modifiability | R-4 | QS-3 |

### Figures

- Under 500 items at once; growth of the file is acceptable for years, with no compaction in the first version.
- Privacy: the file is readable only by its owner. No R-ID backs this or the figure below, so neither is a quality goal.
- `list` answers within 1 s for 10,000 records. No R-ID backs this figure, so it is not a quality goal.

### Stakeholders

- Household members: under five people, sharing one file on one machine.
- Maintainer: one developer who knows Python.

## 2. Constraints

- Runs locally on the user's machine; no hosting, no running cost.
- Linux and macOS; Python 3.8 or newer.
- Holds item names and dates only, kept until removed; no law or contract applies.
- The existing file `~/.pantry.jsonl` stays readable after any change.

## 3. Context and scope

- Out of scope: network access, sync between machines, reminders and notifications.
- Nothing outside the system is exchanged with: output is plain text on stdout, and the only file is the pantry file.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

The ADRs live in `../adr/`. The list of decisions made centrally is [ADR 0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md), proposed and waiting for the architect's approval of its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) or power is cut during `add` | normal operation | every acknowledged item is in the store, a half-written add is absent, and the store still opens | 0 acknowledged items missing and 0 unreadable stores in 100 kill trials |
| QS-2 | QG-2 | the tool is installed on a machine with a stock Python 3 | normal operation | the tool runs with no install step and no third-party import | runs with no install step; a test finds no third-party import |
| QS-3 | QG-3 | a new command is added | normal operation | the change touches only `cli.py` and at most one new module | 0 other files changed in review |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
