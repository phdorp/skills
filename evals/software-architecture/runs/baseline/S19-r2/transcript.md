### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 HEAD && git log HEAD~1..HEAD --oneline && git diff --stat HEAD~1...HEAD && ls docs/specs 2>/dev/null; git branch --list main; git status --short",
 "description": "Verify commit range, diff stat, and spec presence"
}
```

### tool_result

```
e66ec675f7c98f0794e2ef59141e4b95a6dfc36e
05c07cb79f7efd1cdcdf1a87e5b2b77dcf6938af
05c07cb feat: export notes as JSON
 docs/adr/0004-export-as-json-lines.md | 20 ++++++++++++++++++++
 docs/specs/export.md                  | 19 +++++++++++++++++++
 notes/cli.py                          | 10 ++++++++++
 3 files changed, 49 insertions(+)
export.md
```

### tool_use Bash

```json
{
 "command": "git diff HEAD~1 HEAD",
 "description": "Show full diff of the last commit"
}
```

### tool_result

```
diff --git a/docs/adr/0004-export-as-json-lines.md b/docs/adr/0004-export-as-json-lines.md
new file mode 100644
index 0000000..f56346c
--- /dev/null
+++ b/docs/adr/0004-export-as-json-lines.md
@@ -0,0 +1,20 @@
+# 4. Export notes as JSON lines
+
+## Status
+
+accepted 2026-11-20
+
+## Context
+
+People want to take their notes to other tools. Several export formats were possible: CSV,
+one JSON document, or one JSON object per line.
+
+## Decision
+
+`notes export` prints every note as one JSON object per line, with the fields `id`, `text`
+and `created`, oldest first.
+
+## Consequences
+
+Other tools can read the export line by line. A note containing a newline stays on one line,
+because JSON escapes it.
diff --git a/docs/specs/export.md b/docs/specs/export.md
new file mode 100644
index 0000000..8d9ddc3
--- /dev/null
+++ b/docs/specs/export.md
@@ -0,0 +1,19 @@
+# Export notes as JSON
+
+## Problem
+
+Users cannot take their notes to other tools.
+
+## Behaviour
+
+`notes export` prints every note as one JSON line, oldest first:
+
+```text
+{"id": 1, "text": "Buy milk", "created": "2026-11-20T09:00:00+00:00"}
+```
+
+Each line holds the fields `id`, `text` and `created`. The command takes no arguments.
+
+## Out of scope
+
+Importing notes; other formats.
diff --git a/notes/cli.py b/notes/cli.py
index 96974cd..58fb479 100644
--- a/notes/cli.py
+++ b/notes/cli.py
@@ -1,4 +1,6 @@
 import argparse
+import json
+import sqlite3
 import sys
 
 from notes.store import Store, default_path
@@ -10,7 +12,15 @@ def main(argv=None):
     sub.add_parser("add", help="add a note").add_argument("text")
     sub.add_parser("list", help="list all notes")
     sub.add_parser("search", help="find notes containing a term").add_argument("term")
+    sub.add_parser("export", help="print every note as one JSON line")
     args = parser.parse_args(argv)
+    if args.command == "export":
+        db = sqlite3.connect(default_path())
+        rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")
+        for note_id, text, created in rows:
+            print(json.dumps({"id": note_id, "text": text, "created": created}))
+        db.close()
+        return 0
     try:
         store = Store(default_path())
     except Exception as e:  # arc42 section 8: errors go to stderr, exit code 1
```

### tool_use Bash

```json
{
 "command": "cat docs/specs/export.md; echo ---; find . -path ./node_modules -prune -o \\( -iname 'CODING_STANDARDS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'STYLE*' \\) -print",
 "description": "Read the export spec and find standards docs"
}
```

### tool_result

```
# Export notes as JSON

## Problem

Users cannot take their notes to other tools.

## Behaviour

`notes export` prints every note as one JSON line, oldest first:

```text
{"id": 1, "text": "Buy milk", "created": "2026-11-20T09:00:00+00:00"}
```

Each line holds the fields `id`, `text` and `created`. The command takes no arguments.

## Out of scope

Importing notes; other formats.
---
```

### tool_use Bash

```json
{
 "command": "git ls-files && echo --- && cat notes/cli.py && echo --- && cat notes/store.py && echo --- && grep -ril \"arc42\\|standard\\|convention\" --exclude-dir=.git . ; echo ---; ls docs docs/adr; cat docs/adr/000*.md 2>/dev/null | head -80",
 "description": "Read CLI, store, docs, and any standards mentions"
}
```

### tool_result

```
GLOSSARY.md
README.md
docs/adr/0001-use-sqlite-for-storage.md
docs/adr/0002-record-architecture-decisions.md
docs/adr/0003-cli-reaches-storage-only-through-store.md
docs/adr/0004-export-as-json-lines.md
docs/architecture/arc42.md
docs/specs/export.md
notes/__init__.py
notes/__main__.py
notes/cli.py
notes/model.py
notes/store.py
tests/__init__.py
tests/test_notes.py
---
import argparse
import json
import sqlite3
import sys

from notes.store import Store, default_path


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes", description="Keep short notes.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("add", help="add a note").add_argument("text")
    sub.add_parser("list", help="list all notes")
    sub.add_parser("search", help="find notes containing a term").add_argument("term")
    sub.add_parser("export", help="print every note as one JSON line")
    args = parser.parse_args(argv)
    if args.command == "export":
        db = sqlite3.connect(default_path())
        rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")
        for note_id, text, created in rows:
            print(json.dumps({"id": note_id, "text": text, "created": created}))
        db.close()
        return 0
    try:
        store = Store(default_path())
    except Exception as e:  # arc42 section 8: errors go to stderr, exit code 1
        print(f"notes: {e}", file=sys.stderr)
        return 1
    try:
        if args.command == "add":
            note = store.add(args.text)
            print(note.id)
        else:
            found = store.all() if args.command == "list" else store.search(args.term)
            for note in found:
                print(f"{note.id}\t{note.created}\t{note.text}")
    finally:
        store.close()
    return 0
---
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
---
notes/cli.py
docs/adr/0001-use-sqlite-for-storage.md
README.md
docs/architecture/arc42.md
---
docs:
adr
architecture
specs

docs/adr:
0001-use-sqlite-for-storage.md
0002-record-architecture-decisions.md
0003-cli-reaches-storage-only-through-store.md
0004-export-as-json-lines.md
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
# 2. Record architecture decisions

## Status

accepted 2026-10-01

## Context

The architect decides the architecture; contributors and agents implement it. We nee
[... 1388 chars cut]
```

### tool_use Bash

```json
{
 "command": "cat docs/architecture/arc42.md && echo --- && cat README.md && echo --- && cat tests/test_notes.py && echo --- && cat GLOSSARY.md",
 "description": "Read architecture doc, README, tests, glossary"
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
---
# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
---
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from notes.cli import main
from notes.store import Store


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.store = Store(Path(tempfile.mkdtemp()) / "n.db")

    def tearDown(self):
        self.store.close()

    def test_add_then_list(self):
        self.store.add("Buy milk")
        self.assertEqual([n.text for n in self.store.all()], ["Buy milk"])

    def test_search_matches_substring(self):
        self.store.add("Buy milk")
        self.store.add("Call Ann")
        self.assertEqual([n.text for n in self.store.search("mil")], ["Buy milk"])


class CliTest(unittest.TestCase):
    def test_add_and_search(self):
        db = Path(tempfile.mkdtemp()) / "n.db"
        with mock.patch.dict(os.environ, {"NOTES_DB": str(db)}):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main([
[... 408 chars cut]
```

### tool_use Bash

```json
{
 "command": "export PYTHONDONTWRITEBYTECODE=1; T=$(mktemp -d); echo \"== fresh db, export\"; NOTES_DB=$T/fresh.db python3 -m notes export; echo \"exit=$?\"; ls -la $T; echo \"== populated db\"; NOTES_DB=$T/p.db python3 -m notes add $'Line one\\nLine two' >/dev/null; NOTES_DB=$T/p.db python3 -m notes add 'Buy milk' >/dev/null; NOTES_DB=$T/p.db python3 -m notes export; echo \"exit=$?\"; echo \"== bad path\"; NOTES_DB=/nonexistent/x.db python3 -m notes export; echo \"exit=$?\"; echo \"== tests\"; python3 -m unittest 2>&1 | tail -3; echo \"== list on bad path (reference)\"; NOTES_DB=/nonexistent/x.db python3 -m notes list; echo \"exit=$?\"",
 "description": "Exercise export on fresh, populated, and bad-path DBs; run tests"
}
```

### tool_result

```
== fresh db, export
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/sa-eval-5ppn2_dh/project/notes/__main__.py", line 5, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/sa-eval-5ppn2_dh/project/notes/cli.py", line 19, in main
    rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")
sqlite3.OperationalError: no such table: notes
exit=1
total 472
drwx------     2 root root   4096 Nov 22 16:04 .
drwxrwxrwt 14668 root root 475136 Nov 22 16:04 ..
-rw-r--r--     1 root root      0 Nov 22 16:04 fresh.db
== populated db
{"id": 1, "text": "Line one\nLine two", "created": "2026-11-22T15:04:59+00:00"}
{"id": 2, "text": "Buy milk", "created": "2026-11-22T15:04:59+00:00"}
exit=0
== bad path
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/sa-eval-5ppn2_dh/project/notes/__main__.py", line 5, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/sa-eval-5ppn2_dh/project/notes/cli.py", line 18, in main
    db = sqlite3.connect(default_path())
sqlite3.OperationalError: unable to open database file
exit=1
== tests
Ran 3 tests in 0.051s

OK
== list on bad path (reference)
notes: unable to open database file
exit=1
```

### assistant

## Standards

**Scope:** `HEAD~1` (`e66ec67`) to `HEAD` (`05c07cb`), one commit touching `notes/cli.py`, `docs/specs/export.md` and `docs/adr/0004-export-as-json-lines.md`. No `CODING_STANDARDS.md`, `CONTRIBUTING.md` or `AGENTS.md` exists. The documented rules are in `docs/architecture/arc42.md`, `docs/adr/` (0001–0004) and `README.md`.

**Important: `notes/cli.py:3, 17–23`. The export branch breaks ADR-0003 and the arc42 building-block rule.**
ADR-0003 says "Only `notes/store.py` imports `sqlite3` or touches the database file", and "any new command that reads or writes notes goes through `Store`". The commit adds `import sqlite3` to `cli.py` and opens the database directly with `sqlite3.connect(default_path())` and a raw SQL query. arc42 §5 lists `cli` as allowed to use only `store` and `model`. `Store.all()` already returns the rows the export needs.
*Failure scenario:* a contributor who swaps the storage engine (QS-3) must now also change `cli.py`, which violates the stated measure of "0 other files changed".

**Important: `notes/cli.py:17–23`. The export path skips the error convention.**
arc42 §8 says errors go to stderr as `notes: <message>` with exit code 1. The export branch returns before the `try:` block, so it has no handler. I ran it:
- Fresh database (no `notes` table yet): traceback ending in `sqlite3.OperationalError: no such table: notes`, exit 1. `notes list` on the same database creates the table and succeeds.
- Unopenable path (`NOTES_DB=/nonexistent/x.db`): traceback, exit 1. `notes list` on the same path prints `notes: unable to open database file`.

*Failure scenario:* a user who runs `notes export` right after installing gets a Python traceback instead of the documented error line. Routing export through `Store` (for example, `store.all()`, which is the same query) fixes both this and the finding above.

**Minor: `tests/test_notes.py`. No test covers `export`.**
`CliTest` covers only `add` and `search`. The existing suite passes (`python3 -m unittest`: 3 tests, OK), but the ADR's guarantees (one line per note, newline escaped, oldest first) are not checked by any test. I checked them by hand: a note with an embedded newline is emitted on one line, and rows come out in id order.

## Spec

Checked against `docs/specs/export.md`:
- `notes export` prints one JSON object per note, oldest first. Output matches the spec's example shape and key order (`id`, `text`, `created`). Verified on a two-note database.
- The command takes no arguments. The subparser declares none.
- Out-of-scope items (import, other formats) are not implemented.

**No findings.** The spec does not say what happens on a missing table or an unopenable database, so the crash behaviour above is a gap in the error convention (Standards axis), not a spec violation.

---

**Summary:** Standards: 2 Important, 1 Minor (worst: the ADR-0003 violation, `notes/cli.py:3, 17–23`). Spec: 0 findings. Both axes were checked as separate passes in this session, not by subagents, because subagents were not requested. No files were changed.

### result (success)
