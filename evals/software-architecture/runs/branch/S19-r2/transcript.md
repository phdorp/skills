### user

/sa:code-review Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.

### tool_use Bash

```json
{
 "command": "git rev-parse HEAD~1 HEAD main && git log HEAD~1..HEAD --oneline && git diff HEAD~1..HEAD --stat && git diff HEAD~1..HEAD && echo ---SPEC--- && ls docs docs/specs 2>/dev/null; ls -a; find . -path ./.git -prune -o \\( -iname 'CODING_STANDARDS*' -o -iname 'CONTRIBUTING*' -o -iname 'AGENTS.md' -o -iname 'CLAUDE.md' -o -iname '.editorconfig' -o -iname 'STANDARDS*' \\) -print",
 "description": "Resolve SHAs, show last commit diff, list spec and standards files"
}
```

### tool_result

```
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
21d00184f0eba051a9da3fc41661484e5986544e
7b808460ba6d7f67add4ad9fca4f8522884be943
main
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
 "command": "git branch -a && git log --oneline --all | head -20 && echo --- && git diff HEAD~1..HEAD --stat && git diff HEAD~1..HEAD && echo ---SPEC--- && find docs notes tests -type f | head -100 && echo --- && cat README.md GLOSSARY.md | head -150",
 "description": "List branches, last commit diff, and project files"
}
```

### tool_result

```
* master
7b80846 feat: export notes as JSON
21d0018 fixture
---
 docs/adr/0004-export-as-json-lines.md | 20 ++++++++++++++++++++
 docs/specs/export.md                  | 19 +++++++++++++++++++
 notes/cli.py                          | 10 ++++++++++
 3 files changed, 49 insertions(+)
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
---SPEC---
notes/__main__.py
notes/cli.py
notes/store.py
notes/__init__.py
notes/model.py
tests/test_notes.py
tests/__init__.py
docs/adr/0002-record-architecture-decisions.md
docs/adr/0004-export-as-json-lines.md
docs/adr/0003-cli-reaches-storage-only-through-store.md
docs/adr/0001-use-sqlite-for-storage.md
docs/architecture/arc42.md
docs/specs/export.md
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
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
```

### tool_use Bash

```json
{
 "command": "cat docs/architecture/arc42.md && echo ---ADRS--- && cat docs/adr/0002-record-architecture-decisions.md docs/adr/0003-cli-reaches-storage-only-through-store.md docs/adr/0001-use-sqlite-for-storage.md && echo ---CODE--- && cat notes/cli.py notes/store.py notes/model.py notes/__main__.py && echo ---TESTS--- && cat tests/test_notes.py",
 "description": "Read architecture doc, ADRs, and source files"
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
---ADRS---
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
# 1. Use SQLite for storage

## Status

accepted 2026-10-01

## Context

Notes must
[... 4532 chars cut]
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-arm-pdfa8oob/sa/skills/code-review/references/architecture-axis.md"
}
```

### tool_result

```
1	# The Architecture axis
2	
3	Part of [code-review](../SKILL.md). Read this when `docs/architecture/arc42.md` exists: the
4	review then has three axes, Standards, Spec and Architecture, each with its own reviewer and its
5	own report section. Without that file the review keeps two axes and says nothing about
6	architecture.
7	
8	## 1. Sources
9	
10	Collect these before dispatching; the Architecture reviewer gets them and nothing else.
11	
12	- **arc42 section 1:** the requirement IDs (`R-n`) and quality goal IDs (`QG-n`).
13	- **arc42 section 8:** every crosscutting rule, verbatim (error handling, logging, units).
14	- **arc42 section 10:** the quality scenarios (`QS-n`), each with its stimulus, response and
15	  measure.
16	- **ADRs:** every ADR in the directory that section 9 links, with its status.
17	  - Accepted, and so a rule: Status `accepted <date>`, `accepted (legacy)`, or no Status at all
18	    (a legacy ADR, as `domain-modeling` reads it).
19	  - Not a rule: `proposed` (an open decision) and `rejected`. A `superseded` ADR is replaced by
20	    the ADR that supersedes it.
21	
22	ADRs, arc42 and other architecture notes are Architecture's sources here, not Standards'.
23	
24	Done when: you hold the section 1 IDs, the section 8 rules, the section 10 scenarios and the
25	list of ADRs with their statuses.
26	
27	## 2. Checks
28	
29	The reviewer checks the diff against each source:
30	
31	- **ADR conformance:** for each accepted ADR whose area the change falls in, does the diff keep
32	  its Decision? Quote the Decision sentence it breaks.
33	- **Section 8 rules:** does every new or changed code path follow every section 8 rule?
34	- **Quality scenarios:** for each `QS-n` whose stimulus or response the change bears on, does
35	  the change keep its measure? Name the scenario and say how the change affects it, even when
36	  the measure still holds.
37	- **Traceability:** an accepted ADR that the change adds or relies on, whose Context names no
38	  `R-n`, `QG-n` or `QS-n`, is a finding: nobody can tell which requirement it serves. A legacy
39	  ADR (`accepted (legacy)` or no Status) is exempt.
40	- **Open decisions:** a change that relies on a `proposed` ADR is a finding: it depends on an
41	  open decision. It neither conforms to nor breaks that ADR.
42	
43	Done when: each accepted ADR in the change's area, each section 8 rule and each touched
44	scenario has a verdict, and each ADR the change adds or relies on has a traceability verdict.
45	
46	## 3. Report
47	
48	Each finding gives:
49	
50	1. The location: `file:line`.
51	2. The source: `ADR-NNNN` and the Decision sentence, `arc42 §8: <rule>`, `QS-n`, or
52	   `traceability: ADR-NNNN`.
53	3. The evidence: the quoted hunk.
54	4. The fix: one sentence.
55	
56	Severity is graded as on the other axes. A breach of an accepted ADR or a section 8 rule is a
57	documented-rule breach, never a judgement call.
58	
59	Done when: every finding names its source.
60	
61	## 4. Dispatch and aggregate
62	
63	- Dispatch a third reviewer with the Architecture block of
64	  [reviewer-prompt.md](reviewer-prompt.md), together with the Standards and Spec reviewers.
65	  Fill `{ARCHITECTURE_SOURCES}` with the sources from step 1, pasted.
66	- Give the Standards reviewer no ADR or arc42 file: a breach of an ADR or a section 8 rule is
67	  reported under Architecture, not Standards.
68	- Present `## Architecture` beside `## Standards` and `## Spec`, as its own section.
69	- The closing line names the findings and the worst issue for each of the three axes.
70	
71	Done when: the report has an `## Architecture` section and the closing line covers it.
72	
73	## Red flags
74	
75	| Thought | Reality |
76	|---|---|
77	| "The ADR breach is a coding-standard breach" | ADRs and section 8 rules are Architecture's sources. Report it there. |
78	| "The ADR is proposed, but the change follows it, so it conforms" | A proposed ADR is not a rule. Report that the change depends on an open decision. |
79	| "The
[... 278 chars cut]
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-arm-pdfa8oob/sa/skills/code-review/references/reviewer-prompt.md"
}
```

### tool_result

```
1	# Two-axis reviewer prompt
2	
3	Fill this template once per axis (Standards, Spec, and Architecture when [architecture-axis.md](architecture-axis.md) applies) and dispatch each copy to a separate reviewer. Replace everything in `{}`. Delete the sections that belong to the other axes; a reviewer that sees another axis reranks them.
4	
5	```
6	You are a senior code reviewer. You review one axis of one change and report findings. You do not fix anything.
7	
8	## Axis
9	
10	{AXIS}  <!-- "Standards", "Spec" or "Architecture" -->
11	
12	## What was implemented
13	
14	{DESCRIPTION}
15	
16	## Global constraints
17	
18	- This review is read-only on this checkout. Do not mutate the working tree, the index, HEAD, or branch state. Inspect with `git show`, `git diff`, `git log`. If you need another revision checked out, use a separate temporary worktree (`git worktree add /tmp/review-<sha> <sha>`); never move HEAD here.
19	- Do all of the review yourself. Never spawn a subagent, and never ask another reviewer for a second opinion. If the diff feels too large for one pass, review it in passes and say so.
20	- Do not report anything tooling already enforces (formatter, linter, type checker, CI checks).
21	- Stay under 400 words. Findings only, no restating the change.
22	- {GLOBAL_CONSTRAINTS}  <!-- repo-wide rules: generated files to ignore, forbidden APIs, compatibility floors -->
23	
24	## Git range
25	
26	Diff (three-dot, against the merge-base):
27	
28	    {DIFF_COMMAND}
29	
30	Commits under review:
31	
32	    {COMMIT_LIST}
33	
34	Start from the diff. Read surrounding code when a hunk's correctness depends on it.
35	
36	## Spec  <!-- Spec axis only -->
37	
38	Path: {SPEC_PATH}
39	
40	Contents:
41	
42	{SPEC_CONTENTS}
43	
44	The spec is a vision document. It says what the software must do; it does not enumerate every input, environment, or condition. Where the spec is silent, judge by what a reasonable person using this software would expect. A reasonable person's expectation is a requirement, and the spec's silence is not permission. Grade such findings by their effect on that person, not by whether the spec mentions the trigger.
45	
46	## Standards  <!-- Standards axis only -->
47	
48	Documented sources in this repo:
49	
50	{STANDARDS_SOURCES}  <!-- file paths, or pasted rules when the reviewer cannot read them -->
51	
52	The repo overrides the baseline: where a documented standard endorses something the baseline would flag, suppress the smell. Never report a smell as a hard violation.
53	
54	Smell baseline (Fowler, _Refactoring_ ch. 3). Each entry is *what it is* → *how to fix*:
55	
56	{SMELL_BASELINE}
57	
58	## Architecture  <!-- Architecture axis only -->
59	
60	Sources (arc42 sections 1, 8 and 10; the ADRs with their statuses):
61	
62	{ARCHITECTURE_SOURCES}
63	
64	An ADR is a rule when its Status is `accepted <date>`, `accepted (legacy)` or missing (legacy). A `proposed` or `rejected` ADR is not a rule. A breach of an accepted ADR or a section 8 rule is a documented-rule breach, not a judgement call.
65	
66	## Declined to judge
67	
68	Before your verdict, list every behavior you considered and set aside as outside your axis, one line each, with the reason. The implementer rules on each line; nothing you set aside is dropped silently. An empty list means you set nothing aside.
69	
70	## What to check
71	
72	Standards axis:
73	
74	- Every place the diff violates a documented standard. Cite the standard (file + the rule).
75	- Any baseline smell you spot. Name it and quote the hunk. Label it a judgement call.
76	- Anything tooling does not cover but a maintainer would raise in review.
77	
78	Spec axis:
79	
80	- Requirements the spec asked for that are missing or partial.
81	- Behaviour in the diff that was not asked for (scope creep).
82	- Requirements that look implemented but where the implementation is wrong.
83	
84	Architecture axis:
85	
86	- Each accepted ADR whose area the change falls in: does the diff keep its Decision? Cite 
[... 3668 chars cut]
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-arm-pdfa8oob/sa/skills/code-review/references/standards-and-smells.md"
}
```

### tool_result

```
1	# Standards sources and the smell baseline
2	
3	The Standards axis asks whether the diff conforms to how this repo writes code. Two kinds of source answer that: what the repo documents, and a fixed baseline of code smells for what it does not.
4	
5	## 1. Find the documented standards
6	
7	Search the repo for every file that says how code should be written. Typical candidates:
8	
9	- `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `README.md` sections on style.
10	- `docs/` conventions, ADRs, architecture notes, review checklists, `STYLE.md`. When `docs/architecture/arc42.md` exists, ADRs and arc42 belong to the Architecture axis ([architecture-axis.md](architecture-axis.md)), not here.
11	- Linter and formatter configs (`.eslintrc*`, `eslint.config.*`, `ruff.toml`, `pyproject.toml`, `.golangci.yml`, `.rubocop.yml`, `.editorconfig`) — these show what tooling enforces, which you must not re-report.
12	- Language- or area-specific docs (`docs/api-guidelines.md`, `packages/*/README.md`).
13	- Domain vocabulary in `GLOSSARY.md`: a name that contradicts the glossary is a Mysterious Name finding with a documented fix.
14	
15	List the files you found and check they exist in the checkout at `HEAD`. The reviewer has no other way to read them if you only name a path, so either pass their contents or confirm the reviewer can read them in its own checkout.
16	
17	**Skip anything tooling already enforces.** A linter, formatter, or type checker that runs in CI owns those findings. Re-reporting them wastes the reviewer's budget and buries the judgement calls.
18	
19	## 2. Apply the smell baseline
20	
21	On top of whatever the repo documents, always carry this fixed set of Fowler code smells (_Refactoring_, ch. 3). Two rules bind it:
22	
23	- **The repo overrides.** A documented repo standard always wins. Where a repo standard endorses something the baseline would flag, suppress the smell and say nothing.
24	- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. A documented-standard breach can be hard; a smell cannot.
25	
26	Each smell reads *what it is* → *how to fix*. **(OO)** marks a smell that assumes objects and classes; its entry names the dataflow counterpart (blocks, connections, signals, as in `codebase-design`) where one exists. Match it against the diff:
27	
28	- **Long Method**: a function so long that its parts need comments or names of their own. → extract the parts into named functions.
29	- **Large Class**: a class or module holding many unrelated fields or responsibilities. → split it along its responsibilities.
30	- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
31	- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
32	- **Feature Envy** (OO): a method that reaches into another object's data more than its own. → move the method onto the data it envies. Dataflow: a block reading another block's internal variables instead of its outputs → read its output signal, or add one.
33	- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
34	- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
35	- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
36	- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
37	- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
38	- **Speculative Generality**: abstraction, p
[... 1274 chars cut]
```

### tool_use Bash

```json
{
 "command": "T=$(mktemp -d) && export NOTES_DB=$T/a.db && python3 -m notes add \"$(printf 'two\\nlines')\" >/dev/null && python3 -m notes add 'Buy \"milk\"' >/dev/null && python3 -m notes export; echo \"exit=$?\"; echo ---fresh---; NOTES_DB=$T/fresh.db python3 -m notes export; echo \"exit=$?\"; echo ---tests---; python3 -m unittest 2>&1 | tail -3; echo ---arch-grep---; grep -rn \"sqlite3\" notes/ | grep -v \"^notes/store.py\"; rm -rf $T",
 "description": "Exercise export on a temp DB, fresh DB, and run tests"
}
```

### tool_result

```
{"id": 1, "text": "two\nlines", "created": "2026-11-22T15:07:22+00:00"}
{"id": 2, "text": "Buy \"milk\"", "created": "2026-11-22T15:07:22+00:00"}
exit=0
---fresh---
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/sa-eval-8vr0y7fv/project/notes/__main__.py", line 5, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/sa-eval-8vr0y7fv/project/notes/cli.py", line 19, in main
    rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")
sqlite3.OperationalError: no such table: notes
exit=1
---tests---
Ran 3 tests in 0.064s

OK
---arch-grep---
notes/cli.py:3:import sqlite3
notes/cli.py:18:        db = sqlite3.connect(default_path())
```

### assistant

## Standards

No documented coding standards exist in the repo (no `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, or lint config). The ADRs and arc42 belong to the Architecture axis. Judgement calls only:

1. **Possible Long Method**, `notes/cli.py:15-21`. The export branch is inlined in `main()` ahead of the `Store` setup. Fix: extract `_export(...)` and call it from `main()`. You decide.
2. **Test gap**, `tests/test_notes.py`. `CliTest` covers only `add` and `search`. Nothing exercises `export`, including the newline escaping and the oldest-first order that the spec states. A maintainer would likely raise this in review.

## Spec

The core behaviour matches `docs/specs/export.md`. I ran it against a temp DB: one JSON object per line, keys `id`, `text`, `created`, oldest first, newlines in notes escaped onto one line, and no arguments. The existing suite passes (`python3 -m unittest`, 3 tests).

1. **Important: unspecified failure mode**, `notes/cli.py:18-19`. The spec is silent on a missing database, but a reasonable user expects a clean error, not a crash. `notes export` against a fresh path prints a traceback (`sqlite3.OperationalError: no such table: notes`) and exits 1. The other commands report `notes: <message>` on stderr, so this is inconsistent with them.

No scope creep found.

## Architecture

1. **Critical: ADR-0003 breach**, `notes/cli.py:3` and `:18`. ADR-0003 (accepted) states: "Only `notes/store.py` imports `sqlite3` or touches the database file. `notes/cli.py` uses the `Store` class and the `Note` value." The commit adds `import sqlite3` and a direct query in the CLI. Fix: drop the export branch's own connection and use `store.all()`, which already returns `Note` values, after the existing `Store` setup.
2. **Important: arc42 §8 breach**, `notes/cli.py:18-21`. §8 says errors go to stderr as `notes: <message>` with exit code 1. The export path sits outside the `try` that handles that, so a sqlite error becomes a traceback. The fix in item 1 also resolves this, because the export would then run inside the existing error handling.
3. **Important: traceability**, `docs/adr/0004-export-as-json-lines.md`. ADR-0004 is accepted, but its Context names no `R-n`, `QG-n` or `QS-n`. Arc42 §1 has no requirement for exporting. Fix: add a requirement to arc42 §1 and cite it in the ADR's Context, or cite the closest existing one.
4. **Important: QS-3 weakened**, `docs/architecture/arc42.md` §10. The measure says a storage swap changes only `notes/store.py` and its tests, with 0 other files. Because `cli.py` now talks to SQLite, a storage swap would also have to change `cli.py`. Fixing item 1 restores the measure.
5. **Holds**: QS-1 (read-only, no write path changed) and QS-2 (`list` untouched, stdlib only).

---

**Summary:** Standards: 2 judgement calls, worst is the missing export test. Spec: 1 finding, worst is the uncaught traceback on a missing DB (Important). Architecture: 4 findings, worst is the ADR-0003 breach where `cli.py` imports `sqlite3` (Critical).

**Notes on the run:**
- `main` does not exist as a ref in this repo, so I took `HEAD~1` (`21d0018`) as the base.
- I reviewed each axis in a separate pass, not with subagents, because you did not ask for subagents.
- I changed no repo files. The export checks ran against temp databases.

### result (success)
