### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### assistant

I'll run both axes inline as two separate passes, since the system guidance says not to spawn agents unless you ask for it. First, pin the commits and confirm the range.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 HEAD main && git log HEAD~1..HEAD --oneline && git diff --stat HEAD~1 HEAD && git diff HEAD~1 HEAD && echo \"--- main vs HEAD~1 ---\" && git diff --stat HEAD~1 main",
 "description": "Resolve SHAs, show commit and diff"
}
```

### tool_result

```
Exit code 128
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
6a44353574d1e80d34f432e9029514cd1a12fb34
a9a36841af194d7a9233115a4cef86ee8e2836cc
main
```

### tool_use Bash

```json
{
 "command": "ls -la docs/specs 2>/dev/null; cat docs/specs/export.md 2>/dev/null; echo \"--- standards ---\"; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'STYLE*.md' \\) -print",
 "description": "Read spec and locate standards files"
}
```

### tool_result

```
total 12
drwxr-xr-x 2 root root 4096 Nov 22 18:11 .
drwxr-xr-x 5 root root 4096 Nov 22 18:11 ..
-rw-r--r-- 1 root root  456 Nov 22 18:11 export.md
# Export notes to a file

## Problem

Users cannot take their notes to other tools.

## Behaviour

`notes export PATH` writes every note as one JSON line to `PATH`, oldest first:

```text
{"id": 1, "text": "Buy milk", "created": "2026-11-20T09:00:00+00:00"}
```

Each line holds the fields `id`, `text` and `created`. A crash during the export leaves either
the old file at `PATH` or the complete new one.

## Out of scope

Importing notes; other formats.
--- standards ---
```

### assistant

The `main` branch doesn't resolve locally. I'll check what branches exist and rerun the diff.

### tool_use Bash

```json
{
 "command": "git branch -a && echo \"---\" && git log --oneline --all -5 && echo \"--- diff ---\" && git diff --stat HEAD~1 HEAD && git diff HEAD~1 HEAD && echo \"--- standards ---\" && find . -path ./.git -prune -o -type f \\( -iname '*.md' -o -name '.editorconfig' -o -name '.eslintrc*' -o -name 'pyproject.toml' -o -name 'setup.cfg' -o -name 'ruff.toml' \\) -print",
 "description": "List branches, diff, and standards files"
}
```

### tool_result

```
* master
---
a9a3684 feat: export notes to a file atomically
6a44353 fixture
--- diff ---
 docs/specs/export.md | 20 ++++++++++++++++++++
 notes/cli.py         |  6 ++++++
 notes/store.py       | 12 ++++++++++++
 3 files changed, 38 insertions(+)
diff --git a/docs/specs/export.md b/docs/specs/export.md
new file mode 100644
index 0000000..d597ebf
--- /dev/null
+++ b/docs/specs/export.md
@@ -0,0 +1,20 @@
+# Export notes to a file
+
+## Problem
+
+Users cannot take their notes to other tools.
+
+## Behaviour
+
+`notes export PATH` writes every note as one JSON line to `PATH`, oldest first:
+
+```text
+{"id": 1, "text": "Buy milk", "created": "2026-11-20T09:00:00+00:00"}
+```
+
+Each line holds the fields `id`, `text` and `created`. A crash during the export leaves either
+the old file at `PATH` or the complete new one.
+
+## Out of scope
+
+Importing notes; other formats.
diff --git a/notes/cli.py b/notes/cli.py
index 96974cd..cdb7ea3 100644
--- a/notes/cli.py
+++ b/notes/cli.py
@@ -10,6 +10,7 @@ def main(argv=None):
     sub.add_parser("add", help="add a note").add_argument("text")
     sub.add_parser("list", help="list all notes")
     sub.add_parser("search", help="find notes containing a term").add_argument("term")
+    sub.add_parser("export", help="write all notes as JSON lines to a file").add_argument("path")
     args = parser.parse_args(argv)
     try:
         store = Store(default_path())
@@ -20,10 +21,15 @@ def main(argv=None):
         if args.command == "add":
             note = store.add(args.text)
             print(note.id)
+        elif args.command == "export":
+            store.export(args.path)
         else:
             found = store.all() if args.command == "list" else store.search(args.term)
             for note in found:
                 print(f"{note.id}\t{note.created}\t{note.text}")
+    except OSError as e:  # arc42 section 8
+        print(f"notes: {e}", file=sys.stderr)
+        return 1
     finally:
         store.close()
     return 0
diff --git a/notes/store.py b/notes/store.py
index eb064d3..45300c8 100644
--- a/notes/store.py
+++ b/notes/store.py
@@ -1,4 +1,5 @@
 """The only module that knows how notes are stored (ADR-0001, ADR-0003)."""
+import json
 import os
 import sqlite3
 from datetime import datetime, timezone
@@ -33,5 +34,16 @@ class Store:
                                 (f"%{term}%",))
         return [Note(*row) for row in rows]
 
+    def export(self, path):
+        """Write every note as one JSON line to path, atomically (ADR-0004)."""
+        path = Path(path)
+        tmp = path.with_name(path.name + ".tmp")
+        with open(tmp, "w", encoding="utf-8") as f:
+            for note in self.all():
+                f.write(json.dumps({"id": note.id, "text": note.text, "created": note.created}) + "\n")
+            f.flush()
+            os.fsync(f.fileno())
+        os.replace(tmp, path)
+
     def close(self):
         self._db.close()
--- standards ---
./README.md
./GLOSSARY.md
./docs/adr/0004-write-notes-atomically.md
./docs/adr/0002-record-architecture-decisions.md
./docs/adr/0005-add-postgresql-backend.md
./docs/adr/0003-cli-reaches-storage-only-through-store.md
./docs/adr/0001-use-sqlite-for-storage.md
./docs/architecture/arc42.md
./docs/specs/export.md
```

### assistant

The diff is non-empty and the range resolves; `main` doesn't exist locally, so I'm using HEAD~1 as the base. Next I'll read the standards sources (ADRs, arc42, README, glossary) and the full store and CLI modules the diff touches.

### tool_use Bash

```json
{
 "command": "for f in README.md GLOSSARY.md docs/adr/*.md docs/architecture/arc42.md; do echo \"=== $f ===\"; cat \"$f\"; echo; done",
 "description": "Read standards and ADR documents"
}
```

### tool_result

```
=== README.md ===
# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).

=== GLOSSARY.md ===
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.

=== docs/adr/0001-use-sqlite-for-storage.md ===
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

=== docs/adr/0002-record-architecture-decisions.md ===
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

=== docs/adr/0003-cli-reaches-storage-only-through-store.md ===
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

=== docs/adr/0004-write-notes-atomically.md ===
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

=== docs/adr/0005-add-postgresql-backend.md ===
# 5. Add a PostgreSQL backend

## Status

proposed

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.

=== docs/architecture/arc42.md ===
# notes: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add, list and search notes from the command line. | 1 | active | core use |
| R-2 | No note is lost when the process or machine crashes. | 2 | active | users keep notes for years |
| R-3 | Runs on Linux and macOS with only the Python standard library. | 3 | active | installed on locked-down machines |
| R-4 | Notes sync between a user's devices. | - | deferred | n
[... 2048 chars cut]
```

### tool_use Bash

```json
{
 "command": "for f in notes/store.py notes/cli.py; do echo \"=== $f ===\"; cat -n \"$f\"; done; ls notes tests 2>/dev/null",
 "description": "Read full store and CLI source"
}
```

### tool_result

```
=== notes/store.py ===
     1	"""The only module that knows how notes are stored (ADR-0001, ADR-0003)."""
     2	import json
     3	import os
     4	import sqlite3
     5	from datetime import datetime, timezone
     6	from pathlib import Path
     7	
     8	from notes.model import Note
     9	
    10	
    11	def default_path():
    12	    return Path(os.environ.get("NOTES_DB", Path.home() / ".notes.db"))
    13	
    14	
    15	class Store:
    16	    def __init__(self, path):
    17	        self._db = sqlite3.connect(path)
    18	        self._db.execute("CREATE TABLE IF NOT EXISTS notes "
    19	                         "(id INTEGER PRIMARY KEY, text TEXT NOT NULL, created TEXT NOT NULL)")
    20	
    21	    def add(self, text):
    22	        created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    23	        with self._db:
    24	            cur = self._db.execute("INSERT INTO notes (text, created) VALUES (?, ?)",
    25	                                   (text, created))
    26	        return Note(cur.lastrowid, text, created)
    27	
    28	    def all(self):
    29	        rows = self._db.execute("SELECT id, text, created FROM notes ORDER BY id")
    30	        return [Note(*row) for row in rows]
    31	
    32	    def search(self, term):
    33	        rows = self._db.execute("SELECT id, text, created FROM notes WHERE text LIKE ? ORDER BY id",
    34	                                (f"%{term}%",))
    35	        return [Note(*row) for row in rows]
    36	
    37	    def export(self, path):
    38	        """Write every note as one JSON line to path, atomically (ADR-0004)."""
    39	        path = Path(path)
    40	        tmp = path.with_name(path.name + ".tmp")
    41	        with open(tmp, "w", encoding="utf-8") as f:
    42	            for note in self.all():
    43	                f.write(json.dumps({"id": note.id, "text": note.text, "created": note.created}) + "\n")
    44	            f.flush()
    45	            os.fsync(f.fileno())
    46	        os.replace(tmp, path)
    47	
    48	    def close(self):
    49	        self._db.close()
=== notes/cli.py ===
     1	import argparse
     2	import sys
     3	
     4	from notes.store import Store, default_path
     5	
     6	
     7	def main(argv=None):
     8	    parser = argparse.ArgumentParser(prog="notes", description="Keep short notes.")
     9	    sub = parser.add_subparsers(dest="command", required=True)
    10	    sub.add_parser("add", help="add a note").add_argument("text")
    11	    sub.add_parser("list", help="list all notes")
    12	    sub.add_parser("search", help="find notes containing a term").add_argument("term")
    13	    sub.add_parser("export", help="write all notes as JSON lines to a file").add_argument("path")
    14	    args = parser.parse_args(argv)
    15	    try:
    16	        store = Store(default_path())
    17	    except Exception as e:  # arc42 section 8: errors go to stderr, exit code 1
    18	        print(f"notes: {e}", file=sys.stderr)
    19	        return 1
    20	    try:
    21	        if args.command == "add":
    22	            note = store.add(args.text)
    23	            print(note.id)
    24	        elif args.command == "export":
    25	            store.export(args.path)
    26	        else:
    27	            found = store.all() if args.command == "list" else store.search(args.term)
    28	            for note in found:
    29	                print(f"{note.id}\t{note.created}\t{note.text}")
    30	    except OSError as e:  # arc42 section 8
    31	        print(f"notes: {e}", file=sys.stderr)
    32	        return 1
    33	    finally:
    34	        store.close()
    35	    return 0
notes:
__init__.py
__main__.py
cli.py
model.py
store.py

tests:
__init__.py
test_notes.py
```

### assistant

I've read the ADRs, arc42, README, and both changed modules. Before writing findings, I'll check whether the tests cover export and whether the existing suite passes. I'm setting `PYTHONDONTWRITEBYTECODE` so the run leaves no files in the repo.

### tool_use Bash

```json
{
 "command": "grep -n -i \"export\" tests/test_notes.py; echo \"exit-grep=$?\"; PYTHONDONTWRITEBYTECODE=1 python3 -m unittest 2>&1 | tail -5; echo \"--- behaviour check in scratch dir ---\"; D=$(mktemp -d) && cd \"$D\" && export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/sa-eval-_9uka3ug/project NOTES_DB=\"$D/n.db\" && python3 -m notes add \"Buy milk\" && python3 -m notes add \"Héllo \\\"q\\\"\" && python3 -m notes export \"$D/out.jsonl\"; echo \"rc=$?\"; cat \"$D/out.jsonl\"; ls -a \"$D\"; echo \"--- missing dir ---\"; python3 -m notes export \"$D/nope/x.jsonl\"; echo \"rc=$?\"; echo \"--- dir target ---\"; mkdir \"$D/adir\"; python3 -m notes export \"$D/adir\"; echo \"rc=$?\"; ls -a \"$D\"",
 "description": "Run tests and exercise export in scratch dir"
}
```

### tool_result

```
exit-grep=1
...
----------------------------------------------------------------------
Ran 3 tests in 0.072s

OK
--- behaviour check in scratch dir ---
1
2
rc=0
{"id": 1, "text": "Buy milk", "created": "2026-11-22T17:12:25+00:00"}
{"id": 2, "text": "H\u00e9llo \"q\"", "created": "2026-11-22T17:12:25+00:00"}
.
..
n.db
out.jsonl
--- missing dir ---
notes: [Errno 2] No such file or directory: '/tmp/tmp.khnIS4u2WE/nope/x.jsonl.tmp'
rc=1
--- dir target ---
notes: [Errno 21] Is a directory: '/tmp/tmp.khnIS4u2WE/adir.tmp' -> '/tmp/tmp.khnIS4u2WE/adir'
rc=1
.
..
adir
adir.tmp
n.db
out.jsonl
Shell cwd was reset to /tmp/sa-eval-_9uka3ug/project
```

### assistant

## Standards

Base: `HEAD~1` (`6a44353`) → `HEAD` (`a9a3684`). The repo has no local `main` branch, so I used the parent commit as the base. Nothing was changed.

1. **Important: the export format and command were added without an accepted ADR.** ADR-0002 centrally decides "import and export formats" and "CLI command names," and says work depending on those "waits until its ADR is accepted." No ADR covers `notes export` or the JSON-lines format. The code also cites ADR-0004 as its basis, but ADR-0004 is still `proposed`. Relevant: `notes/cli.py:13`, `notes/store.py:37`.
2. **Minor: no tests for export.** `tests/test_notes.py` has no export case, and the commit adds none. The suite passes (3 tests, OK), but nothing exercises the new command. arc42 QS-1 defines the crash-safety measure, and nothing verifies the atomic-write path.
3. **Minor: failed exports leave a `.tmp` file behind.** I ran `notes export <existing-dir>` and got `rc=1`, but `<dir>.tmp` remained on disk. The `open`/`os.replace` path in `notes/store.py:40-46` has no cleanup on error. ADR-0004 doesn't require cleanup, so this is a hygiene issue, not a violation.

Layering (`cli` → `store` → `model`), the ADR-0003 rule (only `store.py` touches storage), stdlib-only use, and the `notes: <message>` / exit 1 error convention are all followed.

**Worst within Standards:** finding 1, the export format and command shipped without an accepted ADR.

## Spec

Checked against `docs/specs/export.md`:

- **Output format:** matches. I ran `notes export` on two notes. Each line is `{"id": …, "text": …, "created": …}` with the fields in the spec's order, and JSON escaping is valid (`"Héllo \"q\""` → `H\u00e9llo \"q\"`).
- **Ordering, oldest first:** `Store.all()` orders by `id`, which is autoincrement, so this matches.
- **Atomicity:** the write goes to `PATH.tmp`, is flushed and `fsync`ed, then moved with `os.replace`. A crash before the replace leaves the old `PATH` intact. I checked this by reading the code; I didn't kill the process mid-write.
- **Out of scope (import, other formats):** not implemented, as specified.

Finding (minor): the spec's behaviour has no test pinning it, so a regression in format, ordering, or atomicity would go unnoticed.

**Worst within Spec:** the missing test for the specified behaviour. The implementation itself matches the spec.

---

**Summary:** Standards has 3 findings (1 important, 2 minor); Spec has 1 minor finding. The worst Standards issue is the export format and command shipped without an accepted ADR; the worst Spec issue is the missing test.

### result (success)
