# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | It is the product's purpose and fixes the storage and CLI shape. |
| R-2 | No item is lost if the machine crashes mid-write. | 1 | active | It decides how every write is made durable. |
| R-3 | Runs with only the Python standard library. | 3 | active | It limits every block's dependencies. |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | It sets the module structure and the dependency rule. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Maintainability: modifiability | R-4 | QS-2 |
| QG-3 | Flexibility: installability | R-3 | QS-3 |
| QG-4 | Functional suitability: functional correctness | R-1 | QS-4 |

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- Standard library only: no package outside the standard library is imported anywhere in `pantry/` or `tests/`.
- Python 3: the code uses `dataclasses` and `date.fromisoformat`, so 3.7 or later. The minimum version is not confirmed.
- Data lives under the user's home directory (`~/.pantry.jsonl`), overridable with `PANTRY_FILE`.

## 3. Context and scope

*As found, unconfirmed.*

The pantry command, run from a terminal. Outside it: the file at `store.path()` (`PANTRY_FILE`, or `~/.pantry.jsonl`), the system clock (`date.today()`), and the command line, stdout and stderr. The system makes no network calls.

The "Out of scope" subsection below is the architect's answer and carries no marker.

### Out of scope

Confirmed by the architect as not wanted:

- protecting the pantry file from other users on the machine (confidentiality);
- list speed for large files (time behaviour);
- importing or exporting the pantry, such as to CSV (interoperability);
- interactive confirmation before `remove` (user error protection); errors are reported with exit codes and messages only.

## 4. Solution strategy

*As found, unconfirmed.*

- **Append-only event log.** Each add and remove is one appended line; the current pantry is the replay of the log (`model.replay`). Serves QG-1: no in-place rewrite that a crash could corrupt.
- **Flush and fsync each append** before the command returns (`store._append`). Serves QG-1.
- **One plain file, no database, standard library only.** Serves QG-3.
- **Dates are parsed once, at input,** and stored as absolute ISO dates. Serves QG-4.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry/__main__.py` | entry point for `python3 -m pantry`; passes argv to `cli.main` and exits with its result | `cli` |
| `pantry/cli.py` | parses commands and flags, prints results, maps errors to exit codes | `dates`, `store`, `model` |
| `pantry/store.py` | reads and appends the pantry file; skips lines that do not parse; exposes `add`, `remove`, `items` | `model` |
| `pantry/model.py` | the `Item` type, the record format, and replay of records into current items | standard library only |
| `pantry/dates.py` | parses date input: ISO dates, `today`, `tomorrow`, `+Nd`, `+Nw` | standard library only |

`tests/test_pantry.py` exercises these blocks through their functions. It is not a building block.

## 6. Runtime view

*As found, unconfirmed.*

- **`add NAME EXPIRES`:** `cli` parses `EXPIRES` with `dates.parse`; on failure it prints to stderr and exits 1. Otherwise `store.add` appends an add record, flushed and fsynced, and the command exits 0.
- **`remove NAME`:** `cli` checks `NAME` against `store.items()`; if absent, it prints to stderr and exits 1. Otherwise `store.remove` appends a remove record.
- **`list [--soon DAYS]`:** `store.items()` replays the whole file. `cli` sorts by expiry, then name case-insensitively, keeps items expiring on or before today plus `DAYS` if given, and prints `ISO-DATE  NAME` per line.

## 7. Deployment view

*As found, unconfirmed.*

Run from the source tree as `python3 -m pantry`. The repository has no packaging file (no `setup.py` or `pyproject.toml`). Tests run with `python3 -m unittest`. Data is on the local disk of the machine, at the path in section 3.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Errors:** user errors print `pantry: <message>` to stderr and exit 1. Bad usage exits 2 with the argparse message on stderr.
- **Durability:** each append is flushed and fsynced. The directory is not fsynced (section 11).
- **Records:** one JSON object per line, with keys `op`, `name` and `expires`. Dates are ISO calendar dates with no time or zone.
- **Dates:** the local calendar date from `date.today()`. Relative input is resolved when the item is added and stored as an absolute date.
- **Names:** item names are exact strings. `remove` and replay match them case-sensitively; `list` sorts them case-insensitively.
- **Naming:** lowercase module names; `Item` for the item class; `to_record`, `removal` and `replay` in `model`.

## 9. Architecture decisions

ADRs live in [`../adr/`](../adr/). The ADR [Record architecture decisions](../adr/0001-record-architecture-decisions.md) is `accepted`. The as-found decisions are proposed in ADR 0002 to 0009, each waiting for the architect's approval.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the interrupted item is either fully stored or absent; items stored before the crash stay readable | 0 acknowledged items lost in 100 SIGKILL trials during `add` |
| QS-2 | QG-2 | a new command is added to the CLI | normal operation | the change touches `cli.py` and at most one new module | a new command's diff touches only `cli.py` and at most one new module |
| QS-3 | QG-3 | the tool is run on a fresh Python 3 install with no pip | normal operation | the tool runs with no install step | 0 non-standard-library imports |
| QS-4 | QG-4 | `list --soon DAYS` is run against items with mixed expiry dates | normal operation | every item expiring within DAYS is listed, none later, sorted by expiry | every item expiring within N days is listed, none later, sorted by expiry |

## 11. Risks and technical debt

*As found, unconfirmed.*

1. **A new record is glued onto a partial line (verified).** After a crash leaves a partial line with no newline, the next `add` appends onto it. Both records end up on one line, and the new item is lost on read. Threatens R-2 and QS-1. A probe confirmed it: an item acknowledged after a torn write was missing from `store.items()`.
2. **Corrupt lines in the middle of the file are skipped silently** (`store._records`). Threatens R-2. The architect has already accepted this in ADR 0001's consequences; it is listed here for review.
3. **A record that is valid JSON but lacks a key raises an error on read** (`model.replay`), so every `list` and `remove` fails until the file is repaired. Threatens R-1. Found by reading; not run.
4. **The directory is not fsynced when the file is created.** A crash just after the first add may lose the file's directory entry. Threatens R-2. Found by reading; not run.
5. **Nothing guards against two processes appending at once.** Threatens R-2. Found by reading; not run.
6. **Technical debt: no compaction.** The file grows with every add and remove, and every command reads all of it. The architect has said list speed is out of scope, so this is debt, not a goal.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
