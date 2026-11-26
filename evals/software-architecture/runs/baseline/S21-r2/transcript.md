### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 main HEAD && git log HEAD~1..HEAD --oneline && git diff --stat HEAD~1..HEAD && git merge-base main HEAD && ls docs/specs 2>/dev/null; find . -path ./node_modules -prune -o \\( -iname 'CODING_STANDARDS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -name '.editorconfig' -o -name 'README.md' \\) -print | grep -v node_modules",
 "description": "Resolve commits, list diff stat, find spec and standards files"
}
```

### tool_result

```
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
6a44353574d1e80d34f432e9029514cd1a12fb34
main
./README.md
```

### tool_use Bash

```json
{
 "command": "git branch -a && git log --oneline -5 && git show --stat HEAD | head -30 && ls -R docs 2>/dev/null | head -50",
 "description": "Inspect branches, recent log, and docs layout"
}
```

### tool_result

```
* master
a9a3684 feat: export notes to a file atomically
6a44353 fixture
commit a9a36841af194d7a9233115a4cef86ee8e2836cc
Author: eval <eval@example.invalid>
Date:   Sun Nov 22 18:12:05 2026 +0100

    feat: export notes to a file atomically

 docs/specs/export.md | 20 ++++++++++++++++++++
 notes/cli.py         |  6 ++++++
 notes/store.py       | 12 ++++++++++++
 3 files changed, 38 insertions(+)
docs:
adr
architecture
specs

docs/adr:
0001-use-sqlite-for-storage.md
0002-record-architecture-decisions.md
0003-cli-reaches-storage-only-through-store.md
0004-write-notes-atomically.md
0005-add-postgresql-backend.md

docs/architecture:
arc42.md

docs/specs:
export.md
```

### tool_use Bash

```json
{
 "command": "git diff HEAD~1...HEAD && echo ---SPEC--- && cat docs/specs/export.md && echo ---ADR4--- && cat docs/adr/0004-write-notes-atomically.md && echo ---ADR3--- && cat docs/adr/0003-cli-reaches-storage-only-through-store.md && echo ---ADR2--- && cat docs/adr/0002-record-architecture-decisions.md",
 "description": "Show the commit diff, spec, and relevant ADRs"
}
```

### tool_result

```
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
---SPEC---
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
---ADR4---
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
---ADR3---
# 3. CLI reaches storage only through the store module

## Status

accepted 2026-10-01

## Context

Contributors should be able to swap the storage engine by changing one module (QG-3, QS-3).

## Decision

Only `notes/store.py` imports `sqlite3` or touches the da
[... 979 chars cut]
```

### tool_use Bash

```json
{
 "command": "git ls-files && echo ---README--- && cat README.md && echo ---ARC42--- && cat docs/architecture/arc42.md | head -150",
 "description": "List tracked files and read README and architecture doc"
}
```

### tool_result

```
GLOSSARY.md
README.md
docs/adr/0001-use-sqlite-for-storage.md
docs/adr/0002-record-architecture-decisions.md
docs/adr/0003-cli-reaches-storage-only-through-store.md
docs/adr/0004-write-notes-atomically.md
docs/adr/0005-add-postgresql-backend.md
docs/architecture/arc42.md
docs/specs/export.md
notes/__init__.py
notes/__main__.py
notes/cli.py
notes/model.py
notes/store.py
tests/__init__.py
tests/test_notes.py
---README---
# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
---ARC42---
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
```

### tool_use Bash

```json
{
 "command": "for f in notes/cli.py notes/store.py notes/model.py tests/test_notes.py GLOSSARY.md docs/adr/0001-use-sqlite-for-storage.md docs/adr/0005-add-postgresql-backend.md; do echo \"=== $f\"; cat -n $f; done",
 "description": "Read full source, tests, glossary, and ADRs 0001 and 0005"
}
```

### tool_result

```
=== notes/cli.py
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
=== notes/store.py
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
=== notes/model.py
     1	from dataclasses import dataclass
     2	
     3	
     4	@dataclass(frozen=True)
     5	class Note:
     6	    id: int
     7	    text: str
     8	    created: str
=== tests/test_notes.py
     1	import io
     2	import os
     3	import tempfile
     4	import unittest
     5	from contextlib import redirect_stdou
[... 2729 chars cut]
```

### tool_use Bash

```json
{
 "command": "python3 -m unittest -q 2>&1 | tail -3; T=$(mktemp -d); export NOTES_DB=$T/n.db; python3 -m notes add \"Buy milk\" >/dev/null; python3 -m notes add 'Café \"x\"\ny' >/dev/null; python3 -m notes export $T/out.jsonl; echo \"exit=$?\"; cat $T/out.jsonl; ls -a $T; python3 -m notes export $T/nodir/out.jsonl; echo \"exit=$?\"; python3 -m notes export $T; echo \"exit=$?\"; ls -a $T; python3 -m notes export \"\" ; echo \"exit=$?\"; awk 'length > 100 {print FILENAME\": \"FNR\": \"length}' notes/*.py; rm -rf $T",
 "description": "Run tests and exercise export edge cases in a temp dir"
}
```

### tool_result

```
Ran 3 tests in 0.083s

OK
exit=0
{"id": 1, "text": "Buy milk", "created": "2026-11-22T17:12:25+00:00"}
{"id": 2, "text": "Caf\u00e9 \"x\"\ny", "created": "2026-11-22T17:12:25+00:00"}
.
..
n.db
out.jsonl
notes: [Errno 2] No such file or directory: '/tmp/tmp.PMLMJoSOCS/nodir/out.jsonl.tmp'
exit=1
notes: [Errno 21] Is a directory: '/tmp/tmp.PMLMJoSOCS.tmp' -> '/tmp/tmp.PMLMJoSOCS'
exit=1
.
..
n.db
out.jsonl
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/sa-eval-3gl_vmps/project/notes/__main__.py", line 5, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/sa-eval-3gl_vmps/project/notes/cli.py", line 25, in main
    store.export(args.path)
    ~~~~~~~~~~~~^^^^^^^^^^^
  File "/tmp/sa-eval-3gl_vmps/project/notes/store.py", line 40, in export
    tmp = path.with_name(path.name + ".tmp")
  File "/usr/lib/python3.13/pathlib/_local.py", line 361, in with_name
    raise ValueError(f"{self!r} has an empty name")
ValueError: PosixPath('.') has an empty name
exit=1
notes/store.py: 43: 103
```

### assistant

## Review: `a9a3684` (`feat: export notes to a file atomically`) against `6a44353`

No `main` branch exists locally, so I used `HEAD~1` (`6a44353`) as the base, as you specified. The spec is `docs/specs/export.md`. I ran both axes inline rather than dispatching subagents. No files were changed. `python3 -m unittest` passes (3 tests).

Standards sources: `README.md`, `docs/architecture/arc42.md`, `docs/adr/0001`–`0005`, `GLOSSARY.md`. There is no `CONTRIBUTING.md` or `CODING_STANDARDS.md`.

## Standards

1. **Important: the implementation rests on decisions whose ADRs are not accepted.** `store.py:37` cites ADR-0004 as its basis, but ADR-0004 is `proposed`. ADR-0002 lists "import and export formats" as a decision the architect must accept centrally, and no accepted ADR covers the JSON-lines export format. ADR-0002 also says work depending on such a decision waits until its ADR is accepted. This commit should wait for ADR acceptance, or the ADRs should be accepted first.
2. **Important: an invalid PATH bypasses the documented error convention.** arc42 §8 requires errors as `notes: <message>` on stderr with exit code 1. `notes export ""` and `notes export .` raise an unhandled `ValueError` from `path.with_name(...)` (`store.py:40`), producing a traceback. I reproduced this. The `except OSError` in `cli.py:30` does not catch it.
3. **Minor: `store.py:43` is 103 characters.** No line-length limit is documented in the repo, so this is style only.

Conforming: ADR-0003 (only `store.py` touches storage; `cli.py` uses `Store`), the dependency rule `cli → store → model`, and the stderr/exit-1 path for `OSError`.

## Spec

1. **Important: nothing tests export or its crash guarantee.** The spec's central requirement is that a crash leaves either the old file or the complete new one. The three existing tests cover only add, list, and search. The behaviour is unverified.
2. **Minor: a failed rename leaves `PATH.tmp` behind.** There is no cleanup on error. I reproduced this when `PATH` is a directory: `os.replace` fails with `[Errno 21]`, and the error message names the `.tmp` file, which is left in place.
3. **Minor: the temp name is fixed.** Two concurrent exports to the same PATH both write `PATH.tmp` and can interleave.

Conforming, verified by running the command: each line has the fields `id`, `text`, and `created`; the order is oldest first; the output is valid JSON Lines; a missing parent directory fails cleanly with exit 1 and leaves `PATH` untouched; and no other formats or import were added.

**Worst issue per axis:** Standards is the unaccepted ADR-0004 and the export format decision (Important, item 1). Spec is the missing tests for the atomicity guarantee (Important, item 1).

### result (success)
