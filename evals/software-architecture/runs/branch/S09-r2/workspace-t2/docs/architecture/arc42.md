# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | It is the product's purpose and fixes the storage and CLI shape. |
| R-2 | No item is lost if the machine crashes mid-write. | 1 | active | It decides how every write is made durable. |
| R-3 | Runs with only the Python standard library. | 3 | active | It limits every block's dependencies. |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | It sets the module structure and the dependency rule. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Maintainability: modifiability | R-4 | QS-2 |
| QG-3 | Flexibility: installability | R-3 | QS-3 |
| QG-4 | Functional suitability: functional correctness | R-1 | QS-4 |

### Stakeholders

## 2. Constraints

## 3. Context and scope

### Out of scope

Confirmed by the architect as not wanted:

- protecting the pantry file from other users on the machine (confidentiality);
- list speed for large files (time behaviour);
- importing or exporting the pantry, such as to CSV (interoperability);
- interactive confirmation before `remove` (user error protection); errors are reported with exit codes and messages only.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The ADR [Record architecture decisions](../adr/0001-record-architecture-decisions.md) is `proposed` and waits for the architect's approval of its text.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the interrupted item is either fully stored or absent; items stored before the crash stay readable | 0 acknowledged items lost in 100 SIGKILL trials during `add` |
| QS-2 | QG-2 | a new command is added to the CLI | normal operation | the change touches `cli.py` and at most one new module | a new command's diff touches only `cli.py` and at most one new module |
| QS-3 | QG-3 | the tool is run on a fresh Python 3 install with no pip | normal operation | the tool runs with no install step | 0 non-standard-library imports |
| QS-4 | QG-4 | `list --soon DAYS` is run against items with mixed expiry dates | normal operation | every item expiring within DAYS is listed, none later, sorted by expiry | every item expiring within N days is listed, none later, sorted by expiry |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
