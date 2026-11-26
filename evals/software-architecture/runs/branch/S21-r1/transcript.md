### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 main HEAD && echo \"---\" && git log main..HEAD --oneline 2>/dev/null; echo \"--- log HEAD~1..HEAD\"; git log HEAD~1..HEAD --oneline; echo \"--- diff stat\"; git diff --stat main HEAD~1 HEAD 2>/dev/null; git diff --stat HEAD~1..HEAD; echo \"--- standards candidates\"; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS*' -o -iname 'CONTRIBUTING*' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'eslint*' -o -iname '.prettierrc*' -o -iname 'README*' \\) -print; ls docs docs/specs 2>/dev/null",
 "description": "Resolve refs, list commits, diff stat, find standards files"
}
```

### tool_result

```
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
d4f2f47f661ab39877029d3cd1cf5ee0625ce2ff
main
--- log HEAD~1..HEAD
24f3111 feat: export notes to a file atomically
--- diff stat
 docs/specs/export.md | 20 ++++++++++++++++++++
 notes/cli.py         |  6 ++++++
 notes/store.py       | 12 ++++++++++++
 3 files changed, 38 insertions(+)
--- standards candidates
./README.md
docs:
adr
architecture
specs

docs/specs:
export.md
```

### tool_use Bash

```json
{
 "command": "git branch -a; echo \"---\"; git log --oneline -5; echo \"---\"; ls docs/architecture docs/adr; echo \"---\"; git diff HEAD~1 HEAD; echo \"--- spec\"; cat docs/specs/export.md; echo \"--- README\"; cat README.md",
 "description": "Check branches, architecture docs, diff, spec, README"
}
```

### tool_result

```
* master
---
24f3111 feat: export notes to a file atomically
d4f2f47 fixture
---
docs/adr:
0001-use-sqlite-for-storage.md
0002-record-architecture-decisions.md
0003-cli-reaches-storage-only-through-store.md
0004-write-notes-atomically.md
0005-add-postgresql-backend.md

docs/architecture:
arc42.md
---
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
--- spec
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
--- README
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
 "command": "S=/tmp/sa-arm-ygo9papq/sa/skills/code-review/references; cat $S/architecture-axis.md; echo \"=== REVIEWER\"; cat $S/reviewer-prompt.md; echo \"=== STANDARDS\"; cat $S/standards-and-smells.md",
 "description": "Read code-review reference files"
}
```

### tool_result

```
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
| "No scenario's measure broke, so there is nothing to say about quality" | Name each scenario the change touches a
[... 12384 chars cut]
```

### tool_use Bash

```json
{
 "command": "cat docs/architecture/arc42.md; echo \"=== ADRs\"; for f in docs/adr/*.md; do echo \"--- $f\"; cat \"$f\"; done",
 "description": "Read architecture doc and ADRs"
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
=== ADRs
--- docs/adr/0001-use-sqlite-for-storage.md
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
--- docs/adr/0002-record-architecture-decisions.md
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

Work tha
[... 1478 chars cut]
```

### tool_use Bash

```json
{
 "command": "echo \"=== store.py\"; cat notes/store.py; echo \"=== cli.py\"; cat notes/cli.py; echo \"=== tests\"; ls tests 2>/dev/null; ls notes",
 "description": "Read store, cli source and test layout"
}
```

### tool_result

```
=== store.py
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
=== cli.py
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
    except OSError as e:  # arc42 section 8
        print(f"notes: {e}", file=sys.stderr)
        return 1
    finally:
        store.close()
    return 0
=== tests
__init__.py
test_notes.py
__init__.py
__main__.py
cli.py
model.py
store.py
```

### tool_use Bash

```json
{
 "command": "ls -a; grep -n \"export\" tests/test_notes.py; echo \"--- pyproject/ruff/setup\"; ls pyproject.toml setup.cfg ruff.toml .flake8 tox.ini 2>/dev/null; echo \"--- run tests (no bytecode, temp db)\"; T=$(mktemp -d); PYTHONDONTWRITEBYTECODE=1 NOTES_DB=$T/n.db python3 -m unittest 2>&1 | tail -5; echo \"--- manual export\"; PYTHONDONTWRITEBYTECODE=1 NOTES_DB=$T/n.db python3 -m notes add \"Buy milk\" >/dev/null; PYTHONDONTWRITEBYTECODE=1 NOTES_DB=$T/n.db python3 -m notes add \"café\" >/dev/null; cd $T && PYTHONDONTWRITEBYTECODE=1 NOTES_DB=$T/n.db PYTHONPATH=/tmp/sa-eval-qn669d9m/project python3 -m notes export out.jsonl; echo \"rc=$?\"; cat out.jsonl; ls -a $T; mkdir $T/d; PYTHONDONTWRITEBYTECODE=1 NOTES_DB=$T/n.db PYTHONPATH=/tmp/sa-eval-qn669d9m/project python3 -m notes export $T/d; echo \"rc dir=$?\"; ls -a $T; echo \"--- relevant tests & line lengths\"; awk 'length > 99 {print FILENAME\": \"FNR\": \"length}' /tmp/sa-eval-qn669d9m/project/notes/*.py",
 "description": "Check tests, configs; run suite and manual export in temp dir"
}
```

### tool_result

```
.
..
.git
GLOSSARY.md
README.md
docs
notes
tests
--- pyproject/ruff/setup
--- run tests (no bytecode, temp db)
...
----------------------------------------------------------------------
Ran 3 tests in 0.071s

OK
--- manual export
rc=0
{"id": 1, "text": "Buy milk", "created": "2026-11-22T17:20:59+00:00"}
{"id": 2, "text": "caf\u00e9", "created": "2026-11-22T17:20:59+00:00"}
.
..
n.db
out.jsonl
notes: [Errno 21] Is a directory: '/tmp/tmp.zY75E35Ffi/d.tmp' -> '/tmp/tmp.zY75E35Ffi/d'
rc dir=1
.
..
d
d.tmp
n.db
out.jsonl
--- relevant tests & line lengths
/tmp/sa-eval-qn669d9m/project/notes/store.py: 33: 100
/tmp/sa-eval-qn669d9m/project/notes/store.py: 43: 103
Shell cwd was reset to /tmp/sa-eval-qn669d9m/project
```

### tool_use Bash

```json
{
 "command": "grep -n \"def export\\|os.replace\\|os.fsync\\|json.dumps\\|with_name\\|import json\" notes/store.py; grep -n \"except OSError\\|export\" notes/cli.py; grep -n \"def test\" tests/test_notes.py; git status --short",
 "description": "Get exact line numbers for cited code"
}
```

### tool_result

```
2:import json
37:    def export(self, path):
40:        tmp = path.with_name(path.name + ".tmp")
43:                f.write(json.dumps({"id": note.id, "text": note.text, "created": note.created}) + "\n")
45:            os.fsync(f.fileno())
46:        os.replace(tmp, path)
13:    sub.add_parser("export", help="write all notes as JSON lines to a file").add_argument("path")
24:        elif args.command == "export":
25:            store.export(args.path)
30:    except OSError as e:  # arc42 section 8
20:    def test_add_then_list(self):
24:    def test_search_matches_substring(self):
31:    def test_add_and_search(self):
```

### assistant

# Code review: `24f3111` (export notes to a file atomically) against `d4f2f47`

**Range:** `d4f2f47..24f3111` (one commit, so three-dot and two-dot are the same). The repo has no `main` branch, only `master`, so I used the parent commit as "main's state before it." **Spec:** `docs/specs/export.md`. `docs/architecture/arc42.md` exists, so the review has three axes. I ran each axis as a separate pass rather than dispatching reviewers. I changed no files. I ran `python3 -m unittest` (3 tests, OK) and a manual export into a temp dir.

## Standards

**Done well:** the change follows the existing `Store` / `cli` split, and the new code is stdlib-only.

- **Important (judgement call): no test for `export`.** `tests/test_notes.py` has three tests, none covering export. The output format and the atomic-rename path are unverified. Cited: `notes/store.py:37-46`, `notes/cli.py:13,24-25`. Fix: add a test that exports and checks the JSON lines.
- **Minor (judgement call):** `notes/store.py:43` is 103 characters, longer than any other line in the file. No line-length rule is documented and no linter config exists, so this is only a style note.

Documented standards: none found (no `CODING_STANDARDS.md`, `CONTRIBUTING.md`, or lint config; README has no style section). No baseline smell clearly matches.

**Worst within axis:** Important (missing test).

## Spec

**Met:** `notes export PATH` writes one JSON line per note, oldest first (`ORDER BY id`), with fields `id`, `text`, `created`. The write goes to a temp file in the same directory, is fsynced, then renamed over `PATH`, so a crash leaves the old or the complete new file. The manual run produced the expected two lines and exited 0.

- **Important: a failed export leaves debris.** Running `notes export <existing-dir>` printed `notes: [Errno 21] Is a directory: '.../d.tmp' -> '.../d'`, exited 1, and left `d.tmp` behind. Any exception raised after the temp file is opened does the same. The spec is silent on this, but a user would not expect a stray file next to their target. Fix: remove the temp file on failure, e.g. `try/except BaseException: os.unlink(tmp); raise`.
- **Minor:** an existing file named `PATH.tmp` is silently overwritten. Same fix area.
- **Minor (scope):** `notes/cli.py:30` adds an `except OSError` that covers `add`, `list` and `search` too, not just `export`. It matches arc42 §8, so it may be intended, but it changes existing commands and should be confirmed.

Declined to judge:
- No success message on export. The spec is silent; a silent success is a normal convention.
- No directory fsync after `os.replace`. The spec's "old or complete" guarantee holds without it.
- Export on a fresh system creates the database, as `list` already does.

**Worst within axis:** Important (stray `.tmp` on failure).

## Architecture

Sources: arc42 §8 (errors to stderr as `notes: <message>`, exit 1); ADR-0001, 0002, 0003 accepted; ADR-0004 and 0005 proposed; QS-1 to QS-3.

- **Important: relies on a proposed ADR.** `notes/store.py:37-46` implements and cites ADR-0004 ("Write notes atomically via a temporary file and rename"), whose Status is `proposed`. The change depends on an open decision. It neither conforms to nor breaks that ADR. Fix: get ADR-0004 accepted before merging, or drop the dependency.
- **Important: export format and command name without an accepted ADR.** ADR-0002's Decision centrally decides "import and export formats" and "CLI command names." Its Consequences say "Work that depends on a decision on the list waits until its ADR is accepted." The JSON-lines format (`store.py:43`) and the `export` command (`cli.py:13`) have no accepted ADR. Fix: write and accept an export-format ADR, or get the architect's explicit sign-off.

Conforming:
- ADR-0003: only `store.py` touches storage; `cli.py` calls `Store.export`.
- §8: the new `OSError` path prints to stderr and exits 1.
- QS-1 is untouched. QS-3's measure holds: a storage swap still changes only `store.py`, because export reads through `self.all()`.
- R-3: no new dependencies (`json`, `os`, `pathlib` are stdlib).

**Worst within axis:** Important (proposed ADR relied on).

---

**Summary per axis:** Standards 2 findings, worst Important (no export test). Spec 3 findings, worst Important (stray `.tmp` on failure). Architecture 2 findings, worst Important (depends on proposed ADR-0004).

### result (success)
