### user

I've reviewed the open ADRs. ADR-0004 is approved. ADR-0005 is rejected: we will not run a
second storage engine, a server database contradicts R-3. One more change: we're moving off
SQLite. Notes will be stored as one JSON file per note, because SQLite files are hard to diff
and repair by hand. Update the decision records accordingly. I'm not available for questions.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200",
 "description": "Show repo status and list files"
}
```

### tool_result

```
d5f8f66 fixture
./README.md
./GLOSSARY.md
./notes/__main__.py
./notes/cli.py
./notes/store.py
./notes/__init__.py
./notes/model.py
./tests/test_notes.py
./tests/__init__.py
./docs/adr/0004-write-notes-atomically.md
./docs/adr/0002-record-architecture-decisions.md
./docs/adr/0005-add-postgresql-backend.md
./docs/adr/0003-cli-reaches-storage-only-through-store.md
./docs/adr/0001-use-sqlite-for-storage.md
./docs/architecture/arc42.md
```

### tool_use Bash

```json
{
 "command": "for f in docs/adr/*.md; do echo \"=== $f\"; cat \"$f\"; echo; done",
 "description": "Read all ADR files"
}
```

### tool_result

```
=== docs/adr/0001-use-sqlite-for-storage.md
# 1. Use SQLite for storage

## Status

accepted 2026-10-01

## Context

Notes must survive crashes (R-2, QG-1, QS-1) and the program may use only the Python standard
library (R-3, QG-2). The standard library ships `sqlite3`, whose transactions are atomic.

## Decision

Store all notes in one SQLite database file, by default `~/.notes.db`.

## Consequences

Crash safety comes from SQLite transactions. The file is binary, so it cannot be read or
repaired with a text editor.

=== docs/adr/0002-record-architecture-decisions.md
# 2. Record architecture decisions

## Status

accepted 2026-10-01

## Context

The architect decides the architecture; contributors and agents implement it. We need a line
between decisions the architect makes centrally and decisions left to whoever builds a block
(R-1, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the storage engine and the on-disk format;
- the dependency rule between blocks: `cli` → `store` → `model`;
- import and export formats;
- CLI command names and exit codes;
- third-party dependencies.

Left to the building blocks (no ADR): internal helpers, SQL query structure, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.

=== docs/adr/0003-cli-reaches-storage-only-through-store.md
# 3. CLI reaches storage only through the store module

## Status

accepted 2026-10-01

## Context

Contributors should be able to swap the storage engine by changing one module (QG-3, QS-3).

## Decision

Only `notes/store.py` imports `sqlite3` or touches the database file. `notes/cli.py` uses the
`Store` class and the `Note` value.

## Consequences

Any new command that reads or writes notes goes through `Store`.

=== docs/adr/0004-write-notes-atomically.md
# 4. Write notes atomically via a temporary file and rename

## Status

proposed

## Context

QS-1 requires that a crash during `add` leaves the store readable (R-2, QG-1). Any file the
store writes besides the database (for example an export) must meet the same rule.

## Decision

Every file the store writes is written to a temporary file in the same directory, flushed with
`os.fsync`, and moved into place with `os.replace`.

## Consequences

A crash leaves either the old file or the new one, never a partial file. Writes cost one extra
`fsync`.

=== docs/adr/0005-add-postgresql-backend.md
# 5. Add a PostgreSQL backend

## Status

proposed

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.
```

### tool_use Bash

```json
{
 "command": "cat README.md GLOSSARY.md docs/architecture/arc42.md && echo ===STORE && cat notes/store.py && echo ===MODEL && cat notes/model.py",
 "description": "Read docs, store and model code"
}
```

### tool_result

```
# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
# notes: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add, list and search notes from the command line. | 1 | active | core use |
| R-2 | No note is lost when the process or machine crashes. | 2 | active | users keep notes for years |
| R-3 | Runs on Linux and macOS with only the Python standard library. | 3 | active | installed on locked-down machines |
| R-4 | Notes sync between a user's devices. | - | deferred | needs a server; revisit next year |
| R-5 | A graphical user interface. | - | rejected | the CLI audience does not want one |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-2 | QS-1 |
| QG-2 | Portability: installability | R-3 | QS-2 |
| QG-3 | Maintainability: modifiability | R-1 | QS-3 |

### Stakeholders

| role | expectation |
|---|---|
| Architect (project owner) | decides the architecture; accepts ADRs |
| Users | keep notes for years without losing any |
| Contributors | change one part without learning the whole program |

## 2. Constraints

- Python 3.11 or later, standard library only (R-3).

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|
| `cli` | parse commands, print results and errors | `store`, `model` |
| `store` | keep notes between runs; the only block that knows the storage | `model` |
| `model` | the `Note` value | - |

## 6. Runtime view

## 7. Deployment view

## 8. Crosscutting concepts

- Errors: reported on stderr as `notes: <message>`, exit code 1.

## 9. Architecture decisions

Decisions are recorded as ADRs in [docs/adr/](../adr/). What is decided centrally is listed in
[ADR-0002 Record architecture decisions](../adr/0002-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the note is either fully stored or absent; the store still opens | 0 unreadable stores in 100 trials |
| QS-2 | QG-2 | a user runs `python3 -m notes list` | fresh Linux or macOS with Python 3.11+ | it works without installing anything | 0 install steps |
| QS-3 | QG-3 | a contributor swaps the storage engine | development | only `notes/store.py` and its tests change | 0 other files changed |

## 11. Risks and technical debt

## 12. Glossary

See [GLOSSARY.md](../../GLOSSARY.md).
===STORE
"""The only module that knows how notes are stored (ADR-0001, ADR-0003)."""
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from notes.model import Note


def default_path():
    return Path(os.environ.get("NOTES_DB", Path.home() / ".notes.db"))


class Store:
    def __init__(self, path):
        self._db = sqlite3.connect(path)
        self._db.execute("CREATE TABLE IF NOT EXISTS notes "
                         "(id INTEGER PRIMARY KEY, text TEXT NOT NULL, created TEXT NOT NULL)")

    def add(self, text):
        created = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with self._db:
            cur = self._db.execute("INSERT INTO notes (text, created) VALUES (?, ?)",
                                   (text, created))
        return Note(cur.lastrowid, text, cre
[... 545 chars cut]
```

### assistant

Before editing, here's what the records show: ADR-0001 chose SQLite, ADR-0002 says the storage engine and on-disk format are decided centrally by ADR, and ADR-0003 confines storage code to `notes/store.py`. The change needs a new ADR that supersedes ADR-0001, not an edit to its body.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-_cwb_fqo/project/docs/adr/0006-store-each-note-as-a-json-file.md",
 "content": "# 6. Store each note as one JSON file\n\n## Status\n\naccepted 2026-11-21, supersedes [ADR-0001](0001-use-sqlite-for-storage.md)\n\n## Context\n\nSQLite files are binary. They are hard to diff and cannot be repaired with a text editor, which\nthe users and maintainers need when a store goes wrong. Crash safety must still hold (R-2, QG-1,\nQS-1), and the program may use only the Python standard library (R-3, QG-2). The `json` module\nis in the standard library, and ADR-0004 already gives an atomic write for any file the store\nwrites.\n\nA second storage engine is not wanted: ADR-0005 (PostgreSQL) is rejected, because a server\ndatabase contradicts R-3.\n\n## Decision\n\nThe store keeps each note in its own file in one directory:\n\n- the directory is `~/.notes/` by default; the environment variable `NOTES_DIR` sets another one;\n- the file name is `<id>.json`, where `<id>` is the note's integer id;\n- the file holds one JSON object with the keys `id` (integer), `text` (string) and `created`\n  (ISO 8601 UTC timestamp, whole seconds);\n- a new note gets the id one higher than the highest existing id, starting at 1;\n- every file is written as ADR-0004 requires: temporary file in the same directory, `os.fsync`,\n  then `os.replace`.\n\nOnly `notes/store.py` reads or writes these files (ADR-0003).\n\n## Consequences\n\n- Each note can be read, diffed and repaired with a text editor.\n- A crash leaves each note either fully written or absent, as before.\n- `os.replace` overwrites silently, so creating a note must not replace an existing file. The\n  mechanism is left to the building block.\n- Search reads every note file. This is acceptable for the current use (R-1) and is the first\n  place to look if search becomes slow.\n- The `NOTES_DB` variable, the file `~/.notes.db` and the `notes` table are gone. Migrating an\n  existing `~/.notes.db` is not decided in this ADR and needs its own decision.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-_cwb_fqo/project/docs/adr/0006-store-each-note-as-a-json-file.md (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-_cwb_fqo/project/docs/adr/0001-use-sqlite-for-storage.md",
 "old_string": "accepted 2026-10-01",
 "new_string": "superseded 2026-11-21 by [ADR-0006](0006-store-each-note-as-a-json-file.md)"
}
```

### tool_result

```
The file /tmp/sa-eval-_cwb_fqo/project/docs/adr/0001-use-sqlite-for-storage.md has been updated successfully.
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-_cwb_fqo/project/docs/adr/0004-write-notes-atomically.md",
 "old_string": "proposed",
 "new_string": "accepted 2026-11-21"
}
```

### tool_result

```
The file /tmp/sa-eval-_cwb_fqo/project/docs/adr/0004-write-notes-atomically.md has been updated successfully.
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-_cwb_fqo/project/docs/adr/0005-add-postgresql-backend.md",
 "old_string": "proposed\n\n## Context",
 "new_string": "rejected 2026-11-21\n\nWe will not run a second storage engine. A server database contradicts R-3.\n\n## Context"
}
```

### tool_result

```
The file /tmp/sa-eval-_cwb_fqo/project/docs/adr/0005-add-postgresql-backend.md has been updated successfully.
```

### tool_use Bash

```json
{
 "command": "git status --short && grep -n \"^accepted\\|^rejected\\|^superseded\\|^proposed\" docs/adr/*.md",
 "description": "Check changed files and ADR status lines"
}
```

### tool_result

```
 M docs/adr/0001-use-sqlite-for-storage.md
 M docs/adr/0004-write-notes-atomically.md
 M docs/adr/0005-add-postgresql-backend.md
?? docs/adr/0006-store-each-note-as-a-json-file.md
docs/adr/0001-use-sqlite-for-storage.md:5:superseded 2026-11-21 by [ADR-0006](0006-store-each-note-as-a-json-file.md)
docs/adr/0004-write-notes-atomically.md:5:accepted 2026-11-21
docs/adr/0002-record-architecture-decisions.md:5:accepted 2026-10-01
docs/adr/0003-cli-reaches-storage-only-through-store.md:5:accepted 2026-10-01
docs/adr/0005-add-postgresql-backend.md:5:rejected 2026-11-21
docs/adr/0006-store-each-note-as-a-json-file.md:5:accepted 2026-11-21, supersedes [ADR-0001](0001-use-sqlite-for-storage.md)
```

### assistant

I updated the decision records. Nothing is committed.

- **ADR-0004** (atomic writes) is now `accepted 2026-11-21`.
- **ADR-0005** (PostgreSQL) is now `rejected 2026-11-21`, with one line saying a second storage engine would contradict R-3.
- **ADR-0001** (SQLite) is now `superseded 2026-11-21 by ADR-0006`. I left its body unchanged.
- **ADR-0006** (new, `docs/adr/0006-store-each-note-as-a-json-file.md`) is `accepted 2026-11-21` and records the decision. ADR-0002 says the on-disk format needs an ADR, which is why this is a new record and not a rewrite.

Choices I made in ADR-0006 that you did not specify, so you can redirect them:
- Directory `~/.notes/`, overridable with `NOTES_DIR`.
- Files named `<id>.json`. Each holds `id`, `text` and `created`.
- Ids are assigned as the highest existing id plus one.
- Each write follows ADR-0004 (temp file, fsync, `os.replace`).

Open items:
- **Migration of an existing `~/.notes.db` is not decided.** ADR-0006 says so and leaves it to a separate decision.
- **ADR-0003** still says only `store.py` imports `sqlite3`. Its rule (only the store touches storage) still holds, so I did not edit it. Say if you want the wording changed.
- **Code and docs still describe SQLite.** `notes/store.py`, `README.md` (the `~/.notes.db` and `NOTES_DB` references) and the tests are unchanged, since you asked only for the decision records. They will need changing when this is implemented.
- **ADR-0004's context** says "any file the store writes besides the database". That is now slightly off, but I left it as approved.

### result (success)
