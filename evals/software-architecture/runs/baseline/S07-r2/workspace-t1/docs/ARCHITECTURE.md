# Architecture

shelf is a command-line list of owned books. It uses only the Python standard library and
stores everything in one JSON file.

## Requirements and status

| # | Requirement | Status | Where |
|---|-------------|--------|-------|
| 1 | Add, list and find books by title or ISBN from the command line | Met, with a gap: ISBN lookup compares the raw stored string, so `find 0441172717` does not match a book stored as `0-441-17271-7` | `cli.py`, `catalog.find` |
| 2 | The catalog survives a crash mid-write | Partly met: a crash during the write leaves the previous file intact. The write is not fsynced, so a power loss just after the rename can still lose the update | `catalog.save` |
| 3 | Runs with only the Python standard library | Met | whole package |
| 4 | An ISBN is checked before a book is stored | Partly met: only `cli.add` checks. `catalog.add` stores anything, and `--isbn ""` skips the check and stores an empty ISBN | `cli.py`, `isbn.py` |
| 5 | Adding a command touches only `cli.py` and one new module | Met by design; see [Adding a command](#adding-a-command) | `cli.py`, `catalog.py` |

Gaps are listed again under [Known gaps](#known-gaps).

## Components

```
 user ──> __main__.py ──> cli.py ──┬──> isbn.py     (check digits, no I/O)
                                   └──> catalog.py ──> JSON file
```

| Module | Responsibility | May import |
|--------|----------------|------------|
| `shelf/__main__.py` | Entry point for `python3 -m shelf`; passes argv to `cli.main` and exits with its code | `cli` |
| `shelf/cli.py` | Parses arguments, validates input, prints results, returns the exit code | `catalog`, `isbn` |
| `shelf/catalog.py` | The only code that reads or writes the file; owns the file location and atomic write | standard library |
| `shelf/isbn.py` | Pure function `valid(text) -> bool` for ISBN-10 and ISBN-13 check digits | standard library |

`cli` calls `catalog` and never opens the file. `catalog` and `isbn` do not import `cli`.

## Data

- **Location:** `$SHELF_FILE` if set, otherwise `~/.shelf.json`.
- **Format:** a JSON array of objects, `{"title": str, "isbn": str | null}`. The ISBN is stored
  as the user typed it, hyphens included.
- **Ordering:** books are kept in insertion order. Nothing else is indexed.

## Flows

**add:** parse args → if `--isbn` is given, `isbn.valid` must be true, else print an error to
stderr and exit 1 → `catalog.add` loads the list, appends, and saves it atomically.

**list / find:** `catalog.load` or `catalog.find` → print one line per book, `Title (ISBN)` when
an ISBN is stored. `find` matches a case-insensitive substring of the title, or an exact string
equal to the stored ISBN.

**Atomic save:** write the full list to `<name>.tmp` next to the file, then `os.replace` it over
the file. Readers see either the old or the new file, never a partial one. See
[ADR 0003](decisions/0003-crash-safe-writes.md).

## Adding a command

1. In `shelf/cli.py`, register a subparser in `main` and add a branch that handles it.
2. If the command needs new storage behaviour, put it in one new module, `shelf/<command>.py`.
   It may call `catalog.load()` and `catalog.save()`, which are public. It must not open the file.
3. Add tests under `tests/`.

No other module changes. See [ADR 0005](decisions/0005-commands-in-cli-plus-one-module.md).

## Known gaps

These are the places where the code does not yet meet the design above. Fixing them is a code
change, not a documentation change.

1. **ISBN lookup is not normalised.** `find` compares the raw string, so hyphenated and bare
   forms of the same ISBN do not match. Fix: normalise both sides with `isbn.py` before comparing.
2. **Writes are not fsynced.** `catalog.save` closes the temp file without `os.fsync`, so after a
   power loss the rename can land before the data. Fix: flush and fsync the temp file, then fsync
   the directory after the rename.
3. **The ISBN check lives only in the CLI.** `catalog.add` accepts any string. Fix: move the check
   into `catalog.add` (or a single validated entry point) so every caller is covered.
4. **Empty ISBN is accepted.** `--isbn ""` is falsy, so the check is skipped and an empty ISBN is
   stored. Fix: check `args.isbn is not None`.
5. **A corrupt file is fatal.** A truncated or invalid JSON file makes every command raise a
   traceback. There is no backup or recovery path.
6. **The temp file name is fixed.** `shelf.tmp` is shared by every writer, so two concurrent
   `add` calls can interleave. Concurrent use is not a stated requirement.
