# pantry: architecture

Structured after arc42 (https://arc42.org).

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | core use |
| R-2 | No item is lost if the machine crashes mid-write. | 2 | active | the list must be trusted |
| R-3 | Runs with only the Python standard library. | 3 | active | installs anywhere Python runs |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | commands are added often |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-2 | QS-1 |
| QG-2 | Maintainability: modifiability | R-4 | QS-2 |


## 2. Constraints

*As found, unconfirmed.*

- Python standard library only (R-3).

## 3. Context and scope

*As found, unconfirmed.*

One user at a command line; one local file, `~/.pantry.jsonl` (`PANTRY_FILE`).

## 4. Solution strategy

*As found, unconfirmed.*

Every change is appended to a JSON Lines file and synced with `fsync`; the item list is replayed from it.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `cli` | parses commands, prints, sets exit codes 0/1/2 | `store`, `dates`, `model` |
| `store` | appends and replays records | `model` |
| `model` | `Item` and the replay of records | - |
| `dates` | parses typed dates (`+3d`) | - |

## 6. Runtime view

*As found, unconfirmed.*

`pantry add` parses the date, builds an `Item`, `store` appends one line and syncs it.

## 7. Deployment view

*As found, unconfirmed.*

Runs where Python 3 runs; no install step.

## 8. Crosscutting concepts

Errors go to stderr; exit 0 success, 1 user error, 2 bad usage.

## 9. Architecture decisions

Decisions are recorded as ADRs in [docs/adr/](../adr/).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | power is cut during `pantry add` | normal operation | every earlier item is still listed | 0 lost items in 100 trials |
| QS-2 | QG-2 | a developer adds a `rename` command | current code | only cli.py and one new module change | 2 files changed at most |


## 11. Risks and technical debt

*As found, unconfirmed.*

- Two processes appending at once are not locked against each other.

## 12. Glossary

No glossary yet.
