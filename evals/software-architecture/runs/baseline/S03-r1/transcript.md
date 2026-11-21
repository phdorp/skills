### user

I've reviewed the open ADRs. ADR-0004 is approved. ADR-0005 is rejected: we will not run a
second storage engine, a server database contradicts R-3. One more change: we're moving off
SQLite. Notes will be stored as one JSON file per note, because SQLite files are hard to diff
and repair by hand. Update the decision records accordingly. I'm not available for questions.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200",
 "description": "Show repo state and list files"
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
 "command": "cat docs/architecture/arc42.md; echo ===README; cat README.md; echo ===GLOSSARY; cat GLOSSARY.md",
 "description": "Read architecture doc, README, and glossary"
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
===README
# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
===GLOSSARY
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
```

### tool_use Bash

```json
{
 "command": "cat notes/store.py notes/model.py; grep -rn -i \"sqlite\\|sql\\|postgres\\|json\" --include=*.py --include=*.md . | grep -v \"^./.git/\"",
 "description": "Read storage code and search for DB references"
}
```

### tool_result

```
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
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str
docs/adr/0002-record-architecture-decisions.md:25:Left to the building blocks (no ADR): internal helpers, SQL query structure, test layout.
notes/store.py:3:import sqlite3
notes/store.py:16:        self._db = sqlite3.connect(path)
docs/adr/0003-cli-reaches-storage-only-through-store.md:13:Only `notes/store.py` imports `sqlite3` or touches the database file. `notes/cli.py` uses the
docs/adr/0005-add-postgresql-backend.md:1:# 5. Add a PostgreSQL backend
docs/adr/0005-add-postgresql-backend.md:13:Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.
docs/adr/0001-use-sqlite-for-storage.md:1:# 1. Use SQLite for storage
docs/adr/0001-use-sqlite-for-storage.md:10:library (R-3, QG-2). The standard library ships `sqlite3`, whose transactions are atomic.
docs/adr/0001-use-sqlite-for-storage.md:14:Store all notes in one SQLite database file, by default `~/.notes.db`.
docs/adr/0001-use-sqlite-for-storage.md:18:Crash safety comes from SQLite transactions. The file is binary, so it cannot be read or
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-ro65rbca/project/docs/adr/0006-store-notes-as-json-files.md",
 "content": "# 6. Store notes as one JSON file per note\n\n## Status\n\naccepted 2026-11-21, supersedes [ADR-0001](0001-use-sqlite-for-storage.md)\n\n## Context\n\nSQLite files are binary: they are hard to diff and cannot be repaired with a text editor. Users\nneed to inspect and fix their notes by hand (R-2, QG-1). Crash safety must still hold (QS-1),\nand the program may use only the Python standard library (R-3, QG-2). A server database\ncontradicts R-3, so it is not an option ([ADR-0005](0005-add-postgresql-backend.md) is rejected).\n\n## Decision\n\nStore each note in its own JSON file inside a store directory, by default `~/.notes/`, which\n`NOTES_DIR` can override. A file is named `<id>.json` and holds the keys `id`, `text` and\n`created`.\n\nEvery file is written as [ADR-0004](0004-write-notes-atomically.md) requires: a temporary file,\n`os.fsync`, then the final name.\n\n- A new note is published with `os.link` from the temporary file to `<id>.json`. `os.link`\n  fails if the name already exists, so two processes can never overwrite each other's note. On\n  failure the store takes the next free id and retries.\n- Ids are integers: one more than the highest existing id, starting at 1.\n\nOnly `notes/store.py` reads or writes these files ([ADR-0003](0003-cli-reaches-storage-only-through-store.md)).\n\n## Consequences\n\nA crash leaves each note either fully written or absent, as before, and a user can open, diff\nand correct any note in a text editor.\n\n`search` and `all` read every file, so search time grows with the number of notes. This gives\nup the faster search that motivated ADR-0005.\n\nThis ADR does not migrate notes from `~/.notes.db` or the `NOTES_DB` variable; a migration is a\nseparate change.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-ro65rbca/project/docs/adr/0006-store-notes-as-json-files.md (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "cd /tmp/sa-eval-ro65rbca/project/docs/adr && python3 - <<'EOF'\nimport re\ndef sub(path, old, new, count=1):\n    s = open(path).read()\n    assert s.count(old) == count, (path, old, s.count(old))\n    open(path, \"w\").write(s.replace(old, new))\n\nsub(\"0001-use-sqlite-for-storage.md\", \"accepted 2026-10-01\",\n    \"superseded 2026-11-21 by [ADR-0006](0006-store-notes-as-json-files.md)\")\nsub(\"0004-write-notes-atomically.md\", \"proposed\", \"accepted 2026-11-21\")\nsub(\"0005-add-postgresql-backend.md\", \"proposed\",\n    \"rejected 2026-11-21. A database server contradicts R-3 (standard library only).\")\nsub(\"0003-cli-reaches-storage-only-through-store.md\",\n    \"Only `notes/store.py` imports `sqlite3` or touches the database file. `notes/cli.py` uses the\",\n    \"Only `notes/store.py` reads or writes the note files. `notes/cli.py` uses the\")\nEOF\ncd /tmp/sa-eval-ro65rbca/project && git diff && git status --short",
 "description": "Create ADR-0006 and update statuses of ADRs 0001, 0003-0005"
}
```

### tool_result

```
diff --git a/docs/adr/0001-use-sqlite-for-storage.md b/docs/adr/0001-use-sqlite-for-storage.md
index da5f92c..d245a56 100644
--- a/docs/adr/0001-use-sqlite-for-storage.md
+++ b/docs/adr/0001-use-sqlite-for-storage.md
@@ -2,7 +2,7 @@
 
 ## Status
 
-accepted 2026-10-01
+superseded 2026-11-21 by [ADR-0006](0006-store-notes-as-json-files.md)
 
 ## Context
 
diff --git a/docs/adr/0003-cli-reaches-storage-only-through-store.md b/docs/adr/0003-cli-reaches-storage-only-through-store.md
index a919305..02f9d53 100644
--- a/docs/adr/0003-cli-reaches-storage-only-through-store.md
+++ b/docs/adr/0003-cli-reaches-storage-only-through-store.md
@@ -10,7 +10,7 @@ Contributors should be able to swap the storage engine by changing one module (Q
 
 ## Decision
 
-Only `notes/store.py` imports `sqlite3` or touches the database file. `notes/cli.py` uses the
+Only `notes/store.py` reads or writes the note files. `notes/cli.py` uses the
 `Store` class and the `Note` value.
 
 ## Consequences
diff --git a/docs/adr/0004-write-notes-atomically.md b/docs/adr/0004-write-notes-atomically.md
index b337c8d..41b7965 100644
--- a/docs/adr/0004-write-notes-atomically.md
+++ b/docs/adr/0004-write-notes-atomically.md
@@ -2,7 +2,7 @@
 
 ## Status
 
-proposed
+accepted 2026-11-21
 
 ## Context
 
diff --git a/docs/adr/0005-add-postgresql-backend.md b/docs/adr/0005-add-postgresql-backend.md
index 5cc28b0..005873d 100644
--- a/docs/adr/0005-add-postgresql-backend.md
+++ b/docs/adr/0005-add-postgresql-backend.md
@@ -2,7 +2,7 @@
 
 ## Status
 
-proposed
+rejected 2026-11-21. A database server contradicts R-3 (standard library only).
 
 ## Context
 
 M docs/adr/0001-use-sqlite-for-storage.md
 M docs/adr/0003-cli-reaches-storage-only-through-store.md
 M docs/adr/0004-write-notes-atomically.md
 M docs/adr/0005-add-postgresql-backend.md
?? docs/adr/0006-store-notes-as-json-files.md
```

### assistant

The decision records are updated. I did not change code, tests, README, or arc42, and I did not commit.

**Changes in `docs/adr/`:**
- **ADR-0004** (atomic writes): status is now `accepted 2026-11-21`.
- **ADR-0005** (PostgreSQL): status is now `rejected 2026-11-21`, with the reason that a database server contradicts R-3.
- **ADR-0001** (SQLite): status is now `superseded 2026-11-21 by ADR-0006`. The body is unchanged.
- **ADR-0003** (store is the only storage module): the decision now says "reads or writes the note files" instead of naming `sqlite3`. The rule itself is unchanged.
- **ADR-0006** (new, `accepted 2026-11-21`): one JSON file per note, `<id>.json` with `id`, `text` and `created`, written under ADR-0004's temp-file, fsync and rename scheme.

**Choices I made that you did not specify. Please confirm or redirect:**
- **Location:** the default directory is `~/.notes/`, overridable with `NOTES_DIR`.
- **Ids:** integers, one more than the highest existing id.
- **Concurrent adds:** a new note is published with `os.link`, which fails rather than overwrites if the name exists, and the store then retries with the next id. Without this, two processes could overwrite each other's note, which would break R-2.
- **Search trade-off:** `search` and `all` read every file, so search slows as the number of notes grows. ADR-0006 records this.
- **Migration:** ADR-0006 does not migrate data from `~/.notes.db`. It states this as a consequence.

**Still out of step with the new decision (not touched):**
- `notes/store.py` still uses SQLite, and `tests/test_notes.py` likely depends on it.
- `README.md` still says notes are stored in `~/.notes.db` and `NOTES_DB` sets the path.
- `arc42.md` has no storage-engine text to change, so it needs no edit.

### result (success)
