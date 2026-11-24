# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 1 | active | The core job; every other requirement protects it. |
| R-2 | No item is lost if the machine crashes mid-write. | 2 | active | Losing data is the costliest failure for a tool that holds the owner's food stock. |
| R-3 | Runs with only the Python standard library. | 4 | active | A constraint more than a trade-off; standard-library durability is possible alongside R-2. |
| R-4 | A new command touches only cli.py and at most one new module. | 3 | active | Shapes the building-block structure and every later change. |

Tie-break R-2 vs R-4 (confirmed by the ranking): R-2 is kept when only one of the two can be
fully met.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-3 | Flexibility: installability | R-3 | QS-1 |
| QG-4 | Maintainability: modifiability | R-4 | QS-2 |

Open, without a measure yet: a goal for R-1 (functional correctness) and a goal for R-2
(recoverability). They are not written as goals until the architect gives a measure.

Ruled out: confidentiality beyond the operating system's default file permissions. The
architect's reason: the item file holds the owner's own food stock, and default permissions
are enough; no encryption.

### Stakeholders

- Owner and sole user: uses the command line on a personal computer, and maintains the code.

## 2. Constraints

- Runs on Linux and macOS with Python 3.9 or newer.
- Uses only the Python standard library; no third-party packages (R-3).
- No hosting and no cost beyond the owner's own machine.

*As found, unconfirmed.*

- Every module imports only the standard library (ADR-0007).
- The entry point is `python3 -m pantry`; the tests run with `python3 -m unittest`.

## 3. Context and scope

Out of scope for the first version: synchronisation between devices, reminders or
notifications, quantities, categories, export, and exchange with other systems or people.

Figures: under 1,000 items; a file of a few hundred KB after five years of use; one person.

*As found, unconfirmed.*

The system is a command-line program on one machine. It reads the environment variable
`PANTRY_FILE` and the home directory to find its file, and the system clock for "today". It
uses no network.

## 4. Solution strategy

*As found, unconfirmed.*

- An append-only log of add and removal records, replayed on each read, serves R-2 (ADR-0002).
- Each record is fsynced as it is appended, serves R-2 (ADR-0003).
- Only the standard library is used, serves R-3 (ADR-0007).
- A thin command layer sits over a store that alone touches the file, serves R-4 (ADR-0005).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `cli` | the commands add, list and remove; argument parsing; exit codes; output | `dates`, `store`, `model` |
| `store` | reads and appends the pantry file; the only module that touches the file | `model` |
| `model` | the item and the add and removal records; replays records into the current items | none |
| `dates` | parses dates typed by users, relative to today | none |
| `__main__` | entry point for `python3 -m pantry` | `cli` |

`__init__.py` holds the package docstring only. The tests in `tests/test_pantry.py` exercise
the modules directly; they are not a block.

## 6. Runtime view

*As found, unconfirmed.*

- **add:** `cli` parses the arguments, `dates` parses the expiry, `store.add` appends one
  record, flushed and fsynced.
- **list:** `store.items` reads the file and skips unparsable lines; `model.replay` builds the
  current items; `cli` sorts them by expiry and name, filters by `--soon` days from today, and
  prints them.
- **remove:** `store.items` checks that the name exists (otherwise exit 1), then appends a
  removal record.

## 7. Deployment view

*As found, unconfirmed.*

There are no packaging files (no `pyproject.toml` or `setup.py`). The program runs from the
checkout with `python3 -m pantry`. Its data is a local file, at `PANTRY_FILE` or
`~/.pantry.jsonl`, on the same machine.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Errors and exit codes:** 0 success, 1 user error, 2 bad usage; user errors on stderr,
  prefixed `pantry:` (ADR-0006).
- **Dates:** `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`, `+Nw`; relative forms count from the
  local date (ADR-0004).
- **Data format:** UTF-8 JSON Lines, one record per line (ADR-0004).
- **Names:** an item's name is its key. Adding a name that exists keeps the later expiry; a
  removal deletes by exact name. `list` sorts names case-insensitively.

## 9. Architecture decisions

Decisions are recorded as ADRs in [`../adr/`](../adr/). The list of decisions made centrally is in [Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-3 | a fresh checkout is run with Python 3.9 or newer | a machine with only the standard library available | the CLI runs with no install step beyond the checkout | 0 imports outside the standard library |
| QS-2 | QG-4 | a commit adds a new command | normal development | the commit changes `cli.py` and at most one new module | 0 commits that change more than `cli.py` plus one new module |

## 11. Risks and technical debt

*As found, unconfirmed.*

1. **Torn write, then lost item** (threatens R-2; ADR-0003). Reproduced: after a line cut
   short, the next `add` joins it and that item is skipped on read.
2. **New file not made durable** (threatens R-2). By reading: fsync covers the file, not its
   directory entry, so a crash right after the first write may lose the new file.
3. **Concurrent writers** (threatens R-2). By reading: nothing locks the file, so two processes
   appending at once may interleave records.
4. **Duplicate names collapse** (threatens R-1). Adding an existing name silently replaces its
   expiry, and removal deletes every record with that name.
5. **Unbounded file** (no requirement yet). The file only grows, and every command replays all
   of it. This is harmless at the figures in section 3; revisit if they change.
6. **Test environment leak** (debt). The tests set `PANTRY_FILE` in the process environment and
   do not restore it.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
