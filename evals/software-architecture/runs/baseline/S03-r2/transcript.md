### user

I've reviewed the open ADRs. ADR-0004 is approved. ADR-0005 is rejected: we will not run a
second storage engine, a server database contradicts R-3. One more change: we're moving off
SQLite. Notes will be stored as one JSON file per note, because SQLite files are hard to diff
and repair by hand. Update the decision records accordingly. I'm not available for questions.

### tool_use Bash

```json
{
 "command": "git status --short && find . -path ./.git -prune -o -type f -print | sort && echo --- && grep -ril \"adr\\|sqlite\" --exclude-dir=.git . | head -50",
 "description": "List project files and find ADR/SQLite references"
}
```

### tool_result

```
./GLOSSARY.md
./README.md
./docs/adr/0001-use-sqlite-for-storage.md
./docs/adr/0002-record-architecture-decisions.md
./docs/adr/0003-cli-reaches-storage-only-through-store.md
./docs/adr/0004-write-notes-atomically.md
./docs/adr/0005-add-postgresql-backend.md
./docs/architecture/arc42.md
./notes/__init__.py
./notes/__main__.py
./notes/cli.py
./notes/model.py
./notes/store.py
./tests/__init__.py
./tests/test_notes.py
---
notes/store.py
docs/adr/0003-cli-reaches-storage-only-through-store.md
docs/adr/0002-record-architecture-decisions.md
docs/adr/0001-use-sqlite-for-storage.md
docs/architecture/arc42.md
```

### tool_use Bash

```json
{
 "command": "for f in docs/adr/*.md; do echo \"=== $f\"; cat \"$f\"; done; echo \"=== arc42\"; cat docs/architecture/arc42.md; echo \"=== README\"; cat README.md; echo \"=== GLOSSARY\"; cat GLOSSARY.md",
 "description": "Read ADRs, architecture doc, README, glossary"
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
=== arc42
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
| Contributors | change
[... 1982 chars cut]
```

### tool_use Bash

```json
{
 "command": "git log --oneline -3 && head -c 0 /dev/null && grep -n \"sqlite\\|database\" notes/store.py | head",
 "description": "Check git log and store.py SQLite references"
}
```

### tool_result

```
d5f8f66 fixture
3:import sqlite3
16:        self._db = sqlite3.connect(path)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-80dvuw6l/project/docs/adr/0006-store-one-json-file-per-note.md",
 "content": "# 6. Store one JSON file per note\n\n## Status\n\naccepted 2026-11-21\n\nSupersedes [ADR-0001](0001-use-sqlite-for-storage.md).\n\n## Context\n\nNotes must survive crashes (R-2, QG-1, QS-1), the program may use only the Python standard\nlibrary (R-3, QG-2), and the store must stay a single module (QS-3). Users must be able to\ninspect, diff and repair their notes by hand. A SQLite file is binary: it is hard to diff and\ncannot be repaired with a text editor, so it no longer meets these needs.\n\n## Decision\n\nStore each note as one JSON file, named `<id>.json`, in one notes directory, by default\n`~/.notes/`. The directory is set with `NOTES_DIR`.\n\nEach file is written under the rule of [ADR-0004](0004-write-notes-atomically.md): temporary\nfile in the same directory, `os.fsync`, then `os.replace`.\n\nOnly `notes/store.py` reads or writes these files ([ADR-0003](0003-cli-reaches-storage-only-through-store.md)).\n\n## Consequences\n\n- A crash leaves each note either fully written or absent; one damaged note does not affect the others.\n- Notes are plain text and can be read, diffed and repaired with a text editor.\n- Search has no index: `search` reads every note file. Acceptable for the note volumes in scope;\n  revisit if search becomes slow (see the rejected [ADR-0005](0005-add-postgresql-backend.md)).\n- Many small files: one extra `fsync` and one directory entry per note.\n- Existing data in `~/.notes.db` is not migrated by this decision; a migration is a separate piece of work.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-80dvuw6l/project/docs/adr/0006-store-one-json-file-per-note.md (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-80dvuw6l/project/docs/adr/0001-use-sqlite-for-storage.md",
 "old_string": "accepted 2026-10-01",
 "new_string": "superseded by [ADR-0006](0006-store-one-json-file-per-note.md) 2026-11-21"
}
```

### tool_result

```
The file /tmp/sa-eval-80dvuw6l/project/docs/adr/0001-use-sqlite-for-storage.md has been updated successfully.
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-80dvuw6l/project/docs/adr/0004-write-notes-atomically.md",
 "old_string": "proposed\n\n## Context\n\nQS-1 requires that a crash during `add` leaves the store readable (R-2, QG-1). Any file the\nstore writes besides the database (for example an export) must meet the same rule.",
 "new_string": "accepted 2026-11-21\n\n## Context\n\nQS-1 requires that a crash during `add` leaves the store readable (R-2, QG-1). Every file the\nstore writes (note files, and for example an export) must meet the same rule."
}
```

### tool_result

```
The file /tmp/sa-eval-80dvuw6l/project/docs/adr/0004-write-notes-atomically.md has been updated successfully.
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-80dvuw6l/project/docs/adr/0003-cli-reaches-storage-only-through-store.md",
 "old_string": "Only `notes/store.py` imports `sqlite3` or touches the database file. `notes/cli.py` uses the\n`Store` class and the `Note` value.",
 "new_string": "Only `notes/store.py` reads or writes the storage (the note files of [ADR-0006](0006-store-one-json-file-per-note.md)).\n`notes/cli.py` uses the `Store` class and the `Note` value."
}
```

### tool_result

```
The file /tmp/sa-eval-80dvuw6l/project/docs/adr/0003-cli-reaches-storage-only-through-store.md has been updated successfully.
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-80dvuw6l/project/docs/adr/0005-add-postgresql-backend.md",
 "old_string": "proposed\n\n## Context",
 "new_string": "rejected 2026-11-21\n\n## Context"
}
```

### tool_result

```
The file /tmp/sa-eval-80dvuw6l/project/docs/adr/0005-add-postgresql-backend.md has been updated successfully.
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-80dvuw6l/project/docs/adr/0005-add-postgresql-backend.md",
 "old_string": "## Consequences\n\nNeeds the `psycopg` package and a running database server.",
 "new_string": "## Consequences\n\nNeeds the `psycopg` package and a running database server.\n\n## Outcome\n\nRejected. We will not run a second storage engine, and a server database contradicts R-3\n(installs on locked-down machines with only the standard library)."
}
```

### tool_result

```
The file /tmp/sa-eval-80dvuw6l/project/docs/adr/0005-add-postgresql-backend.md has been updated successfully.
```

### assistant

The decision records are updated. I didn't change any code, so `notes/store.py` still uses SQLite until the implementation follows.

- **ADR-0004** (atomic writes): status is now `accepted 2026-11-21`. I also changed its context to say every file the store writes, including note files, follows the rule.
- **ADR-0005** (PostgreSQL): status is now `rejected 2026-11-21`, with an Outcome section giving your reason: a second engine, and a server database contradicts R-3.
- **ADR-0006** (new, `docs/adr/0006-store-one-json-file-per-note.md`): one JSON file per note, `accepted 2026-11-21`, superseding ADR-0001. It keeps the atomic-write rule from ADR-0004 and the store-only access rule from ADR-0003.
- **ADR-0001** (SQLite): status is now `superseded by ADR-0006 2026-11-21`. The original text is kept.
- **ADR-0003** (store boundary): the wording no longer names `sqlite3` or the database file. The rule is unchanged.

Choices I made that you should check:
- **Location:** `~/.notes/`, overridable with `NOTES_DIR`. This replaces `~/.notes.db` and `NOTES_DB`.
- **File name:** `<id>.json`.
- **Migration:** existing `~/.notes.db` data is not migrated. The ADR says a migration is separate work.
- **Search:** it reads every file, with no index. The ADR notes this as a consequence to revisit if search gets slow.

Still stale, outside the decision records and not changed: `notes/store.py` (SQLite), `README.md` (points at `~/.notes.db` and `NOTES_DB`), and the arc42 document wherever it describes storage. Nothing is committed.

### result (success)
