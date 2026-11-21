# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add an item with an expiry date and list the items expiring within N days, from the command line. | 1 | active | Defines the product; shapes the CLI and the store. |
| R-2 | No item whose add or remove succeeded is lost if the machine crashes during a write. | 2 | active | Sets how every write is made durable. |
| R-3 | The tool runs on the Python standard library alone, with no third-party packages. | 3 | active | Rules out third-party dependencies. |
| R-4 | Adding a new command changes only `cli.py` and at most one new module. | 4 | active | Sets the building-block boundaries and the dependency rule. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1 | QS-1 |
| QG-2 | Reliability: recoverability | R-2 | QS-2 |
| QG-3 | Flexibility: installability | R-3 | QS-3 |
| QG-4 | Maintainability: modifiability | R-4 | QS-4 |

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- Standard library only: every import in `pantry/` comes from the standard library (see the ADR proposed for third-party dependencies).
- The pantry file is `~/.pantry.jsonl`, or the path in `PANTRY_FILE`.
- No Python version is declared in the repository. The code uses `dataclasses` and `pathlib`, so it needs Python 3.7 or later.

## 3. Context and scope

*As found, unconfirmed.*

- Inside the system: the `pantry` package, run as `python3 -m pantry`.
- Outside the system: the user typing commands; the pantry file on the local disk (`PANTRY_FILE` or `~/.pantry.jsonl`); the system clock (`date.today()`), which gives the meaning of relative dates and of `list --soon`.

## 4. Solution strategy

*As found, unconfirmed.*

- The pantry file is an append-only log of add and remove records. The items are derived by replaying the log (R-2, QG-2).
- Each record is flushed and fsynced when it is written (R-2, QG-2).
- Only the standard library is used (R-3, QG-3).
- The date parsing (`dates`) and the item model (`model`) know nothing of files or commands. The command line (`cli`) only composes them, and `store` is the only block that touches the file (R-4, QG-4).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `pantry/__main__.py` | entry point: passes the arguments to `cli.main` and exits with its code | `cli` |
| `pantry/cli.py` | command parsing; user-facing errors and exit codes; sorting and filtering for `list` | `dates`, `store`, `model` |
| `pantry/store.py` | the pantry file: appends records, reads them back, skips lines it cannot parse | `model` |
| `pantry/model.py` | `Item`, the add and remove records, and the replay of records into items | standard library only |
| `pantry/dates.py` | parses user date text (`YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`, `+Nw`) into a date | standard library only |

## 6. Runtime view

*As found, unconfirmed.*

- `add NAME DATE`: `cli.main` parses the date with `dates.parse`, builds an `Item`, and `store.add` appends its add record and fsyncs the file.
- `list [--soon DAYS]`: `store.items` reads every line of the file, skipping lines that do not parse; `model.replay` keeps the last record per name; `cli` sorts by expiry, then name, and filters to the window.
- `remove NAME`: `cli` reads the items to check that the name exists, then `store.remove` appends a remove record. Exit 1 if it does not exist.

## 7. Deployment view

*As found, unconfirmed.*

The tool runs from a checkout of this repository, as `python3 -m pantry`. The repository has no packaging file (no `pyproject.toml` or `setup.py`), so no installed form exists.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- Errors: a user error prints one line `pantry: <message>` to stderr and exits 1. Bad usage exits 2 (argparse). Unparseable lines in the pantry file are skipped with no message.
- Dates: calendar dates without time, in ISO form. Relative dates are counted from the local date (`date.today()`). `tomorrow` is one day; `+Nw` is seven times N days.
- Names: an item is identified by its exact name. Adding an existing name replaces its expiry date. Removing deletes by exact name. Sorting ignores case.
- Text: the pantry file is UTF-8, one JSON object per line.

## 9. Architecture decisions

The ADRs live in `../adr/`. The list of decisions made centrally is in
[0001. Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | after `add` of items with valid dates, `list --soon N` is run | normal operation | the output lists exactly the items whose expiry is on or before today + N, sorted by expiry | 0 mismatches over a test set of items spread across the window |
| QS-2 | QG-2 | the process is killed with SIGKILL at random points during `add` or `remove` | normal operation | every command that exited 0 is present afterwards and no earlier item is lost; the store still opens | 0 lost acknowledged writes in 200 kill trials |
| QS-3 | QG-3 | the tool is run on a clean Python 3 install | normal operation | every command runs | runs every command with 0 non-stdlib packages installed |
| QS-4 | QG-4 | a developer adds a new command | normal operation | the change touches only `cli.py` and at most one new module | 100% of added commands within that limit, checked in review or a test |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Torn line followed by an append loses the next record** (reproduced). A crash mid-write leaves a partial line with no newline; the next `add` lands on that line and is skipped on read. Threatens R-2.
- **Silent skipping of unparseable lines.** Any damaged line hides its record without a message, so the loss is invisible. Threatens R-2.
- **New file not made durable.** `store` fsyncs the file but not its directory, so a crash just after the first `add` may lose the file. Not reproduced; no crash test exists. Threatens R-2.
- **Unbounded growth.** The file is never compacted and every command reads all of it. No goal covers it yet.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
