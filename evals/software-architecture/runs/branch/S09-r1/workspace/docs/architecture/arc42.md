# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | The product's core function; it fixes what the store holds. |
| R-2 | No item is lost if the machine crashes mid-write. | 1 | active | Shapes the storage format and write path. |
| R-3 | Runs with only the Python standard library. | 3 | active | A third-party-dependency decision; the central list covers it. |
| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | Constrains module boundaries and how features are added. |

Gap check: the architect left out Security: confidentiality and Interaction capability: user
error protection. No requirement was added.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: modifiability | R-4 | QS-1 |

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- Python 3 with the standard library only (`docs/adr/0006-standard-library-only.md`).
- Items are kept in `~/.pantry.jsonl` unless `PANTRY_FILE` names another file (README).
- The code records no minimum Python version.

## 3. Context and scope

*As found, unconfirmed.*

The system is a command-line program that a user runs in a terminal (`python3 -m pantry`). Its only
external dependency is the local file that holds the records. The code talks to no network service
and to no other program.

## 4. Solution strategy

*As found, unconfirmed.*

- The pantry file is an append-only log of `add` and `remove` records; the items are the result of
  replaying the log in order (`docs/adr/0002-storage-format.md`). Each append is fsynced, which
  aims at R-2; section 11 records where that aim falls short.
- Each command is a short path from the command line to one of the building blocks in section 5
  (section 6).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry/__main__.py` | entry point for `python3 -m pantry`; passes arguments to `cli` and exits with its code | `cli` |
| `pantry/cli.py` | parses commands, prints results and user errors, sets exit codes | `store`, `dates`, `model` |
| `pantry/store.py` | reads and appends records in the pantry file | `model` |
| `pantry/model.py` | the `Item` and the add and remove records; replays records into items | none |
| `pantry/dates.py` | parses date text as the user types it (ISO, `today`, `tomorrow`, `+Nd`, `+Nw`) | none |

The tests in `tests/` use every block and are not a block themselves.

The rules that bind these blocks are in `docs/adr/0003-dependency-rule.md`. The code has an edge
from `cli` to `model` that the approved central list does not name.

## 6. Runtime view

*As found, unconfirmed.*

- **add:** `cli` parses the name and the expiry; `dates.parse` turns the expiry into a date;
  `store.add` builds the `Item` record and appends it, then fsyncs.
- **list:** `store.items` reads every line of the file, skips any line that is not JSON, and
  replays the records; `cli` sorts the items by expiry then name, filters with `--soon DAYS` when
  given, and prints one line per item.
- **remove:** `cli` checks that the name is present through `store.items`; then `store.remove`
  appends a removal record. The check and the append are two steps, not one.

## 7. Deployment view

*As found, unconfirmed.*

The program runs on one machine, from the repository or wherever the package is copied, with
`python3 -m pantry`. The data is one file per user, in the home directory by default. The
repository has no packaging file (`pyproject.toml`, `setup.py`) and no install step.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Errors:** user errors go to stderr with the prefix `pantry:` and exit 1; bad usage exits 2
  (`docs/adr/0005-crosscutting-conventions.md`).
- **Dates:** stored and printed as ISO 8601 (`YYYY-MM-DD`); typed as ISO, `today`, `tomorrow`,
  `+Nd` or `+Nw`.
- **Names:** an item's identity is its exact name (case-sensitive for `remove`); `list` sorts names
  ignoring case.
- **Encoding:** the pantry file is UTF-8.
- **Versioning:** none found. The records and the file carry no version field.
- **Testing:** `unittest`, in `tests/test_pantry.py`; the five tests pass.

## 9. Architecture decisions

The decision list is [ADR 0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md),
accepted 2026-11-21. The ADRs recovered from the code are
[0002](../adr/0002-storage-format.md) to [0006](../adr/0006-standard-library-only.md), all
`proposed` until the architect approves them.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a new command is added | normal development | the change touches cli.py and at most one new module; store.py and model.py are unchanged | at most 2 files changed; 0 changes to store.py or model.py |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Torn line makes the next add disappear (threatens R-2).** A line cut short by a crash is
  not terminated by a newline, so the next append is written onto it. `store.py:29` then drops
  the whole line, and the new item is lost. `add` still reports success. Reproduced; the
  existing test `test_a_torn_last_line_is_skipped` does not append after the torn line.
- **Any unreadable line is skipped silently (threatens R-2).** `store.py:27-29` skips any line
  that is not JSON, not only a torn last line. Damage in the middle of the file loses records
  without a message.
- **The new file's directory entry is not fsynced (threatens R-2).** `store.py:14-17` fsyncs the
  file, not its directory. A crash just after the first `add` could lose the file. Not reproduced.
- **A repeated name replaces the earlier item (threatens R-1).** `model.py:24` keys items by name,
  so a second `add` of the same name replaces the first expiry without a message.
- **Removed items stay in the file (debt).** Removals are appended, never compacted, so every
  `list` reads the whole history (`store.py:20-30`).
- **No versioning of the file or the CLI (debt).** The records and commands carry no version; a
  format change would break existing files.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
