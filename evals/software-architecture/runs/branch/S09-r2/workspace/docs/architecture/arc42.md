# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | No item is lost if the machine crashes mid-write. | 1 | active | Data loss is irreversible; the storage format and write rule are expensive to change. |
| R-2 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | Defines the CLI surface and what is stored. |
| R-3 | Runs with only the Python standard library. | 3 | active | Third-party dependency decision. |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | Module-boundary rule; a cost of change rather than a user-visible result. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-1 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Maintainability: modifiability | R-4 | QS-3 |

Open, no measure yet: functional correctness for R-2 (what would show R-2 is met?). Not a goal until the architect gives a measure.

### Gap review

Asked at setup, for each ISO/IEC 25010 characteristic no requirement supports: the architect answered that nothing is missing. No requirement was added from this review.

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- Python 3 with the standard library only (ADR-0004). The code uses `dataclasses` and `date.fromisoformat`, so it needs Python 3.7 or later; no minimum version is stated anywhere.
- The pantry file lives at `$PANTRY_FILE`, or `~/.pantry.jsonl` when that is unset.
- Tests run with `python3 -m unittest`, as the README says.

## 3. Context and scope

*As found, unconfirmed.*

- The user, who runs `python3 -m pantry` from a terminal.
- The pantry file on the local disk.
- The system clock, read for relative dates and for `list --soon`.

Nothing else: no network, no other programs.

## 4. Solution strategy

*As found, unconfirmed.*

- An append-only log of changes, replayed on read: each change is one appended record and the pantry's state is derived from them (ADR-0002). Traces to QG-1.
- Standard library only, with no packaging step (ADR-0004). Traces to QG-2.
- One module per concern (`cli`, `store`, `model`, `dates`), with a thin entry point, and a fixed dependency direction (ADR-0005). Traces to QG-3.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry/__main__.py` (entry point) | passes the arguments to `cli.main` and exits with its code | `cli` |
| `pantry/cli.py` | parses commands, validates input, prints output, maps outcomes to exit codes | `store`, `dates`, `model` |
| `pantry/store.py` | reads and appends the pantry file | `model` |
| `pantry/model.py` | the `Item` type, the add and remove records, and replaying records into items | standard library only |
| `pantry/dates.py` | parses dates as users type them | standard library only |
| `tests/` | unit tests for dates, store and the CLI | `pantry` |

## 6. Runtime view

*As found, unconfirmed.*

- **add:** `cli.main` parses the arguments, `dates.parse` reads the expiry (on a bad date: message on stderr, exit 1), `store.add` turns the item into a record, and `store._append` writes the line, flushes and fsyncs it. Exit 0.
- **remove:** `cli` reads the current items and checks that the name exists (otherwise message on stderr, exit 1). `store.remove` appends a remove record through the same append path. Exit 0.
- **list:** `store.items` reads every line of the file, skips lines that do not parse, and replays the records into items. `cli` sorts by expiry date, then by name case-insensitively, optionally keeps items expiring within `--soon` days of today, and prints `YYYY-MM-DD  name` per item. Exit 0.

## 7. Deployment view

*As found, unconfirmed.*

Run from the source tree as `python3 -m pantry` on the user's machine with a Python 3 interpreter. There is no install or packaging file. The data lives in the user's home directory, or wherever `PANTRY_FILE` points.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Errors:** user errors print `pantry: <message>` on stderr and exit 1. Bad usage gets argparse's message and exit 2. Unparseable lines in the pantry file are skipped silently on read.
- **Dates:** `YYYY-MM-DD` on disk and in output. Input accepts `today`, `tomorrow`, `+Nd` and `+Nw`, resolved against the local date when the command runs.
- **Names:** an item is identified by its exact name. `remove` matches the name exactly, and a second `add` with the same name replaces the first. `list` sorts names case-insensitively.
- **Units:** `--soon` counts days; `+Nw` is seven days per week.
- **Encoding:** UTF-8 for the pantry file.
- **Logging:** none.

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in [`docs/adr/`](../adr/). The list of decisions made centrally is in [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md), accepted 2026-11-22.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed (SIGKILL) during `add` or `remove` | normal operation | every add or remove that returned is present afterwards, and the store still reads | 0 acknowledged items lost in 100 runs |
| QS-2 | QG-2 | the program and its tests are run on a fresh Python 3 interpreter with no packages installed | normal operation | the program runs and the tests pass | 0 non-stdlib imports; tests pass |
| QS-3 | QG-3 | a new CLI command is added | normal operation | the change touches only `pantry/cli.py` and at most one new module | at most 2 changed non-test files per new command |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Torn record glued to the next record (threatens R-1, QG-1).** After a crash cuts a record short, the next append continues on the same line and that next record is lost. Reproduced: `Milk`, added after a simulated torn write, does not appear in `list`.
- **Directory entry not synced (threatens R-1, QG-1).** The file is created by its first append. `_append` fsyncs the file but never its directory, so after a crash the file may be missing. Possible, not reproduced.
- **No locking (threatens R-1 under concurrent use).** Two processes can interleave appends. `remove` checks that the name exists and then appends without a lock.
- **The test suite misses the torn-record defect (threatens QG-3 testability).** The torn-line test only reads the file; no test appends after a torn line.
- **The whole file is read on every command and never compacted.** The file grows with its history, and so does each command's cost.
- **Duplicate names replace silently.** Unconfirmed whether intended; it is a user-error case.
- **`list --soon` includes items that have already expired.** It has no lower bound. Unconfirmed whether intended.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
