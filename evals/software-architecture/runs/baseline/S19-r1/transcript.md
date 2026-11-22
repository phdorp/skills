### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### assistant

I'll pin the commits, confirm the range, and locate the spec before reviewing either axis.

### tool_use Bash

```json
{
 "command": "git rev-parse main HEAD~1 HEAD && git log main..HEAD~1 --oneline 2>/dev/null; echo \"---log HEAD~1..HEAD---\"; git log HEAD~1..HEAD --oneline; echo \"---stat---\"; git diff --stat HEAD~1..HEAD; echo \"---files---\"; ls docs/specs 2>/dev/null; ls",
 "description": "Pin SHAs, show commit list, diff stat, and spec location"
}
```

### tool_result

```
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
main
---log HEAD~1..HEAD---
05c07cb feat: export notes as JSON
---stat---
 docs/adr/0004-export-as-json-lines.md | 20 ++++++++++++++++++++
 docs/specs/export.md                  | 19 +++++++++++++++++++
 notes/cli.py                          | 10 ++++++++++
 3 files changed, 49 insertions(+)
---files---
export.md
GLOSSARY.md
README.md
docs
notes
tests
```

### tool_use Bash

```json
{
 "command": "git merge-base main HEAD && git diff HEAD~1..HEAD",
 "description": "Show full diff for the last commit"
}
```

### tool_result

```
Exit code 128
fatal: Not a valid object name main
```

### tool_use Bash

```json
{
 "command": "cat docs/specs/export.md; echo \"---standards search---\"; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'README.md' \\) -print",
 "description": "Read spec and search for standards documents"
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
---standards search---
./README.md
```

### assistant

`main` doesn't resolve in this repo, so I'll check the branch layout. The user's range is `HEAD~1..HEAD`, which doesn't depend on `main`. I'll read the full diff and the ADR too.

### tool_use Bash

```json
{
 "command": "git branch -a; echo \"---\"; git rev-parse HEAD~1 HEAD; echo \"---diff---\"; git diff HEAD~1 HEAD; echo \"---ls---\"; ls -R notes tests docs | head -50",
 "description": "List branches, pinned SHAs, and full diff"
}
```

### tool_result

```
* master
---
e66ec675f7c98f0794e2ef59141e4b95a6dfc36e
05c07cb79f7efd1cdcdf1a87e5b2b77dcf6938af
---diff---
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
---ls---
docs:
adr
architecture
specs

docs/adr:
0001-use-sqlite-for-storage.md
0002-record-architecture-decisions.md
0003-cli-reaches-storage-only-through-store.md
0004-export-as-json-lines.md

docs/architecture:
arc42.md

docs/specs:
export.md

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

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-_gvs5ppj/project/README.md"
}
```

### tool_result

```
1	# notes
2	
3	Keep short notes from the command line.
4	
5	```sh
6	python3 -m notes add "Buy milk"
7	python3 -m notes list
8	python3 -m notes search milk
9	```
10	
11	Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
12	`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
13	
```

### assistant

The diff bypasses `Store` in `cli.py`, which may conflict with ADR 0003. Let me read the ADRs, architecture doc, store, and CLI to check the standards axis against them.

### tool_use Bash

```json
{
 "command": "cat docs/adr/0003-cli-reaches-storage-only-through-store.md; echo \"=====ADR0001\"; cat docs/adr/0001-use-sqlite-for-storage.md; echo \"=====ADR0002\"; cat docs/adr/0002-record-architecture-decisions.md; echo \"=====ARC42\"; cat docs/architecture/arc42.md; echo \"=====STORE\"; cat notes/store.py; echo \"=====CLI (full)\"; cat notes/cli.py; echo \"=====MODEL\"; cat notes/model.py; echo \"=====GLOSSARY\"; cat GLOSSARY.md",
 "description": "Read ADRs, architecture doc, and source modules"
}
```

### tool_result

```
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
=====ADR0001
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
=====ADR0002
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
=====ARC42
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
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the note is either fully stored or absent; the store still open
[... 3435 chars cut]
```

### tool_use Bash

```json
{
 "command": "cat tests/test_notes.py; echo \"=====MAIN\"; cat notes/__main__.py; echo \"=====INIT\"; cat notes/__init__.py; echo \"=====HEAD~1 cli\"; git show HEAD~1:notes/cli.py | head -5; echo \"=====git log\"; git log --format='%h %an %s' -5",
 "description": "Read tests, entrypoint, and recent history"
}
```

### tool_result

```
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
                self.assertEqual(main(["add", "Buy milk"]), 0)
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(main(["search", "milk"]), 0)
        self.assertIn("Buy milk", out.getvalue())


if __name__ == "__main__":
    unittest.main()
=====MAIN
import sys

from notes.cli import main

sys.exit(main())
=====INIT
"""Keep short notes from the command line."""
=====HEAD~1 cli
import argparse
import sys

from notes.store import Store, default_path

=====git log
05c07cb eval feat: export notes as JSON
e66ec67 eval fixture
```

### assistant

I have the picture for both axes. Before reporting, I'll confirm the one behavioural suspicion (export against a missing database) and check that the existing tests still pass. I'm using a temp path and disabling bytecode so no repo files change.

### tool_use Bash

```json
{
 "command": "T=$(mktemp -d) && export PYTHONDONTWRITEBYTECODE=1; echo \"--- export, fresh db path ---\"; NOTES_DB=\"$T/fresh.db\" python3 -m notes export; echo \"exit=$?\"; ls -la \"$T\"; echo \"--- export after add, with newline+quote text ---\"; NOTES_DB=\"$T/ok.db\" python3 -m notes add $'line1\\nsay \"hi\"' >/dev/null; NOTES_DB=\"$T/ok.db\" python3 -m notes export; echo \"exit=$?\"; echo \"--- unittest ---\"; python3 -m unittest 2>&1 | tail -4; rm -rf \"$T\"",
 "description": "Check export on fresh DB, newline escaping, and run tests"
}
```

### tool_result

```
--- export, fresh db path ---
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/sa-eval-_gvs5ppj/project/notes/__main__.py", line 5, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/sa-eval-_gvs5ppj/project/notes/cli.py", line 19, in main
    rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")
sqlite3.OperationalError: no such table: notes
exit=1
total 472
drwx------     2 root root   4096 Nov 22 16:05 .
drwxrwxrwt 14676 root root 475136 Nov 22 16:05 ..
-rw-r--r--     1 root root      0 Nov 22 16:05 fresh.db
--- export after add, with newline+quote text ---
{"id": 1, "text": "line1\nsay \"hi\"", "created": "2026-11-22T15:05:01+00:00"}
exit=0
--- unittest ---
----------------------------------------------------------------------
Ran 3 tests in 0.066s

OK
```

### assistant

## Review: `05c07cb feat: export notes as JSON` (HEAD~1..HEAD)

**Range:** base `e66ec675f7c98f0794e2ef59141e4b95a6dfc36e` (HEAD~1), head `05c07cb79f7efd1cdcdf1a87e5b2b77dcf6938af`. The repo has no `main` ref (only `master`), so I used the commit's parent as the fixed point, as you asked. The diff is non-empty: 3 files, +49 lines (`docs/adr/0004-export-as-json-lines.md`, `docs/specs/export.md`, `notes/cli.py`). Nothing was changed.

**Spec:** `docs/specs/export.md`. **Standards:** `docs/adr/0001`–`0004`, `docs/architecture/arc42.md` (§5, §8), `GLOSSARY.md`. There is no CONTRIBUTING or CODING_STANDARDS file. I ran the two axes as separate passes.

## Standards

1. **Important: breaks ADR-0003 (the CLI must reach storage only through `Store`).** `notes/cli.py:3` now imports `sqlite3`, and the `export` branch (`cli.py:18-23`) opens the database and runs SQL directly instead of calling a `Store` method. ADR-0003 says "Only `notes/store.py` imports `sqlite3`" and "Any new command that reads or writes notes goes through `Store`." It also undercuts QS-3, the stated reason for that ADR: swapping the storage engine would now mean changing `cli.py` too. Fix: add `Store.export()` or a method that yields notes, and call it from `cli.py`.
2. **Important: breaks the error convention (arc42 §8).** Errors must go to stderr as `notes: <message>` with exit code 1. The export branch sits before the `try` block, so a failure escapes as a raw traceback (see Spec item 1).
3. **Minor: no test.** `tests/test_notes.py` covers `add`, `list`, and `search`, but nothing covers `export`. The README asks that tests be run with `python3 -m unittest`.

Compliant: ADR-0004 is accepted and matches the output format. The new command name and exit code follow ADR-0002. `json.dumps` keeps a newline inside a note on one line, which ADR-0004 requires.

## Spec

1. **Important: crashes on a fresh install.** I ran `NOTES_DB=<new path> python3 -m notes export`. It exited 1 with `sqlite3.OperationalError: no such table: notes`, and it left an empty `fresh.db` file behind. `sqlite3.connect` creates the file, but the table is only created by `Store.__init__`, and the export branch never calls `Store`. The spec says `notes export` prints every note, so with zero notes it should print nothing and exit 0. This is the same root cause as Standards item 1.
2. **Minor: spec gaps.** The spec does not say what happens with zero notes or with a missing database, so item 1 relies on my reading of "prints every note." Once item 1 is fixed, the spec should state the empty-store behaviour.

Met: output is one JSON object per line with `id`, `text`, `created`, in `ORDER BY id` (oldest first). Newlines and quotes are escaped (checked: `"line1\nsay \"hi\""` stays on one line). The command takes no arguments. Import and other formats are not implemented.

Existing tests: `python3 -m unittest` passes, 3 tests OK.

**Standards:** worst issue is Important: the `cli.py` direct-SQLite access breaks ADR-0003.
**Spec:** worst issue is Important: `notes export` crashes with a traceback when the store has no table yet.

### result (success)
