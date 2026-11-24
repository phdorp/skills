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

*As found, unconfirmed.*

- No module imports a third-party package; `pantry` and `tests` use only the standard library.
- The pantry file path comes from the environment variable `PANTRY_FILE`, defaulting to `~/.pantry.jsonl` (`pantry/store.py`).
- The code uses dataclasses, `date.fromisoformat` and `argparse` subparsers with `required=True`, so it needs Python 3.7 or later. The confirmed floor is 3.9.

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

*As found, unconfirmed.*

- The system boundary is the command line and one local file. The program makes no network calls and reads no other file.
- Only `pantry/store.py` opens the pantry file, reading it and appending to it.
- Dates are calendar dates in local time (`date.today()` in `pantry/dates.py`); there is no time zone.

## 4. Solution strategy

*As found, unconfirmed.*

- The pantry is an append-only event log: `add` and `remove` records are appended to one file (`pantry/store.py`), and the current items are derived by replaying them (`pantry/model.py`, `replay`). This traces to R-2: no record is rewritten in place. It also avoids a database, which fits R-3.
- Only the standard library is used: `argparse`, `json`, `dataclasses`, `datetime`, `pathlib`, `re`, `os`, `unittest` (R-3).
- The command module is thin: it parses arguments and calls the store and the date parser; it holds no storage logic (R-4).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry.__main__` | runs `cli.main` with the command-line arguments and exits with its return code | `pantry.cli` |
| `pantry.cli` | parses the commands, prints results and errors, maps them to exit codes 0, 1 and 2 | `pantry.dates`, `pantry.store`, `pantry.model` |
| `pantry.store` | reads and appends the pantry file, located by `PANTRY_FILE` or the home directory | `pantry.model` |
| `pantry.model` | the `Item` type, the add and remove records, and the replay that derives the current items | standard library (`dataclasses`, `datetime`) |
| `pantry.dates` | parses the date forms users type into a `date` | standard library (`datetime`, `re`) |

`pantry/__init__.py` holds only the package docstring. The tests in `tests/` are not a building block of the product.

## 6. Runtime view

*As found, unconfirmed.*

- **add:** `cli` parses the date with `dates`, then `store.add` appends one add record. The append is flushed and fsynced before the command returns.
- **list:** `store` reads every line of the file and replays the records. `cli` filters by the `--soon` limit if given, sorts by expiry date and then by lower-cased name, and prints one line per item.
- **remove:** `cli` checks the name against the current items and returns exit code 1 if it is absent. Otherwise `store.remove` appends a remove record.

Each command is one process that starts, does its work, and exits.

## 7. Deployment view

*As found, unconfirmed.*

- The program runs as `python3 -m pantry` from a checkout of the repository. There is no installation step; the repository has no packaging file (no `pyproject.toml` or `setup.py`).
- Nothing runs in the background and nothing is deployed to a server. The only persistent state is the pantry file.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Errors:** user errors (a bad date, an unknown item) print `pantry: ...` to stderr and return exit code 1. Bad usage returns exit code 2, as argparse reports it. Successful commands return 0.
- **Dates:** ISO 8601 calendar dates (`YYYY-MM-DD`) in the file and in `list` output; the relative forms are resolved against the local date when the command runs.
- **Persistence format:** one JSON object per line with the keys `op`, `name` and, for add records, `expires`.
- **Damaged lines:** a line that does not parse as JSON is skipped silently when the file is read (`store._records`).
- **Naming:** lowercase `snake_case` for functions and modules; `Item` is a frozen dataclass.
- **Logging:** none.

## 9. Architecture decisions

The ADRs are in [`../adr/`](../adr/). The decision on what is made centrally is in
[ADR-0001, "Record architecture decisions"](../adr/0001-record-architecture-decisions.md),
which is accepted.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL at a random point during `add` or `remove` | normal operation | every acknowledged change is present after restart, and the pantry file reads | 0 lost acknowledged changes and 0 unreadable files in 200 random kill points |
| QS-2 | QG-2 | a fresh checkout is run with no install step | Python 3.9+ on Linux and macOS | the program runs | 0 imports outside the standard library; the test suite passes with nothing installed |
| QS-3 | QG-3 | a developer adds a command | normal development | only `cli.py` and at most one new module change | at most 2 files changed; `store.py`, `model.py` and `dates.py` unchanged |
| QS-4 | QG-4 | the user runs `list --soon N` | normal operation | it shows exactly the items expiring on or before today + N, sorted by expiry | 0 mismatches in the list test cases |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Torn last line loses the next add.** After a crash leaves a partial last line, the next `add` is appended onto it and the new record is skipped on read. Reproduced: an item added after a simulated crash is missing. Threatens R-2 and QG-1.
- **Silent skipping of damaged lines.** `store._records` drops any unparseable line, including one in the middle of the file, with no warning. Threatens QG-1: losses go unnoticed.
- **Directory entry not synced on first write.** The file is fsynced after each append, but the directory is not, so a newly created pantry file may not survive a crash on some filesystems. Not checked here. Threatens R-2.
- **No lock between concurrent runs.** Two commands appending at the same time are not coordinated. Threatens R-2.
- **Names are the item key.** Adding an existing name silently replaces its expiry date. `Milk` and `milk` are different items. Threatens QG-4 if users expect otherwise.
- **Unbounded growth.** The file is never compacted, and every command replays all of it. Harmless under 1,000 items; it becomes a time-behaviour concern only if the volume grows.
- **Crash path untested.** The tests cover a torn last line being skipped, but not an add after a torn line and not a crash between write and fsync. Threatens QS-1's verification.
