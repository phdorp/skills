# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | — |
| R-2 | No item is lost if the machine crashes mid-write. | 2 | active | — |
| R-3 | Runs with only the Python standard library. | 3 | active | — |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | — |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-3 | Maintainability: modularity | R-4 | QS-1 |

Open, without a measure yet: R-1 (functional correctness) and R-2 (reliability: recoverability).

### Stakeholders

- The owner: one person, using one machine, who records and lists their own pantry.
- The maintainer: one person, comfortable with Python, with no budget constraint.

## 2. Constraints

- Standard library only; no third-party packages (R-3).
- Python 3.9 or newer.
- Linux and macOS.
- The data holds item names and dates only, kept on the user's machine until they remove the item. No law or contract applies.

*As found, unconfirmed.* All storage is one local file; the code uses no server, network or database (`pantry/store.py:9-10`).

## 3. Context and scope

Out of scope for v1: sync between machines, a GUI, reminders, barcode scanning, and data exchange with other systems.

Figures: up to about 1,000 items, now and in a few years.

*As found, unconfirmed.* The system is the `python3 -m pantry` process. Outside it are the user, who types commands (`pantry/cli.py`); the local file, at `PANTRY_FILE` or `~/.pantry.jsonl` (`pantry/store.py:9-10`); and the system clock, read for relative dates (`pantry/dates.py:9`). Nothing else is contacted.

## 4. Solution strategy

*As found, unconfirmed.*

- **An append-only log.** Each change is one appended record, and the current items are derived by replaying the log. This is the write rule of ADR-0002, which serves R-2.
- **Small blocks with a one-way dependency rule.** A new command changes `cli.py` and at most one new module (R-4, QG-3; ADR-0004).
- **Standard library only.** No third-party package (R-3; ADR-0003).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `__main__` | entry point: runs `cli.main` with the arguments and exits with its code | `cli` |
| `cli` | parses the command line; runs `add`, `list` and `remove`; prints results and errors | `dates`, `store`, `model` |
| `store` | reads and appends the pantry file; the only block that touches the file | `model` |
| `model` | the item and the records; replays records into the current items | none |
| `dates` | parses the date forms the user types | none |

`pantry/__init__.py` holds only the package docstring.

## 6. Runtime view

*As found, unconfirmed.*

- **add:** `cli.main` → `dates.parse` (on failure: message to stderr, exit 1) → `store.add` → `Item.to_record` → `store._append`, which opens the file in append mode, writes one line, flushes and fsyncs.
- **list:** `store.items` → `store._records` (malformed lines skipped) → `model.replay` → sort by expiry, then lowercase name → optional `--soon` filter → print `date  name`.
- **remove:** `store.items` checks the name exists (otherwise message to stderr, exit 1) → `store.remove` appends a `remove` record.

## 7. Deployment view

*As found, unconfirmed.* One Python process, started with `python3 -m pantry` on the user's machine. Nothing is deployed and no service runs. The data is one file in the home directory unless `PANTRY_FILE` names another. Tests run with `python3 -m unittest` (README).

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Exit codes:** 0 success, 1 user error, 2 bad usage, including unknown commands; `--help` exits 0 (`pantry/cli.py:23`). See ADR-0005.
- **Errors:** messages go to stderr, prefixed `pantry:`.
- **Dates:** the accepted forms and the ISO 8601 storage format are in ADR-0006. Relative dates count from today.
- **Names:** `remove` matches the name exactly and case-sensitively (`pantry/cli.py:32`). The list sorts case-insensitively (`pantry/cli.py:37`). A name is unique: adding an existing name replaces its expiry (`pantry/model.py:24`).
- **Expiry in lists:** `list --soon` includes items already past their date (`pantry/cli.py:40`).
- **Malformed lines:** the reader skips any line that does not parse, without a warning (`pantry/store.py:28-29`). See section 11.
- **Logging:** none. Output goes to stdout only for `list`.

## 9. Architecture decisions

ADRs live in `../adr/`. The decision on what is made centrally is recorded in [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md) (accepted 2026-11-24). The decisions recovered from the code are in ADR-0002 to ADR-0006, each `proposed` until you accept it.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-3 | a developer adds a new command (source: developer; artifact: the pantry package) | the current module layout: cli, dates, store, model | the change is confined to cli.py and at most one new module | 0 edits outside cli.py and one new module for a trial command |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **A torn write loses the next record (R-2).** A partial last line with no newline is followed by the next append, which joins that line and is then discarded (`pantry/store.py:13-17`, `:25-29`). Reproduced: the command exits 0 and the item is missing.
- **Silent loss of any bad line (R-2).** Any malformed line is dropped without a warning, not only a torn last line (`pantry/store.py:28-29`). Corruption in the middle of the file loses items unnoticed.
- **A test gap (R-2).** `test_a_torn_last_line_is_skipped` (`tests/test_pantry.py:39`) checks reading after a torn line, not appending after it, so the defect above passes the suite.
- **Permissions (confidentiality, not a confirmed requirement).** The file is created with the default umask (`pantry/store.py:14`), so other local users may be able to read it. The Q6 question is open.
- **No locking.** Two processes that run `add` or `remove` at the same time have no lock, and `remove` checks the file before it appends (`pantry/cli.py:32`). A race can give an inconsistent result.
- **Unbounded log.** Every change appends a line, and the file is never compacted. This is harmless at the expected size of about 1,000 items.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
