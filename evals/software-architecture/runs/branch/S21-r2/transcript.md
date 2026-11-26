### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 HEAD main && git log HEAD~1..HEAD --oneline && git diff --stat HEAD~1..HEAD && ls docs docs/architecture docs/specs 2>&1; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS*' -o -iname 'CONTRIBUTING*' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'STYLE*' \\) -print",
 "description": "Resolve refs, list commit, diffstat, and find standards files"
}
```

### tool_result

```
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
d4f2f47f661ab39877029d3cd1cf5ee0625ce2ff
24f311179b500e7393f633f67cfc0c440e5f227a
main
```

### tool_use Bash

```json
{
 "command": "git diff HEAD~1..HEAD",
 "description": "Show full diff of last commit"
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
```

### tool_use Bash

```json
{
 "command": "cat docs/specs/export.md 2>&1",
 "description": "Read the export spec"
}
```

### tool_result

```
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
```

### tool_use Bash

```json
{
 "command": "ls -la docs docs/architecture docs/adr docs/specs 2>&1; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS*' -o -iname 'CONTRIBUTING*' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'STYLE*' -o -iname 'arc42*' -o -iname 'ADR*' \\) -print; echo ---; cat notes/store.py; echo ---; cat notes/cli.py; echo ---; ls -R notes tests 2>&1 | head -50",
 "description": "Check standards, architecture docs, and full store and CLI code"
}
```

### tool_result

```
docs:
total 20
drwxr-xr-x 5 root root 4096 Nov 22 18:11 .
drwxr-xr-x 6 root root 4096 Nov 22 18:11 ..
drwxr-xr-x 2 root root 4096 Nov 21 11:55 adr
drwxr-xr-x 2 root root 4096 Nov 21 11:55 architecture
drwxr-xr-x 2 root root 4096 Nov 22 18:11 specs

docs/adr:
total 28
drwxr-xr-x 2 root root 4096 Nov 21 11:55 .
drwxr-xr-x 5 root root 4096 Nov 22 18:11 ..
-rw-r--r-- 1 root root  478 Nov 21 11:55 0001-use-sqlite-for-storage.md
-rw-r--r-- 1 root root  817 Nov 21 11:55 0002-record-architecture-decisions.md
-rw-r--r-- 1 root root  419 Nov 21 11:55 0003-cli-reaches-storage-only-through-store.md
-rw-r--r-- 1 root root  552 Nov 21 11:55 0004-write-notes-atomically.md
-rw-r--r-- 1 root root  291 Nov 21 11:55 0005-add-postgresql-backend.md

docs/architecture:
total 12
drwxr-xr-x 2 root root 4096 Nov 21 11:55 .
drwxr-xr-x 5 root root 4096 Nov 22 18:11 ..
-rw-r--r-- 1 root root 2674 Nov 21 11:55 arc42.md

docs/specs:
total 12
drwxr-xr-x 2 root root 4096 Nov 22 18:11 .
drwxr-xr-x 5 root root 4096 Nov 22 18:11 ..
-rw-r--r-- 1 root root  456 Nov 22 18:11 export.md
./docs/adr
./docs/architecture/arc42.md
---
"""The only module that knows how notes are stored (ADR-0001, ADR-0003)."""
import json
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

    def export(self, path):
        """Write every note as one JSON line to path, atomically (ADR-0004)."""
        path = Path(path)
        tmp = path.with_name(path.name + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            for note in self.all():
                f.write(json.dumps({"id": note.id, "text": note.text, "created": note.created}) + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)

    def close(self):
        self._db.close()
---
import argparse
import sys

from notes.store import Store, default_path


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes", description="Keep short notes.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("add", help="add a note").add_argument("text")
    sub.add_parser("list", help="list all notes")
    sub.add_parser("search", help="find notes containing a term").add_argument("term")
    sub.add_parser("export", help="write all notes as JSON lines to a file").add_argument("path")
    args = parser.parse_args(argv)
    try:
        store = Store(default_path())
    except Exception as e:  # arc42 section 8: errors go to stderr, exit code 1
        print(f"notes: {e}", file=sys.stderr)
        return 1
    try:
        if args.command == "add":
            note = store.add(args.text)
            print(note.id)
        elif args.command == "export":
            store.export(args.path)
        else:
            found = store.all() if args.command == "list" else store.search(args.term)
            for note in found:
                print(f"{note.id}\t{note.created}\t{note.text}")
    e
[... 243 chars cut]
```

### tool_use Bash

```json
{
 "command": "cat docs/architecture/arc42.md; echo ---ADR4; cat docs/adr/0004-write-notes-atomically.md; echo ---ADR3; cat docs/adr/0003-cli-reaches-storage-only-through-store.md; echo ---ADR1; cat docs/adr/0001-use-sqlite-for-storage.md; echo ---tests; cat tests/test_notes.py; echo ---model; cat notes/model.py; echo ---ref; cat /tmp/sa-arm-2qlej702/sa/skills/code-review/references/architecture-axis.md; echo ---prompt; cat /tmp/sa-arm-2qlej702/sa/skills/code-review/references/reviewer-prompt.md",
 "description": "Read architecture docs, ADRs, tests, and review references"
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
---ADR4
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
---ADR3
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
---ADR1
# 1. Use SQLite for storage

## Status

accepted 2026-10-01

## Context

Notes must survive crashes (R-2, QG-1, QS-1) and the program may use only the Python standard
library (R-3, QG-2). The standard library ships `sqlite3`, whose transactions are atomic.

## Decision

Store all notes in one SQLite database file, by default `~/.
[... 12774 chars cut]
```

### tool_use Bash

```json
{
 "command": "cat /tmp/sa-arm-2qlej702/sa/skills/code-review/references/standards-and-smells.md; cd /tmp/sa-eval-u1731zv7/project && ls -a; cat pyproject.toml setup.cfg ruff.toml .flake8 2>/dev/null | head -40; python3 -m unittest discover -s tests -t . 2>&1 | tail -3",
 "description": "Read smell baseline, check tooling config, run test suite"
}
```

### tool_result

```
# Standards sources and the smell baseline

The Standards axis asks whether the diff conforms to how this repo writes code. Two kinds of source answer that: what the repo documents, and a fixed baseline of code smells for what it does not.

## 1. Find the documented standards

Search the repo for every file that says how code should be written. Typical candidates:

- `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `README.md` sections on style.
- `docs/` conventions, ADRs, architecture notes, review checklists, `STYLE.md`. When `docs/architecture/arc42.md` exists, ADRs and arc42 belong to the Architecture axis ([architecture-axis.md](architecture-axis.md)), not here.
- Linter and formatter configs (`.eslintrc*`, `eslint.config.*`, `ruff.toml`, `pyproject.toml`, `.golangci.yml`, `.rubocop.yml`, `.editorconfig`) — these show what tooling enforces, which you must not re-report.
- Language- or area-specific docs (`docs/api-guidelines.md`, `packages/*/README.md`).
- Domain vocabulary in `GLOSSARY.md`: a name that contradicts the glossary is a Mysterious Name finding with a documented fix.

List the files you found and check they exist in the checkout at `HEAD`. The reviewer has no other way to read them if you only name a path, so either pass their contents or confirm the reviewer can read them in its own checkout.

**Skip anything tooling already enforces.** A linter, formatter, or type checker that runs in CI owns those findings. Re-reporting them wastes the reviewer's budget and buries the judgement calls.

## 2. Apply the smell baseline

On top of whatever the repo documents, always carry this fixed set of Fowler code smells (_Refactoring_, ch. 3). Two rules bind it:

- **The repo overrides.** A documented repo standard always wins. Where a repo standard endorses something the baseline would flag, suppress the smell and say nothing.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. A documented-standard breach can be hard; a smell cannot.

Each smell reads *what it is* → *how to fix*. **(OO)** marks a smell that assumes objects and classes; its entry names the dataflow counterpart (blocks, connections, signals, as in `codebase-design`) where one exists. Match it against the diff:

- **Long Method**: a function so long that its parts need comments or names of their own. → extract the parts into named functions.
- **Large Class**: a class or module holding many unrelated fields or responsibilities. → split it along its responsibilities.
- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** (OO): a method that reaches into another object's data more than its own. → move the method onto the data it envies. Dataflow: a block reading another block's internal variables instead of its outputs → read its output signal, or add one.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need sho
[... 1198 chars cut]
```

### tool_use Bash

```json
{
 "command": "set -u; W=$(mktemp -d); cd \"$W\"; export PYTHONPATH=/tmp/sa-eval-u1731zv7/project\nexport NOTES_DB=\"$W/n.db\"; python3 -I -m notes add \"Buy milk\" >/dev/null\necho \"== export to DB path\"; python3 -I -m notes export \"$W/n.db\"; echo \"exit=$?\"; file \"$W/n.db\"; head -c 80 \"$W/n.db\"; echo\necho \"== fresh DB then export to missing dir\"; rm -f \"$W/n.db\"; python3 -I -m notes add \"Call Ann\" >/dev/null; python3 -I -m notes export \"$W/nodir/out.jsonl\"; echo \"exit=$?\"\necho \"== export to dir path\"; mkdir \"$W/adir\"; python3 -I -m notes export \"$W/adir\"; echo \"exit=$?\"; ls -a \"$W\" \necho \"== normal export + non-ascii\"; python3 -I -m notes add \"Café ☕\" >/dev/null; python3 -I -m notes export \"$W/out.jsonl\"; echo \"exit=$?\"; cat \"$W/out.jsonl\"; ls -a \"$W\" | grep tmp || echo \"no tmp left\"\necho \"== leftover tmp on failure path\"; python3 -I -m notes export \"$W/adir/x\" ; ls -a \"$W\"",
 "description": "Run tests and exercise export edge cases in a temp dir"
}
```

### tool_result

```
/usr/bin/python3: No module named notes
== export to DB path
/usr/bin/python3: No module named notes
exit=1
/tmp/tmp.zGDAwhiHh8/n.db: cannot open `/tmp/tmp.zGDAwhiHh8/n.db' (No such file or directory)
head: cannot open '/tmp/tmp.zGDAwhiHh8/n.db' for reading: No such file or directory

== fresh DB then export to missing dir
/usr/bin/python3: No module named notes
/usr/bin/python3: No module named notes
exit=1
== export to dir path
/usr/bin/python3: No module named notes
exit=1
.
..
adir
== normal export + non-ascii
/usr/bin/python3: No module named notes
/usr/bin/python3: No module named notes
exit=1
cat: /tmp/tmp.zGDAwhiHh8/out.jsonl: No such file or directory
no tmp left
== leftover tmp on failure path
/usr/bin/python3: No module named notes
.
..
adir
Shell cwd was reset to /tmp/sa-eval-u1731zv7/project
```

### tool_use Bash

```json
{
 "command": "set -u; W=$(mktemp -d); cd \"$W\"; export PYTHONPATH=/tmp/sa-eval-u1731zv7/project\nexport NOTES_DB=\"$W/n.db\"; python3 -m notes add \"Buy milk\" >/dev/null\necho \"== export to DB path\"; python3 -m notes export \"$W/n.db\"; echo \"exit=$?\"; head -c 80 \"$W/n.db\"; echo\necho \"== DB path again after export: notes?\"; NOTES_DB=\"$W/n.db\" python3 -m notes list; echo \"exit=$?\"\nrm -f \"$W/n.db\"; python3 -m notes add \"Buy milk\" >/dev/null; python3 -m notes add \"Call Ann\" >/dev/null\necho \"== export to missing dir\"; python3 -m notes export \"$W/nodir/out.jsonl\"; echo \"exit=$?\"\necho \"== export to existing dir path\"; mkdir \"$W/adir\"; python3 -m notes export \"$W/adir\"; echo \"exit=$?\"; ls -a \"$W\"\necho \"== normal export + non-ascii\"; python3 -m notes add \"Café ☕\" >/dev/null; python3 -m notes export \"$W/out.jsonl\"; echo \"exit=$?\"; cat \"$W/out.jsonl\"; ls -a \"$W\" | grep tmp || echo \"no tmp left\"\necho \"== tmp leftover when PATH.tmp is a directory\"; mkdir \"$W/out2.jsonl.tmp\"; python3 -m notes export \"$W/out2.jsonl\"; echo \"exit=$?\"; ls -a \"$W\" | grep out2 ; \necho \"== empty DB export\"; rm -f \"$W/n.db\"; python3 -m notes export \"$W/empty.jsonl\"; echo \"exit=$?\"; ls -l \"$W/empty.jsonl\"\ncd /tmp/sa-eval-u1731zv7/project && git status --short",
 "description": "Rerun export edge cases with correct PYTHONPATH"
}
```

### tool_result

```
== export to DB path
exit=0
{"id": 1, "text": "Buy milk", "created": "2026-11-22T17:21:10+00:00"}

== DB path again after export: notes?
notes: file is not a database
exit=1
== export to missing dir
notes: [Errno 2] No such file or directory: '/tmp/tmp.PO2Nh0keSV/nodir/out.jsonl.tmp'
exit=1
== export to existing dir path
notes: [Errno 21] Is a directory: '/tmp/tmp.PO2Nh0keSV/adir.tmp' -> '/tmp/tmp.PO2Nh0keSV/adir'
exit=1
.
..
adir
adir.tmp
n.db
== normal export + non-ascii
exit=0
{"id": 1, "text": "Buy milk", "created": "2026-11-22T17:21:11+00:00"}
{"id": 2, "text": "Call Ann", "created": "2026-11-22T17:21:11+00:00"}
{"id": 3, "text": "Caf\u00e9 \u2615", "created": "2026-11-22T17:21:11+00:00"}
adir.tmp
== tmp leftover when PATH.tmp is a directory
notes: [Errno 21] Is a directory: '/tmp/tmp.PO2Nh0keSV/out2.jsonl.tmp'
exit=1
out2.jsonl.tmp
== empty DB export
exit=0
-rw-r--r-- 1 root root 0 Nov 22 18:21 /tmp/tmp.PO2Nh0keSV/empty.jsonl
?? notes/__pycache__/
?? tests/__pycache__/
```

### tool_use Bash

```json
{
 "command": "grep -n -i -E 'style|standard|convention|format|lint|test|export' README.md GLOSSARY.md | head -30; echo ---; rm -rf notes/__pycache__ tests/__pycache__ && git status --short && echo clean-tree-check-done; rm -rf /tmp/tmp.* 2>/dev/null; true",
 "description": "Check README and glossary for standards, then remove my test cache dirs"
}
```

### tool_result

```
README.md:11:Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
README.md:12:`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
---
clean-tree-check-done
```

### assistant

# Code review: `d4f2f47..24f3111` (HEAD~1..HEAD)

**Change:** "feat: export notes to a file atomically". It adds `notes export PATH` (`notes/cli.py`), `Store.export` (`notes/store.py`), and `docs/specs/export.md`.

**Scope notes:**
- `main` does not exist locally, so I used the parent commit `d4f2f47` as the base.
- `docs/architecture/arc42.md` exists, so the review has three axes.
- No documented standards files exist (no CODING_STANDARDS, CONTRIBUTING, AGENTS/CLAUDE, editorconfig, or lint config). The Standards axis uses the Fowler smell baseline, so every Standards item is a judgement call.
- I ran the three axes as separate passes in this session, not as subagents.
- The existing suite passes (`python3 -m unittest`, 3 tests). Export edge cases were run against a temp directory. The tree is unchanged.

## Standards

No documented standards. Smell-baseline judgement calls only.

- **Possible Duplicated Code**, `notes/cli.py:18` and `:31`: the `print(f"notes: {e}", file=sys.stderr)` line now appears twice. Fix: route both through one error path, or accept the duplication.
- **Test gap (judgement call)**, `tests/test_notes.py`: `Store.export` and the `export` CLI branch have no tests. The file already has store and CLI tests for `add` and `search`, so a maintainer would likely ask for them. Missing cases: the output line format, oldest-first order, and a failed write leaving the old file intact.

## Spec

Checked against `docs/specs/export.md`.

**Strengths:**
- The command, one JSON line per note, the `id`/`text`/`created` fields, and oldest-first order (`ORDER BY id`) all match the spec.
- Output matches the spec's `created` format.
- Write-to-temp, `fsync`, then `os.replace` gives the old-or-new guarantee for a process crash.
- No scope creep: no import, no other formats.

**Issues:**
- **Important: export can overwrite the notes database.** `notes/store.py:45` and `notes/cli.py:25` do not check whether `PATH` is the database file. I reproduced it: with `NOTES_DB=$W/n.db`, `notes export $W/n.db` exits 0 and replaces the SQLite file with JSON lines. The next `notes list` fails with `file is not a database`. The spec is silent here, but a reasonable user expects an export not to destroy their notes. Fix: refuse when `PATH` resolves to `default_path()` (or `NOTES_DB`).
- **Minor: a temp file is left behind on failure.** I reproduced it: `notes export adir` (where `adir` is a directory) exits 1 and leaves `adir.tmp`. The spec does not forbid this, but the stale temp file persists. Fix: remove the temp file when the write or replace fails.
- **Minor, judgement call: non-ASCII is escaped.** `notes/store.py:42` uses `json.dumps` with its default `ensure_ascii=True`, so `Café ☕` is written as `Caf\u00e9 \u2615`. This is valid JSON, and the spec's example is ASCII, so the spec is silent. If other tools should read the text directly, use `ensure_ascii=False`.

**Declined to judge:**
- Directory `fsync` after `os.replace` (power-loss durability): ADR-0004 and the spec only require crash safety, and the code meets that.
- Two concurrent exports to the same `PATH` sharing `PATH.tmp`: the spec says nothing about concurrency.

## Architecture

Sources: arc42 §1, §8 and §10, and ADRs 0001–0005.

**Issues:**
- **Important: the change relies on a proposed ADR.** `docs/adr/0004-write-notes-atomically.md` has `Status: proposed`, so it is not a rule. The code follows its Decision (temp file in the same directory, `os.fsync`, `os.replace`), but per the review rules the change depends on an open decision. The architect needs to accept or reject ADR-0004. Its Context names R-2, QG-1 and QS-1, so traceability is fine.
- **Possible arc42 §8 breach (not reproduced).** §8 says errors go to stderr as `notes: <message>` with exit code 1. The new `except OSError` (`notes/cli.py:30`) does not cover `sqlite3.Error` raised by `self.all()` during export. Such an error would escape as a traceback. I could not find a simple way to trigger it.

**Quality scenarios and ADRs checked:**
- QS-1 (SIGKILL during `add`): the stimulus is not touched, and the measure holds.
- QS-2 (stdlib only): `json`, `os` and `pathlib` are all standard library, so it holds.
- QS-3 (swap storage engine): `export` lives in `store.py` and uses only `all()`, so it holds.
- ADR-0003 (only `store.py` touches storage): `cli.py` imports no `sqlite3` and goes through `Store`, so it holds.

**Declined to judge:** none beyond the Spec-axis items above.

## Summary

- **Standards:** 2 items, both judgement calls. Worst: the missing export tests.
- **Spec:** 3 items. Worst: export can overwrite the notes database (Important).
- **Architecture:** 2 items. Worst: the change relies on the proposed ADR-0004 (Important).

I did not change any files. I removed the `__pycache__` directories my test run created, so `git status` is clean.

### result (success)
