# pantry: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | Core use; fixes the CLI interface and the expiry-date data every block uses. |
| R-2 | An item the store has confirmed as added stays listed after a crash at any point during a write. | 1 | active | A lost item cannot be recovered by the user. |
| R-3 | Runs with only the Python standard library. | 3 | active | Limits every dependency choice; the code already meets it. |
| R-4 | Adding a command changes only `cli.py` and at most one new module, tests excluded. | 4 | active | Matters for the next feature, not now. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Functional suitability: functional correctness | R-1 | QS-2 |
| QG-3 | Maintainability: modifiability | R-4 | QS-3 |

### Stakeholders

### Gap review

Asked at setup: security (confidentiality), performance efficiency (capacity), and interaction capability (user error protection). The architect answered that nothing is missing; no requirement was added.

## 2. Constraints

*As found, unconfirmed.*

- The runtime is Python 3 with the standard library only (R-3). The code uses `dataclasses` and `date.fromisoformat`, so it needs Python 3.7 or later. No minimum version is measured yet (QG-3 is open).
- The data file is `~/.pantry.jsonl`, overridable with the `PANTRY_FILE` environment variable.

## 3. Context and scope

*As found, unconfirmed.*

- A person runs `python3 -m pantry` in a terminal.
- Inputs from outside: command-line arguments, the `PANTRY_FILE` environment variable, the file in the home directory, and the system date (`date.today()`).
- Outputs: lists on stdout, errors on stderr, and the exit status.

## 4. Solution strategy

*As found, unconfirmed.*

- Changes are stored as events, not as state: every `add` and `remove` is appended as a record, and the current items are replayed from the records (`store.py`, `model.replay`). This is the basis of R-2.
- A thin command-line layer sits over a model with no I/O: `argparse` dispatch in `cli.py`, and `model.py` holds only data and replay. This is the basis of R-4.
- Dates typed by the user are resolved to absolute dates once, when added (`dates.py`); the file holds ISO dates. This is the basis of R-1.
- The standard library is the only dependency (R-3).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| cli (`pantry/cli.py`) | parses the commands, runs them, prints output and the exit status | store, model, dates |
| store (`pantry/store.py`) | locates the file, appends records, reads them back and replays them | model |
| model (`pantry/model.py`) | the `Item` and its records, and replay; no I/O | (none) |
| dates (`pantry/dates.py`) | parses user date text into dates | (none) |
| entry (`pantry/__main__.py`) | makes `python3 -m pantry` call `cli.main` | cli |
| tests (`tests/test_pantry.py`) | unit tests of dates, store and cli | cli, store, model, dates |

`pantry/__init__.py` holds only the package docstring.

## 6. Runtime view

*As found, unconfirmed.*

- **add:** cli parses the arguments, `dates.parse` turns the expiry into a date, `store.add` appends an `add` record as one line, and it is fsynced.
- **remove:** cli replays the items and checks the name exists (exit 1 if not); `store.remove` appends a `remove` record.
- **list:** `store.items` reads the whole file, skips lines that are not JSON, and replays the records. cli sorts by expiry, then by case-insensitive name, keeps the items up to `today + DAYS` when `--soon` is given (inclusive), and prints `date  name` per line.

## 7. Deployment view

*As found, unconfirmed.*

- It runs from the source tree with `python3 -m pantry`. There is no packaging metadata and no install step.
- The data lives in the home directory of the user who runs it, on that machine.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Names:** items are keyed by their exact name; sorting ignores case.
- **Dates:** the file holds ISO dates; relative forms (`+3d`, `tomorrow`) are resolved when added.
- **Errors:** user errors print to stderr and exit 1; bad usage exits 2 (see ADR 0005).
- **Durability:** each record is fsynced after the append. There is no lock and no atomic rename.
- **Tests:** `unittest`; each test points `PANTRY_FILE` at a temporary file.

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in [`../adr/`](../adr/). [ADR 0001, Record architecture decisions](../adr/0001-record-architecture-decisions.md) lists the decisions made centrally; it is accepted. The ADRs for the decisions the code already makes are proposed until the architect accepts them.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | every item an earlier `add` confirmed is still listed, and the file reads without error | 0 lost confirmed items in 100 trials |
| QS-2 | QG-2 | `list --soon N` is run | normal operation | it lists exactly the items expiring on or before today+N, sorted by expiry | 0 wrong rows at the boundaries N−1, N and N+1 days |
| QS-3 | QG-3 | a developer adds a new command | normal operation | the change touches `cli.py` and at most one new module | at most 2 files changed per new command, tests excluded |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **A partial line corrupts the next write (R-2, QS-1).** After a crash that leaves a partial line with no newline, the next `add` is written onto that line and is lost. Reproduced: "Oats" was lost. The test `test_a_torn_last_line_is_skipped` covers only the read, not this path.
- **Unparsable lines are skipped silently anywhere in the file (R-2).** Corruption in the middle of the file loses records without a message (ADR 0005).
- **A line that is valid JSON but has the wrong shape breaks every command (R-2).** Reproduced: `{}` raised `KeyError: 'op'`, and a bad date raised `ValueError`. One such line stops all use of the file.
- **Unknown `op` values are ignored silently.** Reproduced: `{"op": "eat"}` was accepted with exit 0.
- **Items are keyed by name (R-1, R-2).** A second `add` of a name replaces the first's expiry, and `remove` deletes every match. This is the open question on item identity.
- **No locking.** Two runs at once may interleave their appends. Not tested.
- **The file is never compacted.** Each `list` and `remove` reads and replays the full history. No goal covers this yet; it is debt.
- **Test gaps.** No test covers a crash during a write or the add-after-torn-line path. The tests set `PANTRY_FILE` in `os.environ` and do not restore it.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
