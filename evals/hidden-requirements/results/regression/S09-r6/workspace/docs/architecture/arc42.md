# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | Core use of the product. |
| R-2 | No item is lost if the machine crashes mid-write. | 1 | active | Decides how data is stored and written; the other rows depend on the data being trustworthy. |
| R-3 | A new command touches only `cli.py` and at most one new module. | 3 | active | Sets the module boundary and the dependency rule. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-1 | QS-2 |
| QG-3 | Maintainability: modifiability | R-3 | QS-3 |

### Stakeholders

- The pantry owner: the one person who adds, lists and removes items, on one machine from a terminal.
- The architect: owns the requirements, goals and architecture decisions.

## 2. Constraints

- Python standard library only; no third-party packages.
- Runs on Linux and macOS with Python 3.10 or newer.
- No network access.
- Items are kept in a local file: `~/.pantry.jsonl`, overridable with `PANTRY_FILE`.

*As found, unconfirmed.*

- The code imports only standard-library modules (see ADR-0006).

## 3. Context and scope

Out of scope:

- network access, accounts and cloud sync;
- editing items, quantities, and reminders or notifications (may come later; not part of the first version).

Figures: a few hundred items, one user, one machine.

*As found, unconfirmed.*

- Outside the system: the user at a terminal, the `PANTRY_FILE` environment variable, and the home directory, which holds the default file. Nothing else is contacted.

## 4. Solution strategy

*As found, unconfirmed.*

- The pantry is a log: each add or remove is appended as one JSON record, and the items are the result of replaying the log in order. Crash-safety rests on append-only writes and `fsync` (ADR-0002; R-2, QG-1).
- Replay logic is pure: `model.py` has no file access, so the rules can be tested on their own (QG-2).
- The CLI is a thin layer: `cli.py` parses arguments, calls the store and prints. New commands are added there (R-3, QG-3; ADR-0003).
- Standard library only (ADR-0006).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `cli` (`pantry/cli.py`) | parse arguments, run add, list and remove, print, exit codes | `dates`, `store`, `model` |
| `store` (`pantry/store.py`) | the pantry file: append records, read and replay them | `model` |
| `model` (`pantry/model.py`) | the `Item` and record shapes, and the replay rule | none |
| `dates` (`pantry/dates.py`) | parse dates typed by users | none |
| entry point (`pantry/__main__.py`) | run `cli.main` for `python3 -m pantry` | `cli` |

`pantry/__init__.py` holds only a docstring. The one test module, `tests/test_pantry.py`, exercises `cli`, `store`, `model` and `dates`.

## 6. Runtime view

*As found, unconfirmed.*

- **add:** `cli` parses the date with `dates.parse`, then `store.add` appends one `add` record.
- **remove:** `cli` checks that the name is present in `store.items()`, then `store.remove` appends a `remove` record. A missing name exits 1.
- **list --soon N:** `store.items()` reads the file, skipping lines it cannot parse, and replays the records. `cli` keeps items expiring within N days, sorts them by expiry and then name, and prints them.

## 7. Deployment view

*As found, unconfirmed.*

- Runs as a local process: `python3 -m pantry <command>`. No server, and no packaging file in the repository.
- Data: one file, in the home directory or at `PANTRY_FILE`.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Error handling:** user errors print one line to stderr and exit 1; bad usage exits 2; success exits 0 (ADR-0004).
- **Dates:** users type `today`, `tomorrow`, `+Nd`, `+Nw` or `YYYY-MM-DD`; the file stores `YYYY-MM-DD` (ADR-0005).
- **Naming:** an item is identified by its exact name, case-sensitive, in add and remove. Sorting ignores case. Adding a name that already exists replaces its expiry date.
- **Units:** `--soon` takes days.
- **Logging:** none.

## 9. Architecture decisions

ADRs are in [`../adr/`](../adr/). The "Record architecture decisions" ADR is [`0001-record-architecture-decisions.md`](../adr/0001-record-architecture-decisions.md), accepted 2026-11-24. The ADRs for the decisions the code already makes, [0002](../adr/0002-append-only-json-lines-pantry-file.md) to [0006](../adr/0006-standard-library-only.md), are proposed and await the architect's decision.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` or `remove` | normal operation | every add that returned success is still listed and the file reads without error | 0 lost acknowledged adds and 0 unreadable files in 100 kill trials |
| QS-2 | QG-2 | `list --soon N` runs on generated item sets | normal operation | it shows exactly the items expiring within N days from today, sorted by expiry | 0 mismatches over 1000 generated item sets |
| QS-3 | QG-3 | a new command is added | normal operation | the change touches only `cli.py` and at most one new module | 0 changed files outside `cli.py` and one new module |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Torn last line loses the next add (threatens R-2, QG-1).** After a crash leaves a partial last line, the next `add` is appended onto it, so the new item is silently lost and the command exits 0. Reproduced on the current code.
- **Silent skip of bad lines (threatens R-2, QG-1).** `store._records` skips any line it cannot parse, including one in the middle of the file, with no warning.
- **Test gap (threatens QG-1).** The torn-line test checks only that the partial line is skipped. No test covers an add after a torn line, or a kill during a write.
- **Concurrent commands (threatens R-2 under the agreed concurrency expectation).** Two commands that append at the same time take no lock, and no test covers it.
- **No format version (threatens ADR-0002 and its future changes).** Records carry no version field, so a future format change has no migration path. The architect's versioning decision has no code behind it yet.
- **Unbounded file growth.** The file keeps every add and remove and is never compacted. Not a current goal; noted for the future.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
