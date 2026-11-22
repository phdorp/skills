### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 HEAD main && git log HEAD~1..HEAD --oneline && git diff --stat HEAD~1..HEAD && ls docs docs/specs docs/architecture 2>&1; git merge-base main HEAD",
 "description": "Resolve SHAs, commit list, and diff stats"
}
```

### tool_result

```
Exit code 128
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
86784f6c5d2a529595b63e1975ee969fe2439d00
b2e768114ef39f0973455cfd5c9a0d12ba68dabd
main
fatal: Not a valid object name main
```

### tool_use Bash

```json
{
 "command": "cat docs/specs/export.md; echo ----; git diff main...HEAD 2>/dev/null | head -0; git diff HEAD~1..HEAD",
 "description": "Read spec and show the last commit diff"
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
----
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
 "command": "git status --short; git branch -a; ls -la; ls docs docs/* 2>&1; find . -path ./.git -prune -o -type f -print | sort | head -100; echo ----; cat notes/store.py 2>/dev/null; echo ----; cat notes/cli.py; echo ----; git show HEAD~1:notes/cli.py | head -5 >/dev/null; for f in CODING_STANDARDS.md CONTRIBUTING.md AGENTS.md CLAUDE.md; do test -f $f && { echo \"== $f\"; cat $f; }; done",
 "description": "Inspect repo layout, store module, and standards files"
}
```

### tool_result

```
Exit code 1
* master
total 32
drwxr-xr-x 6 root root 4096 Nov 22 16:02 .
drwx------ 3 root root 4096 Nov 22 16:08 ..
drwxr-xr-x 8 root root 4096 Nov 22 16:08 .git
-rw-r--r-- 1 root root  149 Nov 21 11:54 GLOSSARY.md
-rw-r--r-- 1 root root  330 Nov 21 11:54 README.md
drwxr-xr-x 5 root root 4096 Nov 22 16:02 docs
drwxr-xr-x 2 root root 4096 Nov 22 16:02 notes
drwxr-xr-x 2 root root 4096 Nov 21 11:54 tests
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
./GLOSSARY.md
./README.md
./docs/adr/0001-use-sqlite-for-storage.md
./docs/adr/0002-record-architecture-decisions.md
./docs/adr/0003-cli-reaches-storage-only-through-store.md
./docs/adr/0004-export-as-json-lines.md
./docs/architecture/arc42.md
./docs/specs/export.md
./notes/__init__.py
./notes/__main__.py
./notes/cli.py
./notes/model.py
./notes/store.py
./tests/__init__.py
./tests/test_notes.py
----
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
----
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
----
```

### tool_use Bash

```json
{
 "command": "cat docs/adr/0003-cli-reaches-storage-only-through-store.md; echo ====; cat docs/architecture/arc42.md; echo ====; cat README.md GLOSSARY.md; echo ====; cat notes/model.py; echo ====; cat tests/test_notes.py; echo ====; cat docs/adr/0001-use-sqlite-for-storage.md | head -40",
 "description": "Read ADRs, architecture doc, README, model, and tests"
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
====
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
====
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
====
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str
====
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
        self.store = Store(Path(te
[... 1433 chars cut]
```

### tool_use Bash

```json
{
 "command": "ls /tmp/sa-arm-rhantp65/sa/skills/code-review/references/ && cat /tmp/sa-arm-rhantp65/sa/skills/code-review/references/architecture-axis.md; echo ====; cat /tmp/sa-arm-rhantp65/sa/skills/code-review/references/standards-and-smells.md",
 "description": "Read architecture-axis and standards references"
}
```

### tool_result

```
architecture-axis.md
receiving-feedback.md
reviewer-prompt.md
standards-and-smells.md
# The Architecture axis

Part of [code-review](../SKILL.md). Read this when `docs/architecture/arc42.md` exists: the
review then has three axes, Standards, Spec and Architecture, each with its own reviewer and its
own report section. Without that file the review keeps two axes and says nothing about
architecture.

## 1. Sources

Collect these before dispatching; the Architecture reviewer gets them and nothing else.

- **arc42 section 1:** the requirement IDs (`R-n`) and quality goal IDs (`QG-n`).
- **arc42 section 8:** every crosscutting rule, verbatim (error handling, logging, units).
- **arc42 section 10:** the quality scenarios (`QS-n`), each with its stimulus, response and
  measure.
- **ADRs:** every ADR in the directory that section 9 links, with its status.
  - Accepted, and so a rule: Status `accepted <date>`, `accepted (legacy)`, or no Status at all
    (a legacy ADR, as `domain-modeling` reads it).
  - Not a rule: `proposed` (an open decision) and `rejected`. A `superseded` ADR is replaced by
    the ADR that supersedes it.

ADRs, arc42 and other architecture notes are Architecture's sources here, not Standards'.

Done when: you hold the section 1 IDs, the section 8 rules, the section 10 scenarios and the
list of ADRs with their statuses.

## 2. Checks

The reviewer checks the diff against each source:

- **ADR conformance:** for each accepted ADR whose area the change falls in, does the diff keep
  its Decision? Quote the Decision sentence it breaks.
- **Section 8 rules:** does every new or changed code path follow every section 8 rule?
- **Quality scenarios:** for each `QS-n` whose stimulus or response the change bears on, does
  the change keep its measure? Name the scenario and say how the change affects it, even when
  the measure still holds.
- **Traceability:** an accepted ADR that the change adds or relies on, whose Context names no
  `R-n`, `QG-n` or `QS-n`, is a finding: nobody can tell which requirement it serves. A legacy
  ADR (`accepted (legacy)` or no Status) is exempt.
- **Open decisions:** a change that relies on a `proposed` ADR is a finding: it depends on an
  open decision. It neither conforms to nor breaks that ADR.

Done when: each accepted ADR in the change's area, each section 8 rule and each touched
scenario has a verdict, and each ADR the change adds or relies on has a traceability verdict.

## 3. Report

Each finding gives:

1. The location: `file:line`.
2. The source: `ADR-NNNN` and the Decision sentence, `arc42 §8: <rule>`, `QS-n`, or
   `traceability: ADR-NNNN`.
3. The evidence: the quoted hunk.
4. The fix: one sentence.

Severity is graded as on the other axes. A breach of an accepted ADR or a section 8 rule is a
documented-rule breach, never a judgement call.

Done when: every finding names its source.

## 4. Dispatch and aggregate

- Dispatch a third reviewer with the Architecture block of
  [reviewer-prompt.md](reviewer-prompt.md), together with the Standards and Spec reviewers.
  Fill `{ARCHITECTURE_SOURCES}` with the sources from step 1, pasted.
- Give the Standards reviewer no ADR or arc42 file: a breach of an ADR or a section 8 rule is
  reported under Architecture, not Standards.
- Present `## Architecture` beside `## Standards` and `## Spec`, as its own section.
- The closing line names the findings and the worst issue for each of the three axes.

Done when: the report has an `## Architecture` section and the closing line covers it.

## Red flags

| Thought | Reality |
|---|---|
| "The ADR breach is a coding-standard breach" | ADRs and section 8 rules are Architecture's sources. Report it there. |
| "The ADR is proposed, but the change follows it, so it conforms" | A proposed ADR is not a rule. Report that the change depends on an open decision. |
| "The new ADR is accepted, so it needs no check" | Accepted ADRs are what traceability checks. Name the missing ID. |
| "No scenario's measure brok
[... 5258 chars cut]
```

### tool_use Bash

```json
{
 "command": "export PYTHONDONTWRITEBYTECODE=1; D=$(mktemp -d); echo \"--- missing db:\"; NOTES_DB=$D/none.db python3 -m notes export; echo \"exit=$?\"; ls $D; echo \"--- populated db:\"; NOTES_DB=$D/ok.db python3 -m notes add $'line1\\nline2'; NOTES_DB=$D/ok.db python3 -m notes add 'Café'; NOTES_DB=$D/ok.db python3 -m notes export; echo \"exit=$?\"; echo \"--- args:\"; NOTES_DB=$D/ok.db python3 -m notes export extra; echo \"exit=$?\"; echo \"--- unreadable path:\"; NOTES_DB=/nonexistent/dir/x.db python3 -m notes export; echo \"exit=$?\"; echo \"--- list on same bad path (for comparison):\"; NOTES_DB=/nonexistent/dir/x.db python3 -m notes list; echo \"exit=$?\"; echo \"--- tests:\"; python3 -m unittest 2>&1 | tail -3; git status --short",
 "description": "Run export in temp DBs and existing tests without writing bytecode"
}
```

### tool_result

```
--- missing db:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/sa-eval-_9j2j14w/project/notes/__main__.py", line 5, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/sa-eval-_9j2j14w/project/notes/cli.py", line 19, in main
    rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")
sqlite3.OperationalError: no such table: notes
exit=1
none.db
--- populated db:
1
2
{"id": 1, "text": "line1\nline2", "created": "2026-11-22T15:09:12+00:00"}
{"id": 2, "text": "Caf\u00e9", "created": "2026-11-22T15:09:13+00:00"}
exit=0
--- args:
usage: notes [-h] {add,list,search,export} ...
notes: error: unrecognized arguments: extra
exit=2
--- unreadable path:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/sa-eval-_9j2j14w/project/notes/__main__.py", line 5, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/sa-eval-_9j2j14w/project/notes/cli.py", line 18, in main
    db = sqlite3.connect(default_path())
sqlite3.OperationalError: unable to open database file
exit=1
--- list on same bad path (for comparison):
notes: unable to open database file
exit=1
--- tests:
Ran 3 tests in 0.085s

OK
```

### assistant

Review of `HEAD~1..HEAD` (`86784f6..b2e7681`, "feat: export notes as JSON") against the spec `docs/specs/export.md`. I changed no files.

Two notes on the setup. The repo has no `main` branch, only `master`, so I used `HEAD~1` as the base, as you specified. `docs/architecture/arc42.md` exists, so the review has three axes, not two.

## Architecture

- **[Important] ADR-0003 breach.** `notes/cli.py:4` adds `import sqlite3`, and `cli.py:18-19` opens the database and runs raw SQL. ADR-0003's Decision says: "Only `notes/store.py` imports `sqlite3` or touches the database file. `notes/cli.py` uses the `Store` class and the `Note` value." Fix: add the export query to `Store` (or reuse `Store.all()`) and format the output in `cli.py`.
- **[Important] arc42 §8 breach.** §8 says errors go to stderr as `notes: <message>` with exit code 1. The export branch returns before the `try/except` that other commands use, so errors escape as a traceback. I reproduced this: `NOTES_DB=/nonexistent/dir/x.db python3 -m notes export` prints a Python traceback, while `list` on the same path prints `notes: unable to open database file`. Fix: route the export branch through the same error handling.
- **[Important] QS-3 weakened.** QS-3's measure is "0 other files changed" when the storage engine is swapped. Storage access now also lives in `cli.py`, so a storage change touches a file outside `store.py`. Fix: the same move as the ADR-0003 finding.
- **[Minor] Traceability.** ADR-0004 is `accepted`, not legacy, and its Context names no `R-n`, `QG-n` or `QS-n`. No requirement in arc42 §1 covers export either. Fix: add a requirement to §1 and cite it in ADR-0004.

Unaffected: QS-1 (read-only path) and QS-2 (stdlib only).

## Standards

No `CODING_STANDARDS.md`, `CONTRIBUTING.md` or lint config exists. Only the smell baseline applies.

- **[Minor] Possible Duplicated Code** (judgement call). `cli.py:19` repeats the `SELECT id, text, created FROM notes ORDER BY id` query and row shaping from `store.py`'s `all()`. Fix: call `store.all()` and serialise the `Note` values. The rule breach itself is reported under Architecture.
- **[Minor] No test for `export`** (judgement call). `README.md` documents running `python3 -m unittest`, but no rule requires tests per command. `tests/test_notes.py` covers `add` and `search` only. Fix: add a CLI test that runs `main(["export"])` against a temp database.

## Spec

Conforms: one JSON object per line, keys `id`, `text`, `created` in that order, oldest first (`ORDER BY id`), no arguments (`notes export extra` exits 2), and newlines in note text are escaped.

- **[Important] Empty store fails.** The spec says the command "prints every note". With no notes it should print nothing and succeed. On a fresh install, `NOTES_DB=<new path> python3 -m notes export` raises `sqlite3.OperationalError: no such table: notes` with exit 1, and it leaves an empty database file behind. `Store.__init__` creates the table, but the export path skips `Store`. Fix: the same move as the Architecture finding, which gets the table creation for free.

## Summary

- Architecture: 4 findings. Worst: ADR-0003 breach (Important).
- Standards: 2 findings. Worst: possible Duplicated Code (Minor).
- Spec: 1 finding. Worst: empty store fails (Important).

All three Important items come from one root cause: the export branch in `cli.py` bypasses `Store`. Moving the query into `Store` and routing the branch through the existing `try/except` should fix all three.

### result (success)
