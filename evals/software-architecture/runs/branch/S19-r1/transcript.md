### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "BASE_SHA=$(git rev-parse HEAD~1) && HEAD_SHA=$(git rev-parse HEAD) && echo \"BASE $BASE_SHA\" && echo \"HEAD $HEAD_SHA\" && git log HEAD~1..HEAD --oneline && git diff --stat HEAD~1..HEAD && ls docs docs/specs docs/architecture 2>&1; ls -a; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS.md' -o -iname 'CONTRIBUTING.md' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '*style*.md' -o -iname '.editorconfig' -o -iname '.eslintrc*' -o -iname 'biome.json*' -o -iname '.prettierrc*' \\) -print",
 "description": "Resolve SHAs, list commits, diff stats, and find standards files"
}
```

### tool_result

```
BASE 61604089270ba97dde5c260ae761e738d364b5b9
HEAD 13c3cf27907ecaa2284bd514ade7bef1f5753231
13c3cf2 feat: export notes as JSON
 docs/adr/0004-export-as-json-lines.md | 20 ++++++++++++++++++++
 docs/specs/export.md                  | 19 +++++++++++++++++++
 notes/cli.py                          | 10 ++++++++++
 3 files changed, 49 insertions(+)
docs:
adr
architecture
specs

docs/architecture:
arc42.md

docs/specs:
export.md
.
..
.git
GLOSSARY.md
README.md
docs
notes
tests
```

### tool_use Bash

```json
{
 "command": "git diff HEAD~1...HEAD 2>/dev/null || git diff HEAD~1 HEAD",
 "description": "Show the full diff of the last commit"
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
 "command": "cat /tmp/sa-arm-0irqx61n/sa/skills/code-review/references/architecture-axis.md; echo ----; cat /tmp/sa-arm-0irqx61n/sa/skills/code-review/references/standards-and-smells.md | head -80; echo ----; cat docs/architecture/arc42.md; echo ----; cat notes/store.py; echo ----; cat README.md GLOSSARY.md; ls notes tests docs/adr; cat docs/adr/*.md | head -150",
 "description": "Read review references, architecture doc, store module, and docs"
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
[... 12042 chars cut]
```

### tool_use Bash

```json
{
 "command": "cat notes/cli.py && echo ---- && grep -n \"def test\\|export\" tests/test_notes.py | head -40 && echo ---- && tmp=$(mktemp -d) && NOTES_DB=$tmp/fresh.db python3 -m notes export; echo \"exit=$?\"; ls -la $tmp; NOTES_DB=$tmp/new.db python3 -m notes add \"a\nb\" >/dev/null && NOTES_DB=$tmp/new.db python3 -m notes export; echo \"exit=$?\"; python3 -m unittest 2>&1 | tail -3",
 "description": "Read cli.py, grep tests, and exercise export on fresh and populated DBs"
}
```

### tool_result

```
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
20:    def test_add_then_list(self):
24:    def test_search_matches_substring(self):
31:    def test_add_and_search(self):
----
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/sa-eval-dv80fohw/project/notes/__main__.py", line 5, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/sa-eval-dv80fohw/project/notes/cli.py", line 19, in main
    rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")
sqlite3.OperationalError: no such table: notes
exit=1
total 516
drwx------     2 root root   4096 Nov 22 18:20 .
drwxrwxrwt 17990 root root 520192 Nov 22 18:20 ..
-rw-r--r--     1 root root      0 Nov 22 18:20 fresh.db
{"id": 1, "text": "a\nb", "created": "2026-11-22T17:20:47+00:00"}
exit=0
Ran 3 tests in 0.071s

OK
```

### assistant

**Reviewed:** `13c3cf2` "feat: export notes as JSON" (`6160408..13c3cf2`), 3 files: `notes/cli.py`, `docs/specs/export.md`, `docs/adr/0004-export-as-json-lines.md`. Spec: `docs/specs/export.md`. `docs/architecture/arc42.md` exists, so the review has three axes. No files were changed. I ran the export against a fresh and a populated temp DB under `/tmp`, and the existing tests pass (3 OK).

## Standards

No `CODING_STANDARDS.md`, `CONTRIBUTING.md`, or lint config exists in the repo, so the smell baseline applies.

1. **Possible Long Method** (judgement call), `notes/cli.py:17-23`. The export logic (connect, query, print, close) sits inline in `main()`, between argument parsing and the store-based dispatch. → Move it into a named function, or into `Store` (see Architecture).
2. **No test for export** (judgement call), `tests/test_notes.py`. `add`, `list` and `search` each have tests; `export` has none. That is why the fresh-DB crash below went unnoticed. → Add a test that runs `export` against a temp `NOTES_DB`.

**Worst Standards issue:** Minor (possible Long Method).

## Spec

Spec conformance holds for populated databases: fields `id`, `text`, `created`, oldest first, no arguments, and newlines inside a note are escaped on one line. The gap is an empty or fresh database:

- **Important**, `notes/cli.py:18`. With `NOTES_DB` pointing at a new file, `sqlite3.connect` creates an empty file, and the query then fails with `sqlite3.OperationalError: no such table: notes` and a traceback, exit 1. The spec says the command prints every note, so a store with none should print nothing and exit 0. Store's `__init__` creates the table; this path skips it. → Create the table, or route through `Store`, which already does.

**Worst Spec issue:** Important (fresh-DB crash).

## Architecture

- **Critical: ADR-0003 breach**, `notes/cli.py:3` and `notes/cli.py:18-19`. ADR-0003 (accepted) says "Only `notes/store.py` imports `sqlite3` or touches the database file." This diff imports `sqlite3` in `cli.py` and runs SQL there. arc42 §5 also says `store` is "the only block that knows the storage." Quoted hunk: `db = sqlite3.connect(default_path())` / `rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")`. → Use the existing `Store.all()` and drop the `sqlite3` import from `cli.py`.
- **Important: arc42 §8 error rule**, `notes/cli.py:18`. The export path sits before the `try` that reports errors as `notes: <message>` on stderr with exit 1. The fresh-DB failure therefore escapes as a traceback. This is the same root cause as the Spec finding; the fix above covers both.
- **Minor: traceability**, `docs/adr/0004-export-as-json-lines.md:9-11`. ADR-0004 is accepted, and its Context names no `R-n`, `QG-n` or `QS-n`, so nobody can tell which requirement it serves. R-1 (CLI use) looks like the candidate, but that is your call as the architect. → Name the requirement in Context.
- **Quality scenario QS-3 weakened**, measure "0 other files changed" for swapping the storage engine (arc42 §10). After this diff, a storage swap must also change `notes/cli.py`. → Resolved by the `Store.all()` fix above.

**Worst Architecture issue:** Critical (ADR-0003 breach).

---

**Summary:** Standards: 2 findings, worst Minor. Spec: 1 finding, worst Important. Architecture: 3 findings, worst Critical.

### result (success)
