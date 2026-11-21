# Architecture

shelf is a command-line list of the books you own. It has no dependencies outside the Python
standard library.

## Requirements and how the design meets them

| # | Requirement | Design | Status |
|---|-------------|--------|--------|
| 1 | Add, list and find books by title or ISBN from the command line | `cli.py` parses `add`, `list`, `find`; `catalog.find` matches title (case-insensitive substring) or ISBN | Met for title. ISBN lookup is exact string match, so `0441172719` does not find a book stored as `0-441-17271-7` (see gaps) |
| 2 | Catalog survives a crash mid-write | `catalog.save` writes a temporary file and calls `os.replace`, which is atomic on POSIX | Met for process crashes. Not fsynced, so a power loss can still lose data (see gaps) |
| 3 | Standard library only | Only `argparse`, `json`, `os`, `pathlib`, `sys`, `unittest` are used | Met |
| 4 | An ISBN is checked before a book is stored | `cli.add` calls `isbn.valid` and exits with status 1 on failure ([ADR 0002](decisions/0002-validate-isbn-locally.md)) | Met through the CLI only; `catalog.add` stores whatever it is given (see gaps) |
| 5 | Adding a command touches only `cli.py` and one new module | See "Adding a command" below | Partly met: command dispatch lives in `cli.py`, and a command needing new storage must also change `catalog.py` |

## Modules

```
shelf/
  __main__.py  entry point: python3 -m shelf  -> cli.main(sys.argv[1:])
  cli.py       parses arguments, validates input, prints results
  catalog.py   load / save / add / find over the JSON file
  isbn.py      pure function: ISBN-10 and ISBN-13 check digits
```

Dependencies point one way:

```
__main__ -> cli -> catalog
              \-> isbn
```

- `cli` is the only module that prints or reads `sys.argv`. It never reads the file directly.
- `catalog` is the only module that touches the file. It knows nothing about argument parsing.
- `isbn` has no I/O and no state. It is the single place that defines a valid ISBN.

## Storage

- Location: `$SHELF_FILE`, or `~/.shelf.json` when unset ([ADR 0001](decisions/0001-store-books-in-one-json-file.md)).
- Format: a JSON array of objects `{"title": str, "isbn": str | null}`.
- Write path: `save` writes the full list to `<file>.tmp`, then renames it over the catalog.
  A crash before the rename leaves the previous catalog intact. A stale `.tmp` file may remain
  and is overwritten on the next save.
- Read path: `load` returns `[]` when the file does not exist. A corrupt file raises
  `json.JSONDecodeError`; nothing repairs it.
- Concurrency: none. Two simultaneous `add` calls can lose one book (read-modify-write with no lock).

## Adding a command

The intended recipe:

1. Put the command's logic in one new module (for example `shelf/remove.py`) that takes the
   parsed arguments and calls `catalog`.
2. In `cli.py`, register the subcommand with `argparse` and dispatch to the new module.

Limits of this recipe today:

- `cli.main` dispatches with an `if`/`else` chain, so each command adds a branch to `cli.py`.
  This is within the allowed files, but it grows with every command.
- If a command needs a storage operation that `catalog` does not offer (for example `remove`),
  `catalog.py` must change too. The recipe breaks there.

To make requirement 5 hold for every command, `catalog` should expose its primitives (`load`,
`save`) as a stable API, so a new command module can perform its own read-modify-write without
touching `catalog.py`. Command registration could then be a table in `cli.py`.

## Quality goals

Only goals with a measure are listed. Goals without a measure are in "Open" below.

| Goal | Measure | Current result |
|------|---------|----------------|
| Crash safety | Killing the process during `save` leaves the previous catalog loadable and unchanged | Expected to pass; not yet tested |
| Invalid ISBNs never stored | Every add with a bad check digit is rejected, through the CLI and through `catalog.add` | Fails for `catalog.add` (gap 1) |
| Lookup by ISBN in any formatting | `find` returns the book for `0441172719`, `0-441-17271-7` and `044117271x` alike | Fails (gap 2) |
| Standard library only | No import outside the standard library in `shelf/` | Passes (checked by reading the imports) |
| Cheap command extension | A new command changes `cli.py` and one new module only | Partly met (see "Adding a command") |

Open (no measure yet): ease of use of the CLI output, and how the file format evolves across
versions.

## Known gaps

These are discrepancies between the requirements and the code, found by running the tests and
the CLI. Ranked by my judgement of user impact: the first item makes a stated requirement fail
silently, the last is a limitation only under concurrent use. The code has not been changed.

1. **ISBN validation is not in the catalog** (requirement 4). `catalog.add(title, isbn)` stores any
   string. `cli.add` is the only check, so any other caller can store an invalid ISBN. Moving the
   check into `catalog.add` would make requirement 4 hold for every caller.
2. **ISBN lookup is exact** (requirement 1). `find` compares the query with the stored string.
   `shelf add Dune --isbn 0-441-17271-7` followed by `shelf find 0441172719` finds nothing.
   The ISBN should be normalised (hyphens removed, `x` upper-cased) when stored and when searched.
3. **No fsync before rename** (requirement 2). `save` does not call `os.fsync`, so after a power
   loss the renamed file may be empty or partial on some filesystems. Process crashes are safe.
4. **No locking.** Concurrent writers can lose updates.

## Documents

| Document | Role | Read it for |
|----------|------|-------------|
| `README.md` | Entry point | What shelf is, how to run it, where to look next |
| `docs/architecture.md` (this file) | Structure | Requirements, modules, storage, quality goals, gaps |
| `docs/decisions/0001-…` | ADR | Why storage is one JSON file |
| `docs/decisions/0002-…` | ADR | Why ISBNs are checked locally |

ADRs follow the same shape: Status, Context, Decision, Consequences. Add a new ADR when a decision
changes the modules, the storage format or a requirement.
