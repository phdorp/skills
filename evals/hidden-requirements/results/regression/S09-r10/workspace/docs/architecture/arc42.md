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

*As found, unconfirmed.*

- No Python version or platform is declared in the repository; the code uses `dataclasses` and `date.fromisoformat`, so it needs Python 3.7 or newer.
- No packaging metadata (no `pyproject.toml`, `setup.py` or requirements file).

## 3. Context and scope

- Out of scope: network access, sync between machines, reminders and notifications.
- Nothing outside the system is exchanged with: output is plain text on stdout, and the only file is the pantry file.

*As found, unconfirmed.*

- The system is entered through its command line (`python3 -m pantry <command>`) and reads and writes one file: `PANTRY_FILE` if set, otherwise `~/.pantry.jsonl`.

## 4. Solution strategy

*As found, unconfirmed.*

- The pantry is an append-only log: every add or remove is one appended record, and the current items are computed by replaying the log. Each append is flushed and fsynced before the command returns (QG-1, R-2).
- The log is plain text, one JSON object per line, readable without the tool (R-1).
- Only the standard library is used, and each module has one job (R-3, QG-2, QG-3).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry/__main__.py` | entry point for `python3 -m pantry`: passes the arguments to `cli` and exits with its code | `cli` |
| `pantry/cli.py` | the commands `add`, `list` and `remove`: argument parsing, user messages, exit codes | `dates`, `store`, `model` |
| `pantry/dates.py` | parses dates as users type them: `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`, `+Nw` | none |
| `pantry/store.py` | the pantry file: appends records, reads them back, and replays them into items | `model` |
| `pantry/model.py` | `Item`, the `add` and `remove` records, and the replay of records into items | none |
| `pantry/__init__.py` | the package docstring only | none |

The tests in `tests/` use `cli`, `dates`, `store` and `model`; they are not a block of the product.

## 6. Runtime view

*As found, unconfirmed.*

- `add NAME EXPIRES`: `cli` parses the date with `dates`; an unparseable date prints `pantry: not a date` to stderr and exits 1. Otherwise `store` appends one add record, flushes and fsyncs it, and the command exits 0.
- `remove NAME`: `cli` replays the store to check that the name exists; if not, it prints `pantry: no such item` and exits 1. Otherwise `store` appends one remove record and the command exits 0.
- `list [--soon DAYS]`: `store` replays the whole file into items; with `--soon`, items expiring after today plus DAYS are dropped; the rest are sorted by expiry date, then by name ignoring case, and printed as `YYYY-MM-DD  NAME`. The command exits 0.

## 7. Deployment view

*As found, unconfirmed.*

- Runs as a local Python process: `python3 -m pantry` from the project directory. The repository declares no installation.
- Data lives in one local file, `PANTRY_FILE` or `~/.pantry.jsonl`.
- Tests run with `python3 -m unittest`.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Errors:** a user error prints `pantry: <message>` to stderr and exits 1; bad usage is reported by argparse and exits 2. Lines in the file that do not parse are skipped silently on read.
- **Dates:** calendar dates in ISO 8601; `dates.parse` takes an optional `today` so tests can fix the date.
- **Record format:** one JSON object per line. An add record has the keys `op` (`"add"`), `name` and `expires`; a remove record has `op` (`"remove"`) and `name`.
- **Identity:** an item is identified by its name, compared case-sensitively. A later add with the same name replaces the earlier item.
- **Configuration:** the environment variable `PANTRY_FILE` overrides the file path.
- **Logging:** none.

## 9. Architecture decisions

The ADRs live in `../adr/`. The list of decisions made centrally is [ADR 0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md), accepted 2026-11-24.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) or power is cut during `add` | normal operation | every acknowledged item is in the store, a half-written add is absent, and the store still opens | 0 acknowledged items missing and 0 unreadable stores in 100 kill trials |
| QS-2 | QG-2 | the tool is installed on a machine with a stock Python 3 | normal operation | the tool runs with no install step and no third-party import | runs with no install step; a test finds no third-party import |
| QS-3 | QG-3 | a new command is added | normal operation | the change touches only `cli.py` and at most one new module | 0 other files changed in review |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Torn last line:** if a crash leaves a cut-off last line, the next `add` is appended onto it, and that record is then unparseable and skipped, so the new item is silently lost. Reproduced by running the code. Threatens R-2 (QS-1).
- **New file not made durable:** the first write creates the file, but the directory entry is never fsynced, so after a crash the file may be missing although `add` returned. Found by reading; not reproduced. Threatens R-2 (QS-1).
- **Damage in the middle is silent:** any unparseable line is skipped without a warning, so lost records are not reported. Threatens R-2.
- **Unbounded growth:** the file is never compacted and each command reads all of it. Threatens the `list` time figure and the item volume figure over the years.
- **Name as identity:** `Milk` and `milk` are two items, and a second `add` with an existing name silently replaces the first. Threatens R-1 correctness, which is still an open question.
- **Test isolation:** the tests set `PANTRY_FILE` in `os.environ` and never restore it. Threatens the maintainability of the tests (QG-3).
