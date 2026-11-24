# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No item is lost if the machine crashes mid-write. | 1 | active | System-level: it decides the storage design, the costliest part to change later. |
| R-2 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | System-level: it fixes the command-line interface and the expiry-date model. |
| R-3 | A new command touches only cli.py and at most one new module. | 3 | active | System-level: it sets the dependency rule between the building blocks. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-1 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-2 | QS-2 |
| QG-3 | Maintainability: modifiability | R-3 | QS-3 |

Not a goal: Security (confidentiality). The architect's answer to the "did you leave out" question: nothing is missing.

Open, without a measure, so no goal yet: Portability (adaptability), from the standard-library constraint in section 2. Which Python versions and operating systems must it run on with no install step?

### Stakeholders

## 2. Constraints

- Runs with only the Python standard library, with no third-party dependencies. Stated by the architect as a requirement; it bounds the solution, so it is a constraint and has no R-row.

*As found, unconfirmed.*

- Requires Python 3.7 or newer: the code uses `dataclasses` and `date.fromisoformat`. No version is declared anywhere in the repository.
- The pantry is one local file: `PANTRY_FILE` if set, otherwise `~/.pantry.jsonl`.

## 3. Context and scope

*As found, unconfirmed.*

The system is a single-user command-line program on one machine. Its surroundings are the file system (the pantry file), the environment variable `PANTRY_FILE`, the home directory, the system clock (`date.today()`), and the terminal (arguments, standard output, standard error). It talks to no network service and no other system.

## 4. Solution strategy

*As found, unconfirmed.*

- Every change is appended as one record, and the current pantry is recomputed by replaying the records in order. This serves R-1 and QG-1 (ADRs 0002 and 0003).
- Date parsing and replay are pure functions with no file access (`dates.parse` takes `today`; `model.replay` takes records), so they are tested without touching the disk. This serves QG-3.
- Only the standard library is used, as stated in section 2.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry/__main__.py` (entry point) | runs `cli.main` with the arguments and exits with its return code | cli |
| `pantry/cli.py` | parses the commands, calls the other blocks, prints output, chooses the exit code | dates, store, model |
| `pantry/dates.py` | turns the user's date text into a date | standard library |
| `pantry/model.py` | the `Item` value, the add and remove records, and replaying records into items | standard library |
| `pantry/store.py` | reads the pantry file and appends records to it | model, standard library |
| `tests/` | unit tests for all blocks | all blocks |

## 6. Runtime view

*As found, unconfirmed.*

- **add:** `cli.main` parses the arguments, `dates.parse` turns the date text into a date, and `store.add` appends one record through `_append`, which writes, flushes and fsyncs before returning success.
- **list --soon N:** `store.items` reads the whole file, skipping any line that does not parse, and `model.replay` builds the current items. `cli` sorts them by expiry date and then by lowercase name, keeps those expiring by today plus N days, and prints them.
- **remove:** `cli` checks that the name is in the current items, exits with 1 if it is not, and otherwise `store.remove` appends a remove record.

## 7. Deployment view

*As found, unconfirmed.*

The program runs from the source tree as `python3 -m pantry`. The repository has no packaging file and no install step, and no service runs in the background. Each user's data is one file in their home directory (or at `PANTRY_FILE`).

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Errors:** user errors print a `pantry:` message on standard error and exit with 1; bad usage exits with 2 (ADR 0006).
- **Dates:** calendar days only, with no time or zone; relative dates resolve against the local date (ADR 0007).
- **Persistence:** one JSON object per line, with dates as ISO strings; each write is flushed and fsynced (ADRs 0002 and 0003).
- **Logging:** none.
- **Tests:** `unittest` in `tests/`. Each test sets `PANTRY_FILE` to a temporary file.

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in `../adr/`. The ADR [0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md) lists which decisions are made centrally.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the machine crashes or the process is killed while `add` or `remove` writes | normal operation | every item whose command returned success is still listed, and the pantry file still reads | 0 lost items and 0 unreadable files in 100 kill-during-write trials |
| QS-2 | QG-2 | the user runs `list --soon N` | normal operation | exactly the items expiring by today plus N days are listed, earliest first | 0 mismatches against a reference list over 1,000 random item sets |
| QS-3 | QG-3 | a developer adds one read-only command | the current code | only cli.py and at most one new module change | at most 2 files changed in a reference change |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Risk: a new item is lost after a crash.** When a crash leaves a partial last line with no newline, the next `add` or `remove` is written onto that same line, so `_records` skips it and the command still reports success. Checked by running the code in a scratch file; the test suite covers only reading a torn line. Threatens QS-1 (QG-1).
- **Risk: damaged lines are skipped silently.** `_records` skips any line that fails to parse, anywhere in the file, with no warning, so a damaged line in the middle hides items. By reading the code. Threatens QS-1 (QG-1).
- **Risk: concurrent commands can interleave.** There is no lock, so two commands appending at the same time can produce interleaved lines. By reading the code; not tested. Threatens QS-1 (QG-1).
- **Risk: a new file can be lost on a crash.** The file is fsynced, but its directory entry is not, so a crash soon after the first `add` may lose the file. By reading the code; not tested. Threatens QS-1 (QG-1).
- **Risk: a new storage operation spreads across blocks.** A new record kind (a rename, say) changes `model.py` and `store.py`, not only `cli.py` and one new module. Threatens QS-3 (QG-3).
- **Debt: the file grows without bound.** Every command reads the whole file, and nothing compacts it. The scale of use is not yet confirmed. Threatens nothing measured yet.
- **Debt: adding an existing name replaces its date.** Replay is keyed by name, and the domain question whether two items may share a name is open.
- **Debt: tests change the process environment.** `setUp` sets `PANTRY_FILE` in `os.environ` and never restores it.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
