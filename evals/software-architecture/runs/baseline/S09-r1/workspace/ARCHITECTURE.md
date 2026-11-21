# Architecture

`pantry` is a standard-library-only Python command-line tool. It keeps a list of
pantry items with expiry dates and prints what expires soon. This document
describes how the code is built today, the requirements it is meant to meet,
and where it falls short.

## Requirements

| # | Requirement | Status |
|---|---|---|
| 1 | Add pantry items with an expiry date; list what expires soon, from the CLI. | Met: `add`, `list --soon N`. |
| 2 | No item is lost if the machine crashes mid-write. | **Not met.** See [Known gaps](#known-gaps). |
| 3 | Runs with only the Python standard library. | Met. No third-party imports anywhere. |
| 4 | A new command touches only `cli.py` and at most one new module. | **Partly met.** See [Adding a command](#adding-a-command). |

## Modules

```
pantry/
  __main__.py   entry point: python3 -m pantry  ->  cli.main(argv)
  cli.py        argument parsing, command dispatch, output, exit codes
  dates.py      user date syntax -> datetime.date (pure)
  model.py      Item, record shapes, replay (pure)
  store.py      the pantry file: append records, read records (I/O)
```

Dependency direction (arrows mean "imports"):

```
__main__ -> cli -> dates
                -> store -> model
                -> model
```

- `dates` and `model` have no I/O and no dependencies inside the package. They
  are the easiest parts to test.
- `store` is the only module that touches the filesystem.
- `cli` is the only module that prints or reads `sys.argv`, and the only one
  that decides exit codes.

## Data model

The pantry file (default `~/.pantry.jsonl`, or `$PANTRY_FILE`) is an
**append-only event log**: one JSON object per line.

```json
{"op": "add", "name": "Milk", "expires": "2026-11-25"}
{"op": "remove", "name": "Milk"}
```

The current pantry is never stored directly. It is computed by `model.replay`,
which applies the records in order. `add` sets or overwrites an item by name.
`remove` drops it by name. Removing an absent name is a no-op.

Consequences:

- Writes never rewrite existing bytes. A write is one `append`.
- The file is the full history. Nothing is compacted yet, so it grows without
  bound.
- Item identity is the name, exactly as typed. `Milk` and `milk` are different
  items.

## Write and read path

Writing (`store._append`): open in append mode, write one line, `flush`, then
`os.fsync`. A record is durable once `add` or `remove` returns.

Reading (`store._records`): read the whole file, parse each line as JSON, and
skip lines that fail to parse. The skip exists so that a line cut short by a
crash does not stop the tool from starting.

## Command flow

`cli.main(argv)` does the following:

1. Parses arguments with `argparse`. A parse error or `--help` maps to exit
   code 0 for help and 2 for bad usage.
2. Runs the command. `add` parses the date with `dates.parse`, then calls
   `store.add`. `remove` checks that the name exists, then calls
   `store.remove`. `list` calls `store.items()`, sorts by
   `(expires, name.lower())`, filters with `--soon`, and prints
   `YYYY-MM-DD  Name`.
3. Returns the exit code. The contract is 0 for success, 1 for a user error
   (bad date, unknown item), and 2 for bad usage.

`dates.parse` accepts `YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`, and `+Nw`.
Relative forms are resolved against `date.today()`, and the function takes an
injectable `today` for tests.

## Adding a command

Requirement 4 says a new command should touch only `cli.py` and at most one
new module. The current layout supports that only when the command reads
existing data or uses the existing record types.

- **Fits:** a command that reads items (for example, `list --expired`). Add a
  subparser and a branch in `cli.main`, put the logic in one new module that
  takes `store.items()` as input, and leave `store` and `model` alone.
- **Does not fit:** a command that needs a new record type (for example, `edit`
  or `use` to change an expiry date). It must also change `model.py`
  (`replay`) and `store.py`, which is two existing modules, not one.

To keep the rule for the second case, a future change should either add the
new op to `model.py` as a single declared record type, or add an op registry
so a command module can register its own record type without editing
`model.py`. Neither exists yet. This is a decision for whoever adds the first
such command.

## Testing

`tests/test_pantry.py` uses `unittest` and points `PANTRY_FILE` at a temporary
file for each test. Run the suite with `python3 -m unittest`. The suite covers
relative date parsing, add/remove replay, skipping a torn last line, `list
--soon` ordering, and exit codes. It does not cover crash recovery beyond the
torn-last-line case, and it does not cover a torn line followed by further
writes.

## Known gaps

1. **A crash mid-write can lose the next item (requirement 2).** If a crash
   leaves a partial line with no trailing newline, the next `add` appends its
   record directly after the partial bytes. The two become one line, which
   fails to parse, and the newer record is skipped on read. Reproduced: after
   `Rice` is written, a partial `{"op": "add", "na` is appended, then `Milk` is
   added. `store.items()` returns only `Rice`, and the file contains
   `{"op": "add", "na{"op": "add", "name": "Milk", ...}`.

   Possible fix: before appending, check whether the file ends with `\n` and,
   if not, write a `\n` first. Reads should also report skipped lines rather
   than dropping them silently, so corruption in the middle of the file is
   visible.

2. **Directory entries are not fsynced.** When the file is first created, the
   `fsync` covers the file's data but not the directory entry that names it.
   A crash right after the first `add` can lose the file. Fix: fsync the parent
   directory once when the file is created.

3. **Skipped lines are silent.** `_records` drops any unparseable line,
   including corruption in the middle of the file, with no warning.

4. **The log grows without bound.** There is no compaction. This is acceptable
   for a pantry-sized file but should be noted.

## Decisions

- **Append-only log, not a rewritten JSON document.** Appends are the
  simplest crash-tolerant write: no temp files, no renames, and an interrupted
  write can only damage the last line.
- **Replay on every read.** The file is small, and this avoids a second
  source of truth that could drift from the log.
- **`fsync` on every write.** Slower, but it makes "returned successfully"
  mean "on disk," which requirement 2 depends on.
- **Standard library only.** `argparse`, `json`, `datetime`, `pathlib`, and
  `os` cover everything needed.
