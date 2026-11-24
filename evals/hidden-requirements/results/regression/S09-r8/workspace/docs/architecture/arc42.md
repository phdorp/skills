# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No item is lost if the machine crashes mid-write. | 1 | active | A lost item cannot be recovered. |
| R-2 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | It is the product's core function. |
| R-3 | Runs with only the Python standard library. | 3 | active | A constraint on every choice, not a feature. |
| R-4 | A new command touches only `cli.py` and at most one new module. | 4 | active | Keeps later commands cheap to add. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-1 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-2 | QS-2 |
| QG-3 | Flexibility: installability | R-3 | QS-3 |
| QG-4 | Maintainability: modifiability | R-4 | QS-4 |

### Stakeholders

## 2. Constraints

- Runs with only the Python standard library: no third-party packages (R-3).

*As found, unconfirmed.*

- Python 3 only: the code uses `date.fromisoformat`, dataclasses and f-strings (Python 3.7 or newer). The minimum version is an open question (not confirmed).
- Data is a plain-text JSON-lines file in the user's home directory (`~/.pantry.jsonl`), overridable with `PANTRY_FILE`. See ADR-0002 (proposed).

## 3. Context and scope

*As found, unconfirmed.*

- One user runs the command-line tool on one machine, from a shell (`python3 -m pantry <command>`).
- The only external system is the local file at `PANTRY_FILE` or `~/.pantry.jsonl`. Nothing is sent over a network.
- Commands: `add NAME EXPIRES`, `list [--soon DAYS]`, `remove NAME`.

## 4. Solution strategy

*As found, unconfirmed.*

- **Append-only log, replayed on read** (QG-1). Every `add` and `remove` appends one record and is flushed and fsynced. The current state is rebuilt by replaying the file, so a crash can only lose the record being written.
- **Thin CLI over small modules** (QG-4). `cli` dispatches commands; `dates` parses user input; `store` does file I/O; `model` defines items and replay.
- **Standard library only** (QG-3): `argparse`, `json`, `pathlib`, `datetime`, `dataclasses`, `unittest`.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry/__main__.py` | entry point for `python3 -m pantry`; passes arguments to `cli.main` and exits with its code | `cli` |
| `pantry/cli.py` | parses the `add`, `list` and `remove` commands, reports user errors, prints results | `dates`, `store`, `model` |
| `pantry/dates.py` | parses dates as users type them: ISO dates, `today`, `tomorrow`, `+Nd`, `+Nw` | nothing internal |
| `pantry/store.py` | the pantry file: appends records, reads and skips unparseable lines | `model` |
| `pantry/model.py` | the `Item` type, record shapes, and `replay` (current items from records) | nothing internal |
| `pantry/__init__.py` | package docstring only | nothing |
| `tests/` | `unittest` tests of dates, store and cli behaviour | `cli`, `dates`, `store`, `model` |

## 6. Runtime view

*As found, unconfirmed.*

- **`add NAME EXPIRES`:** `cli` parses the date with `dates.parse`. On failure it prints `pantry: not a date` to stderr and exits 1. Otherwise `store.add` appends one `add` record, flushes and fsyncs, and `cli` exits 0.
- **`remove NAME`:** `cli` reads the current items with `store.items`. If the name is absent it prints `pantry: no such item` and exits 1. Otherwise `store.remove` appends a `remove` record.
- **`list [--soon DAYS]`:** `store.items` reads the file, skipping lines that do not parse, and `model.replay` returns the current items. `cli` sorts them by expiry, then name, filters by the limit if given, and prints `date  name` lines.

## 7. Deployment view

*As found, unconfirmed.*

- A local Python 3 process, run with `python3 -m pantry` from the project directory. There is no server, no service and no build step.
- The data file is `PANTRY_FILE` if set, otherwise `~/.pantry.jsonl`.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Exit codes:** 0 success, 1 user error (bad date, unknown item), 2 bad usage. Errors go to stderr with the prefix `pantry:` (ADR-0004, proposed).
- **Dates:** the store keeps ISO dates (`YYYY-MM-DD`). Users may type relative forms; `+Nd` is days and `+Nw` is weeks. `list --soon DAYS` counts days from today.
- **Encoding:** the file is UTF-8.
- **Records:** JSON objects with `op` (`add` or `remove`), `name` and, for `add`, `expires`.
- **Naming:** lower-case module names; no logging.

## 9. Architecture decisions

The ADRs live in [`../adr/`](../adr/). The "Record architecture decisions" ADR is [ADR-0001](../adr/0001-record-architecture-decisions.md), accepted 2026-11-24.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed during `add` | normal operation, store on a local disk | every add that reported success is present afterwards, and the store opens | 0 acknowledged items lost in 100 kill trials |
| QS-2 | QG-2 | `list --soon N` runs over a generated set of items | normal operation | exactly the items expiring within N days are listed, sorted by expiry | 0 mismatches against a reference computation in 100 generated sets |
| QS-3 | QG-3 | a fresh Python install with no packages runs the tool | `python3 -m pantry` | the tool runs, and the source imports no non-standard package | 0 third-party imports in the source |
| QS-4 | QG-4 | a new command is added | normal development | the change touches `cli.py` and at most one new module, and no other file | 0 other files changed per new command |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **R-1 is not met (lost item after a crash).** A torn last line is skipped on read, but the next `add` is appended onto it, so both records end up on one line and the new item is lost (reproduced). `tests/test_pantry.py` does not cover an add after the tear. Threatens R-1 and QS-1. The fix may change the record format, so it waits for ADR-0002.
- **Unparseable lines are skipped silently.** Corruption anywhere in the file, not only at the end, drops records without a message. Threatens R-1.
- **Durability of a new file is unverified.** The first `add` creates the file. The code fsyncs the file but not its directory, so on some file systems a power loss right after the first add could lose the entry. Threatens R-1 under power loss, which Q3 has not settled.
- **No format version.** The records carry no version field, so a future format change cannot be told apart from today's. Open decision on the ADR-0001 list.
- **Duplicate names replace silently.** `add` with an existing name overwrites its date with no message. Q4 is open; this is current behaviour, not a confirmed rule.
- **Whole file read on every command.** `store.items` reads and replays the full file each time. Fine at the volumes assumed so far (Q2 is open); no requirement sets a limit.
- **Test isolation.** `tests/test_pantry.py` sets `PANTRY_FILE` in `os.environ` without restoring it, so tests share global state.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
