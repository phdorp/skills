# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No item the pantry has accepted is lost or made unreadable when the machine crashes or the process is killed during a write. | 1 | active | Data loss is the costliest failure, and it constrains the storage. |
| R-2 | Users add an item with a name and an expiry date (ISO date, `today`, `tomorrow`, `+Nd`, `+Nw`), list the items that expire within N days, and remove an item, from the command line. | 2 | active | The core function. |
| R-3 | The program runs on Python 3 with no third-party packages installed. | 3 | active | A mandated technology choice that limits every other decision. |
| R-4 | Adding a command changes only `cli.py` and at most one new module. | 4 | active | Modifiability of the dependency structure. |

The R-IDs follow the confirmed rank. The brief's numbering was 1 add/list, 2 crash safety,
3 standard library, 4 new command; that is R-2, R-1, R-3, R-4 here.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-1 | QS-1 |
| QG-2 | Maintainability: modifiability | R-4 | QS-2 |
| QG-3 | Portability: adaptability | R-3 | QS-3 |

Not a goal, by the architect's confirmation that nothing is missing: time behaviour. The
architect's reason is not stated.

Open, without a measure: Functional suitability: functional correctness (from R-2). The
measure is the item-set size and the window N that count as proof.

### Stakeholders

- The household member who uses the pantry from the command line on a personal computer.
- The maintainer who builds and maintains the code. Who, and with which skills, is not yet
  confirmed.

## 2. Constraints

- Python standard library only; no third-party packages (R-3).
- Python 3.9 or later.
- Runs on any operating system where Python 3 runs. No hosting, and no licence beyond the
  project's own.
- The data stays on the user's machine until removed: `~/.pantry.jsonl`, overridable with
  `PANTRY_FILE`. No law or contract applies.

## 3. Context and scope

- In scope: one household, one personal computer, up to a few hundred items.
- Out of scope: sync between machines, notifications, a GUI, multi-user access.
- External interfaces: none. No other program reads the pantry file.

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The "Record architecture decisions" ADR is
[0001](../adr/0001-record-architecture-decisions.md) (proposed; awaiting the architect's approval).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) during `add` or `remove` | normal operation, with items already stored | every item added before the failure is still listed and the store still opens | 0 lost or unreadable items in 100 kill trials |
| QS-2 | QG-2 | a developer adds a command | design and implementation | the change is confined to `cli.py` and at most one new module | 0 changed files outside those two, checked on the commit that adds a command |
| QS-3 | QG-3 | a fresh Python 3.9 install with no packages beyond the standard library | normal operation | every command runs | 0 third-party imports |

## 11. Risks and technical debt

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
