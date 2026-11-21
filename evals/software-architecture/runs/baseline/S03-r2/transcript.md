### user

I've reviewed the open ADRs. ADR-0004 is approved. ADR-0005 is rejected: we will not run a
second storage engine, a server database contradicts R-3. One more change: we're moving off
SQLite. Notes will be stored as one JSON file per note, because SQLite files are hard to diff
and repair by hand. Update the decision records accordingly. I'm not available for questions.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200",
 "description": "Show repo status, history and file list"
}
```

### tool_result

```
14bfb8f fixture
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
 "command": "for f in docs/adr/*.md; do echo \"=== $f\"; cat \"$f\"; echo; done; echo \"=== GLOSSARY\"; cat GLOSSARY.md; echo \"=== README\"; cat README.md",
 "description": "Read all ADRs, glossary and README"
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

=== GLOSSARY
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
=== README
# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
```

### tool_use Bash

```json
{
 "command": "cat docs/architecture/arc42.md; echo \"=== store.py\"; cat notes/store.py; echo \"=== model.py\"; cat notes/model.py; echo \"=== cli.py\"; cat notes/cli.py; echo \"=== tests\"; cat tests/test_notes.py",
 "description": "Read architecture doc and source files"
}
```

### tool_result

```
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
=== store.py
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
        return Note(cur.lastrowid, text, created)

    def all(self):
        rows = self._db.execute("SELECT id, text, created FROM notes ORDER BY id")
        return [Note(*row) for row in rows]

    def search(self, term):
        rows = self._db.execute("SELECT id, text, created FROM notes WHERE text LIKE ? ORDER BY id",
                                (f"%{term}%",))
        return [Note(*row) for row in rows]

    def close(self):
        self._db.close()
=== model.py
from dataclasses import dataclass


@dat
[... 2364 chars cut]
```

### assistant

I have the full picture: ADR-0001 (SQLite), ADR-0004 (proposed, approved), ADR-0005 (PostgreSQL, rejected), and the arc42 doc. I'll read the ADR files with the file tool before editing them.

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-k4_p0lio/project/docs/adr/0001-use-sqlite-for-storage.md"
}
```

### tool_result

```
1	# 1. Use SQLite for storage
2	
3	## Status
4	
5	accepted 2026-10-01
6	
7	## Context
8	
9	Notes must survive crashes (R-2, QG-1, QS-1) and the program may use only the Python standard
10	library (R-3, QG-2). The standard library ships `sqlite3`, whose transactions are atomic.
11	
12	## Decision
13	
14	Store all notes in one SQLite database file, by default `~/.notes.db`.
15	
16	## Consequences
17	
18	Crash safety comes from SQLite transactions. The file is binary, so it cannot be read or
19	repaired with a text editor.
20	
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-k4_p0lio/project/docs/adr/0004-write-notes-atomically.md"
}
```

### tool_result

```
1	# 4. Write notes atomically via a temporary file and rename
2	
3	## Status
4	
5	proposed
6	
7	## Context
8	
9	QS-1 requires that a crash during `add` leaves the store readable (R-2, QG-1). Any file the
10	store writes besides the database (for example an export) must meet the same rule.
11	
12	## Decision
13	
14	Every file the store writes is written to a temporary file in the same directory, flushed with
15	`os.fsync`, and moved into place with `os.replace`.
16	
17	## Consequences
18	
19	A crash leaves either the old file or the new one, never a partial file. Writes cost one extra
20	`fsync`.
21	
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-k4_p0lio/project/docs/adr/0005-add-postgresql-backend.md"
}
```

### tool_result

```
1	# 5. Add a PostgreSQL backend
2	
3	## Status
4	
5	proposed
6	
7	## Context
8	
9	Users with many notes asked for faster search (R-1).
10	
11	## Decision
12	
13	Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.
14	
15	## Consequences
16	
17	Needs the `psycopg` package and a running database server.
18	
```

### assistant

Decisions I'm making, since you're not available for questions:
- ADR-0001 is marked superseded by a new ADR-0006, not rewritten, so the history stays intact.
- The new ADR sets the notes directory to `~/.notes/` (overridable with `NOTES_DIR`, replacing `NOTES_DB`), with one `<id>.json` file per note.

Updating the records now.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-k4_p0lio/project/docs/adr/0001-use-sqlite-for-storage.md",
 "old_string": "accepted 2026-10-01\n",
 "new_string": "superseded by [ADR-0006](0006-store-notes-as-json-files.md) on 2026-11-21 (was accepted 2026-10-01)\n"
}
```

### tool_result

```
The file /tmp/sa-eval-k4_p0lio/project/docs/adr/0001-use-sqlite-for-storage.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-k4_p0lio/project/docs/adr/0004-write-notes-atomically.md",
 "old_string": "proposed\n\n## Context\n\nQS-1 requires that a crash during `add` leaves the store readable (R-2, QG-1). Any file the\nstore writes besides the database (for example an export) must meet the same rule.",
 "new_string": "accepted 2026-11-21\n\n## Context\n\nQS-1 requires that a crash during `add` leaves the store readable (R-2, QG-1). Every note\nfile in the store, and any other file the store writes (for example an export), must meet the\nsame rule. Under [ADR-0006](0006-store-notes-as-json-files.md) each note is one file, so this\nrule is what keeps a note from being half-written."
}
```

### tool_result

```
The file /tmp/sa-eval-k4_p0lio/project/docs/adr/0004-write-notes-atomically.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-k4_p0lio/project/docs/adr/0005-add-postgresql-backend.md",
 "old_string": "proposed\n\n## Context",
 "new_string": "rejected 2026-11-21\n\nWe will not run a second storage engine. A server database contradicts R-3 (runs with only the\nPython standard library, no installation). Search speed is not addressed here; see the\n[storage decision in ADR-0006](0006-store-notes-as-json-files.md).\n\n## Context"
}
```

### tool_result

```
The file /tmp/sa-eval-k4_p0lio/project/docs/adr/0005-add-postgresql-backend.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### assistant

I wrote a link in ADR-0005 that implies ADR-0006 addresses search speed, and it doesn't. I'll correct that sentence.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-k4_p0lio/project/docs/adr/0005-add-postgresql-backend.md",
 "old_string": "Python standard library, no installation). Search speed is not addressed here; see the\n[storage decision in ADR-0006](0006-store-notes-as-json-files.md).",
 "new_string": "Python standard library, no installation). The search-speed request behind this ADR (R-1) is\nstill open; this rejection does not address it."
}
```

### tool_result

```
The file /tmp/sa-eval-k4_p0lio/project/docs/adr/0005-add-postgresql-backend.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-k4_p0lio/project/docs/adr/0006-store-notes-as-json-files.md",
 "content": "# 6. Store notes as one JSON file per note\n\n## Status\n\naccepted 2026-11-21\n\nSupersedes [ADR-0001](0001-use-sqlite-for-storage.md).\n\n## Context\n\nSQLite stores all notes in one binary file. That file is hard to diff and cannot be repaired by\nhand with a text editor. Crash safety (R-2, QG-1, QS-1) and the standard-library-only rule\n(R-3, QG-2) still apply. [ADR-0004](0004-write-notes-atomically.md) gives a safe write for any\nsingle file, so one file per note keeps crash safety without a database.\n\n## Decision\n\nStore each note as its own file in the notes directory, `~/.notes/` by default, overridable\nwith `NOTES_DIR` (this replaces `NOTES_DB`).\n\n- File name: `<id>.json`, where `<id>` is the note id.\n- File content: a JSON object with the fields `id` (integer), `text` (string) and `created`\n  (UTC timestamp, ISO 8601, seconds precision).\n- Every note file is written as ADR-0004 requires.\n\nOnly `notes/store.py` reads or writes these files (ADR-0003).\n\n## Consequences\n\n- A note can be read, diffed and repaired with a text editor.\n- Crash safety comes from ADR-0004: a crash leaves each note either fully stored or absent.\n- Listing and searching read every note file. This is slower than a database index for very\n  large collections. It is accepted for now; see the open search-speed request (R-1) in\n  [ADR-0005](0005-add-postgresql-backend.md).\n- `NOTES_DB` and `~/.notes.db` no longer apply. Existing SQLite data is not migrated by this\n  decision; any migration is a separate decision.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-k4_p0lio/project/docs/adr/0006-store-notes-as-json-files.md (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "git status --short && git diff --stat && sed -n 1,12p docs/adr/0005-add-postgresql-backend.md",
 "description": "Show changed files and verify ADR-0005 header"
}
```

### tool_result

```
 M docs/adr/0001-use-sqlite-for-storage.md
 M docs/adr/0004-write-notes-atomically.md
 M docs/adr/0005-add-postgresql-backend.md
?? docs/adr/0006-store-notes-as-json-files.md
 docs/adr/0001-use-sqlite-for-storage.md | 2 +-
 docs/adr/0004-write-notes-atomically.md | 8 +++++---
 docs/adr/0005-add-postgresql-backend.md | 6 +++++-
 3 files changed, 11 insertions(+), 5 deletions(-)
# 5. Add a PostgreSQL backend

## Status

rejected 2026-11-21

We will not run a second storage engine. A server database contradicts R-3 (runs with only the
Python standard library, no installation). The search-speed request behind this ADR (R-1) is
still open; this rejection does not address it.

## Context
```

### assistant

The decision records now reflect your choices. The code, tests and README still use SQLite, so they don't match yet.

**Changes in `docs/adr/`:**
- **ADR-0004** (atomic writes): status is now `accepted 2026-11-21`. Its context now covers every note file, since each note is a file under the new decision.
- **ADR-0005** (PostgreSQL): status is `rejected 2026-11-21`. The reason is recorded: a second storage engine, and a server database contradicts R-3. The search-speed request behind it (R-1) is noted as still open.
- **ADR-0006** (new, `store-notes-as-json-files.md`): accepted 2026-11-21, supersedes ADR-0001. It records one JSON file per note, named `<id>.json`, with fields `id`, `text` and `created`. Writes follow ADR-0004.
- **ADR-0001** (SQLite): status is now superseded by ADR-0006. The text is unchanged, so the history stays readable.

**Choices I made that you should check:**
- The notes directory is `~/.notes/`, overridable with `NOTES_DIR`, which replaces `NOTES_DB`.
- Existing SQLite data is not migrated. The ADR says any migration is a separate decision.
- Search and list read every file. The ADR accepts this for now and says so under consequences.

**Not changed, because they aren't decision records:**
- `notes/store.py` still uses `sqlite3`. This is the main gap, and ADR-0003 (only `store.py` touches storage) is still the right boundary for the rewrite.
- `tests/test_notes.py` still builds a `.db` file.
- `README.md` still describes `~/.notes.db` and `NOTES_DB`.
- `docs/architecture/arc42.md` has no storage details to update, so I left it alone.

Nothing is committed. The changes are in the working tree: three modified ADRs and one new file.

### result (success)
