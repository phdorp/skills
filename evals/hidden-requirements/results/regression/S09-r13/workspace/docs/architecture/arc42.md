# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | |
| R-2 | No item is lost if the machine crashes mid-write. | 1 | active | |
| R-3 | Runs with only the Python standard library. | 3 | active | |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Maintainability: modifiability | R-4 | QS-2 |

Open, without a measure yet (not goals until the architect gives one):

- Flexibility: adaptability, from R-3. What would show it is met? On which Python versions and operating systems must it run?
- Functional suitability: functional correctness, from R-1. What would show it is met? Should `list --soon` include items already past their expiry date?

Ruled out by the architect, no reason given: Security: confidentiality; Performance efficiency: time behaviour.

### Stakeholders

## 2. Constraints

- Runs with only the Python standard library (R-3).

*As found, unconfirmed.*

- Items are kept in a local file: `PANTRY_FILE`, or `~/.pantry.jsonl` by default (README; `pantry/store.py`).
- Tests run with `python3 -m unittest` (README).

## 3. Context and scope

*As found, unconfirmed.*

pantry is a command-line program that one person runs in a terminal. It reads and writes one
local file and talks to no other system: the code uses no sockets, no network and no subprocess.

| partner | exchanged with pantry |
|---|---|
| the user, in a terminal | commands and arguments in; item lines and error messages out |
| the local file (`PANTRY_FILE` or `~/.pantry.jsonl`) | JSON records, read and appended |
| the Python 3 runtime | the program is started as `python3 -m pantry` |

## 4. Solution strategy

*As found, unconfirmed.*

- The state is an append-only log of add and remove records, replayed on each read; no file is
  rewritten (QG-1, R-2; ADR 0002).
- Each record is fsynced as it is written, and unreadable lines are skipped on read (QG-1, R-2;
  ADR 0003). This does not yet meet R-2; see section 11.
- The code is split by concern: the CLI, file access, records and replay, date parsing. A new
  read-only command can stay in `cli.py` (QG-2, R-4; ADR 0006).
- Only the standard library is used (R-3; ADR 0007).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry/__main__.py` | entry point: runs `cli.main` with the arguments and exits with its code | `cli` |
| `pantry/cli.py` | argument parsing, the commands `add`, `list`, `remove`, their output and exit codes | `store`, `dates`, `model` |
| `pantry/store.py` | the file: its path, appending records, reading them and skipping unreadable lines | `model` |
| `pantry/model.py` | the `Item` and the record kinds; replay of records into items; no file access | none in pantry |
| `pantry/dates.py` | parsing of date input; no file access | none in pantry |
| `pantry/__init__.py` | package docstring only | none |

The tests in `tests/test_pantry.py` use `cli`, `store`, `dates` and `model`. They are not a building block of the product.

## 6. Runtime view

*As found, unconfirmed.*

- `add NAME EXPIRES`: `cli` reads the date with `dates.parse`, builds an `Item` and calls
  `store.add`, which appends one add record and fsyncs it. Exit 0.
- `remove NAME`: `cli` reads all items (`store.items`, which replays the file) and checks the name.
  If it is there, `store.remove` appends one remove record. Exit 0. Otherwise exit 1.
- `list [--soon DAYS]`: `cli` replays the items, sorts them by expiry and then name, keeps those
  expiring on or before today plus DAYS if given, and prints one line per item. Exit 0.

## 7. Deployment view

*As found, unconfirmed.*

The program runs from the source tree with `python3 -m pantry`. The repository has no packaging
metadata (no `pyproject.toml`, `setup.py` or `setup.cfg`), so no installed artifact exists. The
data file is on the user's own machine.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Dates:** calendar dates in ISO format (`YYYY-MM-DD`), with no time and no zone; "today" is the
  machine's local date (ADR 0008).
- **Errors:** a user error prints `pantry: <message>` to stderr and exits 1; bad usage exits 2 with
  argparse's message (ADR 0004).
- **Unreadable data:** lines that do not parse are skipped silently (ADR 0003).
- **Persistence:** append-only, with an fsync after each record (ADR 0002, ADR 0003).
- **Names:** items are identified by their exact name, which is case-sensitive; the list sorts by
  name ignoring case.
- **Logging:** none.

## 9. Architecture decisions

ADRs live in `../adr/`. The list of decisions made centrally is in
[0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL at a random point during `add` or `remove` | normal operation | every add or remove that reported success is in the store, and the store still opens | 0 acknowledged items lost in 100 kill trials |
| QS-2 | QG-2 | a new command is added | the existing code base | only `cli.py` and at most one new module change | 0 other files changed across the next 3 commands added |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Torn line, then a lost record (R-2, QG-1).** After a crash leaves a cut line without a newline,
  the next `add` is written onto that line, and both are lost. Reproduced on 2026-11-24. The test
  suite does not cover an append after a torn line, so it passes. Decision: ADR 0003.
- **Duplicate name silently replaces (R-1).** Adding a name that already exists replaces its expiry
  without a warning: a second `Milk` makes the first disappear. Reproduced on 2026-11-24. No
  decision covers this yet.
- **Record-changing commands strain R-4 (QG-2).** Such a command needs a new record kind in
  `model.py` and changes in `store.py`, beyond `cli.py`. Decision: ADR 0006.
- **Expired items in `list --soon` (R-1).** They are included today. The architect has not decided
  whether they belong (Q11). Decision: ADR 0005.
- **Unbounded growth (technical debt).** The file is never compacted and every command reads all of
  it, so start-up slows as it grows. The architect ruled out time behaviour, so this is debt, not a
  breached goal. Decision: ADR 0002.
- **No lock between processes (R-2).** Two commands running at once are not guarded against each
  other. Small appends usually do not interleave, but nothing in the code guarantees it.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
