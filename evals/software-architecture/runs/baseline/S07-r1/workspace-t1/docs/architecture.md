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

## Known gaps

These are discrepancies between the requirements and the code, found by running the tests and
the CLI. The code has not been changed.

1. **ISBN validation is not in the catalog.** `catalog.add(title, isbn)` stores any string.
   `cli.add` is the only check, so any other caller can store an invalid ISBN. Moving the check
   into `catalog.add` would make requirement 4 hold for every caller.
2. **ISBN lookup is exact.** `find` compares the query with the stored string.
   `shelf add Dune --isbn 0-441-17271-7` followed by `shelf find 0441172719` finds nothing.
   The ISBN should be normalised (hyphens removed, `x` upper-cased) when stored and when searched.
3. **No fsync before rename.** `save` does not call `os.fsync`, so after a power loss the renamed
   file may be empty or partial on some filesystems. Process crashes are safe.
4. **No locking.** Concurrent writers can lose updates.

## Decisions

- [0001 — Store books in one JSON file](decisions/0001-store-books-in-one-json-file.md)
- [0002 — Validate ISBNs locally](decisions/0002-validate-isbn-locally.md)
