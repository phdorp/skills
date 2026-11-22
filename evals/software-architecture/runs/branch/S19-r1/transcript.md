### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 HEAD main 2>&1; echo ---; git log HEAD~1..HEAD --oneline; echo ---; git diff --stat HEAD~1..HEAD; echo ---; ls docs docs/specs docs/architecture 2>&1; echo ---; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'arc42.md' \\) -print",
 "description": "Resolve refs, list commit, diffstat, and find standards files"
}
```

### tool_result

```
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
86784f6c5d2a529595b63e1975ee969fe2439d00
b2e768114ef39f0973455cfd5c9a0d12ba68dabd
main
---
b2e7681 feat: export notes as JSON
---
 docs/adr/0004-export-as-json-lines.md | 20 ++++++++++++++++++++
 docs/specs/export.md                  | 19 +++++++++++++++++++
 notes/cli.py                          | 10 ++++++++++
 3 files changed, 49 insertions(+)
---
docs:
adr
architecture
specs

docs/architecture:
arc42.md

docs/specs:
export.md
---
./docs/architecture/arc42.md
```

### tool_use Bash

```json
{
 "command": "git diff HEAD~1..HEAD",
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
 "command": "cat /tmp/sa-arm-z6ntv9bk/sa/skills/code-review/references/architecture-axis.md; echo ======; cat docs/architecture/arc42.md; echo ======; ls -R notes tests 2>/dev/null; echo ======; cat notes/cli.py; echo ======; cat notes/store.py 2>/dev/null; echo ======; cat /tmp/sa-arm-z6ntv9bk/sa/skills/code-review/references/standards-and-smells.md | head -80",
 "description": "Read architecture axis reference, arc42, and source files"
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
[... 10665 chars cut]
```

### tool_use Bash

```json
{
 "command": "ls docs/adr; for f in docs/adr/000[123]*.md; do echo \"== $f\"; cat \"$f\"; done; echo ======; cat tests/test_notes.py; echo ======; cat notes/model.py; echo ======; ls GLOSSARY.md 2>&1; git status --short",
 "description": "Read ADRs, tests, and check working tree"
}
```

### tool_result

```
0001-use-sqlite-for-storage.md
0002-record-architecture-decisions.md
0003-cli-reaches-storage-only-through-store.md
0004-export-as-json-lines.md
== docs/adr/0001-use-sqlite-for-storage.md
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
== docs/adr/0002-record-architecture-decisions.md
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
== docs/adr/0003-cli-reaches-storage-only-through-store.md
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
======
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
======
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str
======
GLOSSARY.md
```

### tool_use Bash

```json
{
 "command": "D=$(mktemp -d) && echo \"fresh db: $D/fresh.db\" && NOTES_DB=$D/fresh.db PYTHONPATH=. python3 -m notes export; echo \"exit=$?\"; echo ---; NOTES_DB=$D/n.db PYTHONPATH=. python3 -m notes add 'line one\nline two \"q\" é' >/dev/null && NOTES_DB=$D/n.db PYTHONPATH=. python3 -m notes export; echo \"exit=$?\"; echo ---; NOTES_DB=/nonexistent/dir/x.db PYTHONPATH=. python3 -m notes export 2>&1 | tail -2; echo \"exit=${PIPESTATUS[0]}\"; echo ---; PYTHONPATH=. python3 -m pytest -q 2>&1 | tail -3; python3 -m unittest discover -s tests -q 2>&1 | tail -3",
 "description": "Run export on fresh, populated, and bad-path DBs, then tests"
}
```

### tool_result

```
fresh db: /tmp/tmp.hefQVECkzU/fresh.db
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/sa-eval-p9zdrvrd/project/notes/__main__.py", line 5, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/sa-eval-p9zdrvrd/project/notes/cli.py", line 19, in main
    rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")
sqlite3.OperationalError: no such table: notes
exit=1
---
{"id": 1, "text": "line one\nline two \"q\" \u00e9", "created": "2026-11-22T15:09:06+00:00"}
exit=0
---
    db = sqlite3.connect(default_path())
sqlite3.OperationalError: unable to open database file
exit=1
---
/usr/bin/python3: No module named pytest
Ran 3 tests in 0.073s

OK
```

### assistant

Base: the repo has no `main` branch, so I used `HEAD~1` (86784f6) as the fixed point, which is the state before `b2e7681`. No files were changed. I ran the export against temporary databases and ran the test suite; I did the review inline rather than dispatching reviewers.

## Standards

No documented standards exist here (no `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, lint or editor config). Findings use the smell baseline, so each is a judgement call.

- **possible Duplicated Code** (`notes/cli.py:19`): the `SELECT id, text, created FROM notes ORDER BY id` query and the row-to-note mapping repeat `Store.all()` (`notes/store.py:28`). Fix: call `store.all()` and format the returned `Note` values.
- **possible Divergent Change** (`notes/cli.py:17-23`): `main()` gains a second storage path, so it now changes for storage reasons as well as CLI reasons. Fix: move the query into `Store`, as in the Architecture finding below.
- **Inconsistent resource handling** (`notes/cli.py:18-22`): `db.close()` is not in a `finally`, unlike the store path directly below (`cli.py:30-40`). Fix: follow the file's own pattern, or drop the raw connection entirely (see the Architecture finding).

## Spec

`docs/specs/export.md` is implemented as written. With a populated database, output is one JSON object per line, oldest first, with `id`, `text`, `created`, and no arguments. Newlines in note text are escaped correctly.

- **Important, empty or fresh store** (`notes/cli.py:18-19`): the spec says the command prints every note. With no notes, the table has not been created yet, so the command crashes with `sqlite3.OperationalError: no such table: notes` and a traceback, exit 1. I reproduced this on a fresh `NOTES_DB`. The expected behaviour is empty output and exit 0. Fix: open the database through `Store(default_path())` first, which creates the table, then export through the store.
- **Minor, no test** (`tests/test_notes.py`, unchanged): nothing exercises `export`. The spec does not require a test, but this is why the crash above went unnoticed.

## Architecture

Sources: arc42 §5, §8, §10 (QS-3), ADR-0002, ADR-0003, ADR-0004.

- **Important, breach of ADR-0003** (`notes/cli.py:3, 18`): the accepted Decision says "Only `notes/store.py` imports `sqlite3` or touches the database file." `cli.py` now imports `sqlite3`, calls `sqlite3.connect`, and runs SQL. Fix: add an export or read method to `Store`, and have `cli.py` call it with the same `try`/`finally` as the other commands.
- **Important, arc42 §8 error convention** (`notes/cli.py:18-19`): errors are supposed to go to stderr as `notes: <message>` with exit 1. The export path has no `try`, so sqlite errors surface as tracebacks. I reproduced this with `NOTES_DB=/nonexistent/dir/x.db`, which prints `sqlite3.OperationalError: unable to open database file` as a traceback. Fix: route through the same `try`/`except` as the other commands. Moving the query into `Store` covers this too.
- **Minor, weakened QS-3** (arc42 §10): the measure "0 other files changed" when the storage engine is swapped no longer holds, because `cli.py` now depends on the storage engine. Fix: the same as the ADR-0003 finding.
- **Minor, traceability** (`docs/adr/0004-export-as-json-lines.md:7-8`): ADR-0004 is accepted and its Context names no `R-n`, `QG-n` or `QS-n`, so nobody can tell which requirement it serves. Fix: the architect should name the requirement in Context, or add one to arc42 §1 if none fits. This is for you to decide, not me.

Worst issue per axis: Standards, duplicated query (judgement call); Spec, crash on an empty or fresh store; Architecture, breach of ADR-0003 (sqlite access outside `store.py`).

### result (success)
