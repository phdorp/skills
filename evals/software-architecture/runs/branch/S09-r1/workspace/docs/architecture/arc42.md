# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | Core function; fixes the CLI surface. |
| R-2 | No item is lost if the machine crashes mid-write. | 2 | active | Data loss is the worst failure; fixes durable, append-only storage. |
| R-3 | Runs with only the Python standard library. | 3 | active | Dependency rule that bounds every other choice. |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | Change-locality rule; yields to R-2 if a crash-safety fix needs a second module. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-1 | QS-2 |
| QG-3 | Portability: installability | R-3 | QS-3 |
| QG-4 | Maintainability: modifiability | R-4 | QS-4 |

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- Standard library only (R-3); see [ADR-0004](../adr/0004-standard-library-only.md).
- Python 3. No version is pinned. The code needs 3.7 or later (`dataclasses`, `date.fromisoformat`).
- Runs from the source tree as `python3 -m pantry`. No packaging metadata was found.

## 3. Context and scope

*As found, unconfirmed.*

The system is the `pantry` package. Outside it:

- **The user**, at a shell, who runs `python3 -m pantry <command>`.
- **The pantry file**, `~/.pantry.jsonl` or the path in the `PANTRY_FILE` environment variable,
  on the local file system.
- **The system clock**, read through `date.today()` for relative dates and for `list --soon`.

## 4. Solution strategy

*As found, unconfirmed.*

- **Append-only log, state by replay** (R-2, QG-1): every change is a record appended to the
  pantry file, and the items are rebuilt from the records on each run. See
  [ADR-0002](../adr/0002-append-only-jsonl-storage.md) and
  [ADR-0003](../adr/0003-fsync-each-record.md).
- **Thin command layer over pure modules** (R-4, QG-4): `cli` parses and prints. `dates` parses
  user dates, `model` defines the item and the replay, and `store` does the file I/O. See
  [ADR-0005](../adr/0005-building-block-dependencies.md).
- **Standard library only** (R-3, QG-3). See [ADR-0004](../adr/0004-standard-library-only.md).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `cli` (`pantry/cli.py`, entry point `pantry/__main__.py`) | parse the three commands, print output, map errors to exit codes | `dates`, `store`, `model` |
| `dates` (`pantry/dates.py`) | turn user date text into a `date`: ISO, `today`, `tomorrow`, `+Nd`, `+Nw` | none |
| `store` (`pantry/store.py`) | locate the pantry file, append records with fsync, read and skip unparsable lines | `model` |
| `model` (`pantry/model.py`) | the `Item` and the record shapes, and `replay` | none |

`pantry/__init__.py` holds only the package docstring. The tests (`tests/test_pantry.py`) call
`cli.main` and the modules directly, with a temporary `PANTRY_FILE`; they are not a block.

## 6. Runtime view

*As found, unconfirmed.*

- **`add NAME EXPIRES`:** `cli` calls `dates.parse`, then `store.add`, which appends one
  `add` record and fsyncs it. Exit 0.
- **`remove NAME`:** `cli` reads the names through `store.items`. If the name is absent it prints
  an error and exits 1. Otherwise `store.remove` appends a `remove` record. Exit 0.
- **`list [--soon DAYS]`:** `store.items` reads the whole file, skips lines that do not parse, and
  replays the records. `cli` sorts by expiry, then by name case-insensitively. With `--soon`, it
  keeps items expiring on or before today plus DAYS. It prints `YYYY-MM-DD  NAME` per line.
- **Errors:** an unparsable date prints `pantry: not a date: …` to stderr and exits 1. Bad usage is
  reported by `argparse` and exits 2. `--help` exits 0.

## 7. Deployment view

*As found, unconfirmed.*

A single user's machine. The code runs from the source tree with `python3 -m pantry`. No
installer, `setup.py` or `pyproject.toml` was found. The data lives in one file per user, at
`~/.pantry.jsonl` or at `PANTRY_FILE`.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Error handling:** user errors print one line to stderr and exit 1. Usage errors exit 2 (see
  [ADR-0006](../adr/0006-cli-commands-and-exit-codes.md)). Unparsable lines in the pantry file are
  skipped without a message (`store._records`); see section 11.
- **Naming:** an item's name is its identity. `add` with an existing name replaces that item's
  expiry, and `remove` matches the name exactly, case-sensitively. `list` sorts names
  case-insensitively.
- **Dates:** ISO 8601 in the file and in output ([ADR-0007](../adr/0007-iso-dates.md)). Relative
  forms resolve at command time against the machine's local date. `+Nw` is 7 days.
- **Units:** `--soon` and `+Nd` count days.
- **Configuration:** the `PANTRY_FILE` environment variable overrides the file path.
- **Testing:** `unittest` (`python3 -m unittest`). The tests use a temporary file for each test.

## 9. Architecture decisions

The ADRs live in [`docs/adr/`](../adr/). The list of decisions the architect makes centrally is in [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md) (accepted 2026-11-21). The decisions the code already makes are drafted as proposed ADRs 0002–0007, awaiting approval.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add`, and a further `add` then runs | normal operation | the earlier item is either fully stored or absent; the store still opens; the further add is not lost | 0 lost items in 100 kill-during-add trials followed by a further add |
| QS-2 | QG-2 | `list --soon N` is run over a corpus of items with varied expiry dates | normal operation | every item with expiry on or before today + N is listed, sorted by expiry | 0 misses in a test corpus |
| QS-3 | QG-3 | the tool is installed on a clean Python 3 with no pip step | fresh interpreter | every command runs | 0 non-standard-library imports |
| QS-4 | QG-4 | a new command is added | normal development | only `cli.py` and at most one new module change | 0 changes outside `cli.py` and one new module in the next added command |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Torn last line merges with the next record** (threatens R-2, QG-1). A crash that leaves a
  partial line with no newline is followed by the next `add` on the same line, and that record
  is then skipped on read. Reproduced on 2026-11-21. The test suite covers reading past a torn
  line, not appending after one.
- **Silent skipping of unparsable lines** (threatens R-2). Any bad line is dropped without a
  message, including corruption in the middle of the file.
- **Directory not fsynced on first create** (threatens R-2). [ADR-0003](../adr/0003-fsync-each-record.md)
  covers the file's data only. Found by reading; not reproduced.
- **No file lock** (threatens R-2). Two processes appending at once are not ruled out. Found by
  reading; not reproduced.
- **Whole file read on every command, no compaction** (technical debt). The file grows with
  every `add` and `remove`.
- **One item per name** (open question for the architect). A second `add` of the same name
  replaces the first item's date without warning. Intended or not is not stated anywhere.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
