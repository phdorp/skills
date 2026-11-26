# Architecture

pantry is a single-user command-line tool. It records pantry items with an expiry date and lists what expires soon. It is a small Python package with no third-party dependencies.

This document describes the code as it is today. Section [Known gaps](#known-gaps) lists where the code does not yet meet the requirements.

## Requirements

These constrain every design decision below.

1. Users add pantry items with an expiry date and list what expires soon, from the command line.
2. No item is lost if the machine crashes mid-write.
3. Runs with only the Python standard library.
4. A new command touches only `cli.py` and at most one new module.

## Module map

```
pantry/
  __main__.py   python3 -m pantry entry point; calls cli.main and exits with its code
  cli.py        argument parsing, command dispatch, output, exit codes
  dates.py      parses user date input into datetime.date
  model.py      Item value type, event records, replay of events into current items
  store.py      the storage file: append events, read events back
tests/
  test_pantry.py  unit tests (unittest) for dates, store round trips, CLI behaviour
```

Dependency direction is one way:

```
__main__ -> cli -> dates
                -> store -> model
                 cli  -> model (Item)
```

- `model` imports nothing from the package. It knows about items and events, not files.
- `store` knows where the file is and how to read and write it. It depends on `model` for event records and replay. It knows nothing about the CLI.
- `dates` is pure: it takes an optional `today` so tests do not depend on the clock.
- `cli` is the only module that prints or reads `sys.argv`. It returns an exit code; it never calls `sys.exit` itself (`__main__` does).

## Data model

An `Item` is a frozen dataclass with `name: str` and `expires: date`. The name is the identity: two adds with the same name refer to the same item, and the later one sets the expiry.

The file is an event log, not a snapshot. Each line is one JSON object:

```json
{"op": "add", "name": "Milk", "expires": "2026-11-25"}
{"op": "remove", "name": "Milk"}
```

The current pantry is derived by `model.replay`, which applies the events in order: `add` sets `items[name]`, `remove` pops it. Lines with any other `op` are ignored, so older code can read a log that newer code has extended with new event types.

## Storage

Location: `$PANTRY_FILE` if set, otherwise `~/.pantry.jsonl`.

Writes are appends only. `store._append` opens the file in append mode, writes one line, flushes, and calls `os.fsync`. Nothing is rewritten in place, so earlier lines are never touched by a later write. That is the basis of requirement 2.

Reads (`store._records`) parse each line independently. A line that does not parse as JSON is skipped. This is how a line cut short by a crash is tolerated.

There is no lock. Two concurrent `pantry` processes can interleave appends.

## Command flow

Entry: `python3 -m pantry <args>` runs `__main__`, which calls `cli.main(argv)`.

| Command | Path |
|---|---|
| `add NAME DATE` | `dates.parse` converts `DATE` to a `date` (on `ValueError`, print an error and exit 1). Then `store.add(Item)` appends an `add` event. |
| `remove NAME` | `store.items()` is checked for `NAME` (missing: print an error and exit 1). Then `store.remove` appends a `remove` event. |
| `list [--soon DAYS]` | `store.items()` replays the log. Items are sorted by `(expires, name lower-cased)`. With `--soon`, items with `expires <= today + DAYS` are kept. Items already past their date are included, so they show up at the top. |

Every command reads the whole file. This is fine for a pantry-sized log and keeps the code simple. A log grows with every add and remove, so it is never compacted.

Exit codes (set in `cli.main`): `0` success, `1` user error (bad date, unknown item), `2` bad usage (argparse error, unknown command). `--help` exits 0.

Output: `list` prints `YYYY-MM-DD  Name`, one item per line. Errors go to stderr.

## Date input

`dates.parse` accepts, case-insensitively and after stripping whitespace:

- `today`, `tomorrow`
- `+Nd` and `+Nw` (N days or weeks from today)
- `YYYY-MM-DD` (anything `date.fromisoformat` accepts)

Anything else raises `ValueError`. Dates are local calendar dates; there is no time of day or time zone.

## Adding a command (requirement 4)

The rule: a new command changes `cli.py` (a subparser in `main` and a branch that dispatches to it) and at most one new module that holds its logic. It should not need changes to `store.py` or `model.py`.

That is possible only if the command can be built from what the store already offers: `store.items()`, `store.add(Item)`, `store.remove(name)`. Commands that only read the pantry (such as a `show` or a different filter) meet this rule. Commands that change an existing item in a new way do not. An `edit` or `rename` command needs a new event type, which means changes to `model.replay` and to the store API, so it breaks requirement 4 as the code stands. See [Open decisions](#open-decisions).

## Testing

`python3 -m unittest` runs `tests/test_pantry.py`. Each test points `PANTRY_FILE` at a fresh temporary file. The tests cover relative dates, add/remove replay, a torn last line being skipped, `list --soon` ordering, and exit codes.

No test covers a torn line followed by a further write (see Known gaps).

## Known gaps

1. **A torn line can swallow the next record (requirement 2 is not met).** If a crash leaves a partial line with no trailing newline, the next append is written onto the same physical line. Both records are then unparseable, and the new item is silently lost. Reproduced: after `add Rice`, a partial line `{"op": "add", "na` appended, then `add Milk` succeeds with exit 0, but `list` shows only Rice. The fix belongs in `store._append`: if the file does not end in `\n`, write a newline before the record (or truncate the partial tail). A test should cover this case.
2. **The directory is not fsynced when the file is created.** `os.fsync` on the file makes its data durable, but on a crash the first write to a new file can leave the directory entry missing, so the file, and its first item, could disappear. Fix: fsync the parent directory after creating the file.
3. **Concurrent writers are unguarded.** Two processes appending at once may interleave. Nothing here is protected by a lock.
4. **Unknown ops are silently ignored.** Helpful for forward compatibility, but a typo in an op name loses that event without any warning.

## Open decisions

- **How to support update-type commands within requirement 4.** Options: (a) allow `model.py` and `store.py` to change for such commands and relax requirement 4 for them; (b) make the store a generic "append event" function so a new command can define its own event type in its own module and register a replay rule. Option (b) keeps the rule but moves replay into a registry, which is more machinery than the code needs today.
- **Compaction.** The log only grows. Acceptable for now; if it ever matters, rewrite it atomically (write a temp file, fsync, `os.replace`). That is the one place the append-only approach cannot be used.
