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

*As found, unconfirmed.*

- The program reads and writes only the pantry file, at the path from `PANTRY_FILE` or the
  home directory. It makes no network calls.

## 3. Context and scope

- In scope: one household, one personal computer, up to a few hundred items.
- Out of scope: sync between machines, notifications, a GUI, multi-user access.
- External interfaces: none. No other program reads the pantry file.

*As found, unconfirmed.*

- The user runs the command in a terminal. The only thing the program touches outside itself
  is the pantry file.

## 4. Solution strategy

*As found, unconfirmed.*

- The pantry is an append-only log of add and remove records, replayed on every read (R-1,
  QG-1; [ADR-0002](../adr/0002-append-only-event-log.md)).
- Each append is flushed and fsynced before the command returns (R-1, QG-1).
- Pure logic lives in `model` and `dates`; file I/O only in `store`; parsing and output only in
  `cli` (R-4, QG-2).
- Only the standard library is used (R-3, QG-3; [ADR-0006](../adr/0006-standard-library-only.md)).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `__main__` | entry point for `python3 -m pantry`: passes the arguments to `cli.main` and exits with its code | `cli` |
| `cli` | command parsing, dispatch, output and exit codes for `add`, `list` and `remove` | `dates`, `store`, `model` |
| `dates` | turns the user's date text (ISO date, `today`, `tomorrow`, `+Nd`, `+Nw`) into a date | none |
| `store` | the pantry file: appends records, reads lines, skips lines that are not JSON, and replays the state | `model` |
| `model` | the `Item` and the add and remove records; replays records into the current items | none |

`tests/` is not a block. It uses `cli`, `dates`, `store` and `model` through their public
functions.

## 6. Runtime view

*As found, unconfirmed.*

- **add:** `cli` parses the arguments, then `dates.parse` (on failure: stderr, exit 1), then
  `store.add` appends one JSON line and fsyncs it. Exit 0. An add whose name already exists is
  not checked: on replay the later record wins, so the earlier expiry date is replaced.
- **list:** `store.items` reads every line, skips those that are not JSON, and `model.replay`
  builds the items. `cli` sorts by expiry, then name ignoring case, filters with `--soon DAYS`
  against today's date, and prints `date  name` per item.
- **remove:** `cli` reads the items to check the name exists (exit 1 if not), then appends a
  remove record. Nothing guards against two commands running at once.

## 7. Deployment view

*As found, unconfirmed.*

The program runs from the source tree as `python3 -m pantry`. There is no packaging file and no
install step.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Errors:** user errors print `pantry: <message>` to stderr and exit 1. Bad command-line usage
  exits 2 (argparse prints the usage).
- **Records:** one JSON object per line, UTF-8. An `add` record has `op`, `name` and `expires`
  (ISO date); a `remove` record has `op` and `name`. Names are matched exactly, case included.
- **Dates:** relative dates (`today`, `tomorrow`, `+Nd`, `+Nw`) are computed from the machine's
  local date when the command runs.
- **Durability:** every append is fsynced. The directory entry is not fsynced when the file is
  first created.

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The "Record architecture decisions" ADR is
[0001](../adr/0001-record-architecture-decisions.md) (accepted 2026-11-24).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) during `add` or `remove` | normal operation, with items already stored | every item added before the failure is still listed and the store still opens | 0 lost or unreadable items in 100 kill trials |
| QS-2 | QG-2 | a developer adds a command | design and implementation | the change is confined to `cli.py` and at most one new module | 0 changed files outside those two, checked on the commit that adds a command |
| QS-3 | QG-3 | a fresh Python 3.9 install with no packages beyond the standard library | normal operation | every command runs | 0 third-party imports |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **A torn write makes the next add vanish (R-1, QG-1).** After a partial last line, the next
  record is appended onto it, so the whole line is skipped and `add` still reports success.
  Reproduced in a temporary file. The test suite does not cover appending after a tear, so it
  passes.
- **Unreadable lines are skipped silently (R-1).** A corrupt line in the middle of the file loses
  nothing visible and reports nothing. Reproduced.
- **A valid JSON line with missing fields stops every command (QS-1).** `model.replay` raises
  `KeyError` on a record without `expires`, so `list` fails until the file is repaired by hand.
  Reproduced.
- **A new file's directory entry is not fsynced (R-1).** After a crash in the first write, the
  file may not exist. Untested.
- **Adding an existing name replaces its date silently (R-2).** Reproduced; the user is not told.
- **`remove` checks, then appends, without a lock (R-1).** Two commands at once can interleave.
  Not tested.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
