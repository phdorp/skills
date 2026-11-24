# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | Shapes the command surface and the item model. |
| R-2 | An item that `add` or `remove` reported as done is still there after a crash at any point during the write, and the store still opens. | 2 | active | Shapes storage; the write strategy is a central decision (ADR 0001). |
| R-3 | Runs with only the Python standard library. | 3 | active | Forbids third-party dependencies, a central decision (ADR 0001); also a constraint in section 2. |
| R-4 | Adding a command changes `cli.py` and at most one new module; no existing module changes. | 4 | active | Fixes the building-block boundaries and the dependency rule. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1 | QS-1 |
| QG-2 | Reliability: recoverability | R-2 | QS-2 |
| QG-3 | Maintainability: modifiability | R-4 | QS-3 |

Open, no measure yet (R-3, Portability: installability): the minimum Python version the
measure needs is not confirmed.

Round 1: the architect reports no quality characteristic missing beyond these goals.

### Stakeholders

| name or role | interest |
|---|---|

## 2. Constraints

- Runs with only the Python standard library (R-3).

*As found, unconfirmed.*

- The pantry file is the only storage: `PANTRY_FILE`, or `~/.pantry.jsonl` (`pantry/store.py`).
- Python 3: the code uses f-strings and `date.fromisoformat`; no minimum version is stated.

## 3. Context and scope

*As found, unconfirmed.*

The system is a local command run from a terminal (`python3 -m pantry`). It talks to:

- the user's terminal: arguments in, output on stdout, errors on stderr;
- the local file at `PANTRY_FILE`, or `~/.pantry.jsonl`;
- the system clock (`date.today()`), for relative dates and the "soon" window.

Nothing else: no network, no other programs or services.

## 4. Solution strategy

*As found, unconfirmed.*

- **Append-only log.** Every change is one JSON record appended to the file; the items are the
  result of replaying the records in order. Serves R-2 (QG-2). Its gap is in section 11.
- **Thin command layer over pure modules.** `cli` parses arguments and prints; `model` and
  `dates` do no file I/O. Serves R-4 (QG-3): a new command is a new branch in `cli` plus, at
  most, one module.
- **Dates fixed on input.** Relative dates (`+3d`, `tomorrow`) become absolute dates when typed,
  so the file never holds a relative date. Serves R-1 (QG-1).
- **Standard library only.** Serves R-3.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry/__main__.py` | entry point for `python3 -m pantry`: passes the arguments to `cli` and exits with its code | `cli` |
| `pantry/cli.py` | the commands `add`, `list`, `remove`: argument parsing, messages, exit codes | `dates`, `store`, `model` |
| `pantry/dates.py` | turns typed dates (`2026-11-25`, `today`, `tomorrow`, `+3d`, `+2w`) into dates | none |
| `pantry/model.py` | `Item`, the add and remove records, and replaying records into the items left | none |
| `pantry/store.py` | the pantry file: its path, appending records, reading them back, skipping unreadable lines | `model` |
| `pantry/__init__.py` | package docstring only | none |

The `may use` column is what the code does today; ADR 0003 covers it.

## 6. Runtime view

*As found, unconfirmed.*

- **`add NAME DATE`:** `cli` parses the date with `dates`, builds an `Item`, and `store` appends
  its record. Exit 0. An unparsable date exits 1 and writes nothing.
- **`remove NAME`:** `cli` checks that the name is among the items, then `store` appends a
  remove record. Exit 1 if there is no such item.
- **`list [--soon DAYS]`:** `store` reads every record, `model` replays them, and `cli` sorts by
  expiry then name and prints `DATE  NAME`. With `--soon`, it keeps the items expiring on or
  before today plus DAYS.
- **A crash during `add` or `remove`:** see section 11, risk 1.

## 7. Deployment view

*As found, unconfirmed.*

Run from the source tree with `python3 -m pantry`. The repository has no packaging file (no
`pyproject.toml` or `setup.py`), so there is no install step. Each user's data lives in one file:
`PANTRY_FILE`, or `~/.pantry.jsonl`.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Errors:** a user error prints `pantry: <message>` to stderr and exits 1; bad usage exits 2
  (argparse); `--help` exits 0.
- **Storage format:** one JSON object per line. `add` records have the keys `op`, `name` and
  `expires` (an ISO date); `remove` records have `op` and `name`.
- **Dates:** stored as ISO dates (`YYYY-MM-DD`). Relative forms are resolved on input and never
  stored.
- **Names:** an item is identified by its exact name. Adding a name that exists replaces its
  expiry, with no message; `remove` deletes by exact name. Sorting ignores case.
- **Unreadable lines:** `store.py` skips them without a message.
- **Configuration:** the `PANTRY_FILE` environment variable overrides the file path.
- **Tests:** `unittest` in `tests/test_pantry.py`; the tests point `PANTRY_FILE` at a temporary
  directory. Test layout is not on the ADR 0001 list: arc42 only.

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The list of decisions the architect makes centrally is the ADR
"Record architecture decisions": [`../adr/0001-record-architecture-decisions.md`](../adr/0001-record-architecture-decisions.md)
(accepted 2026-11-24).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | `list --soon N` is run on a fixed set of items | normal operation | it shows exactly the items whose expiry is within N days of today | 100 % match on the fixed test set |
| QS-2 | QG-2 | the process is killed with SIGKILL during `add` or `remove` | normal operation | every change reported as done is still there, and the store still opens | 0 lost changes and 0 unreadable stores in 100 kill trials |
| QS-3 | QG-3 | a developer adds a command | normal development | only `cli.py` and at most one new module change | at most 2 files changed per new command; 0 existing modules changed |

## 11. Risks and technical debt

*As found, unconfirmed.*

1. **A write after a torn line loses the new item (threatens R-2, QS-2).** A crash mid-write can
   leave a line without its newline. The next `add` or `remove` is appended onto that line, so
   the change is unreadable and silently skipped. Reproduced: `add Milk` exited 0 and `list`
   did not show it. The tests do not cover this.
2. **The new file's directory entry is not synced (threatens R-2).** `store.py` fsyncs the file,
   not its directory, so after a power loss the file created by the first `add` may be missing.
   Read from the code, not reproduced.
3. **Unreadable lines are skipped silently (threatens R-2).** Any unparsable line is dropped
   without a message, not only a torn last line, so a loss is invisible. Reproduced with a
   garbage line in the file.
4. **The file only grows (debt).** Every `add` and `remove` appends, nothing compacts the file,
   and every command reads all of it. Not measured; a concern only as the list grows.
5. **Adding an existing name replaces its expiry (debt).** Reproduced: two `add Milk` commands
   left one Milk with the later date. R-1 does not say what should happen.
6. **No packaging metadata (debt).** Without `pyproject.toml`, the tool runs only from the
   source tree; tests run with `python3 -m unittest` from the root.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
