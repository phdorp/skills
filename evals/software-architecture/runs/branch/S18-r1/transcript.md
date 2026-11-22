### user

/sa:executing-plans Execute the plan in docs/plans/2026-11-22-search-and-tags.md, inline. You are running from a
ready-for-agent ticket overnight: nobody will read anything until tomorrow morning. Commit your
work on this branch and end with a final report.

### tool_use Bash

```json
{
 "command": "git status && git branch --show-current && ls docs/plans/ && cat docs/plans/2026-11-22-search-and-tags.md && ls docs/architecture 2>/dev/null",
 "description": "Check repo state and read the plan"
}
```

### tool_result

```
On branch master
nothing to commit, working tree clean
master
2026-11-22-search-and-tags.md
# Search and tags Implementation Plan

**Goal:** Search shows the newest notes first, and notes can carry tags that `list` filters on.

**Tech Stack:** Python 3.11 standard library; `unittest`.

## Global Constraints

- Run `python3 -m unittest` after every task; it passes.
- One commit per task.

### Task 1: Newest search results first

**Files:** Modify `notes/store.py`, `tests/test_notes.py`.

- [ ] **Step 1:** Test `test_search_lists_newest_first`: add "Buy milk", then "Milk the budget", search "milk", expect "Milk the budget" before "Buy milk". Run it. Expected: fails.
- [ ] **Step 2:** In `Store.search`, order by id, newest first. Expected: all tests pass. **Commit** `feat: list search results newest first`.

### Task 2: Tags

**Files:** Modify `notes/store.py`, `notes/cli.py`, `notes/model.py`, `tests/test_notes.py`.

- [ ] **Step 1:** Tests: `notes add --tag work "Call Ann"` stores the tag; `notes list --tag work` prints only notes tagged `work`; a store created before this change still opens. Expected: fail.
- [ ] **Step 2:** Add a `tags` column (comma-separated text, default empty) to the `notes` table, migrating an existing table with `ALTER TABLE`; `Note` gains `tags`; `add` takes `--tag` (repeatable); `list` takes `--tag`. Expected: all tests pass. **Commit** `feat: tag notes and filter list by tag`.
arc42.md
```

### tool_use Bash

```json
{
 "command": "find . -path ./.git -prune -o -type f -print | head -100 && cat notes/*.py && cat tests/test_notes.py && cat docs/architecture/arc42.md | head -150",
 "description": "Inspect project code, tests, and architecture doc"
}
```

### tool_result

```
./README.md
./GLOSSARY.md
./notes/__main__.py
./notes/cli.py
./notes/store.py
./notes/__init__.py
./notes/model.py
./tests/test_notes.py
./tests/__init__.py
./docs/adr/0004-store-tags-with-each-note.md
./docs/adr/0002-record-architecture-decisions.md
./docs/adr/0003-cli-reaches-storage-only-through-store.md
./docs/adr/0001-use-sqlite-for-storage.md
./docs/plans/2026-11-22-search-and-tags.md
./docs/architecture/arc42.md
"""Keep short notes from the command line."""
import sys

from notes.cli import main

sys.exit(main())
import argparse
import sys

from notes.store import Store, default_path


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes", description="Keep short notes.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("add", help="add a note").add_argument("text")
    sub.add_parser("list", help="list all notes")
    sub.add_parser("search", help="find notes containing a term").add_argument("term")
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
        else:
            found = store.all() if args.command == "list" else store.search(args.term)
            for note in found:
                print(f"{note.id}\t{note.created}\t{note.text}")
    finally:
        store.close()
    return 0
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str
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
            with redirect_stdo
[... 2843 chars cut]
```

### tool_use Bash

```json
{
 "command": "cat docs/adr/0004-store-tags-with-each-note.md docs/adr/0003-cli-reaches-storage-only-through-store.md && grep -n -i \"status\\|open\\|proposed\" docs/adr/*.md; cat README.md; echo ---; cat GLOSSARY.md; echo ---; S=/tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans; ls -R $S; cat $S/references/architecture-decisions.md $S/references/inline.md",
 "description": "Read ADRs, docs, and inline-mode reference"
}
```

### tool_result

```
# 4. Store tags with each note

## Status

proposed

## Context

Notes need tags that `list` can filter on. Tags change the on-disk format and add CLI options,
both decided centrally (ADR-0002). Serves R-1; keeps QS-3.

## Decision

Add a `tags` text column (comma-separated, default empty) to the `notes` table, migrated with
`ALTER TABLE`; `add` and `list` take `--tag`.

## Consequences

Every store migrates on first open. A tag cannot contain a comma.
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
docs/adr/0002-record-architecture-decisions.md:3:## Status
docs/adr/0003-cli-reaches-storage-only-through-store.md:3:## Status
docs/adr/0004-store-tags-with-each-note.md:3:## Status
docs/adr/0004-store-tags-with-each-note.md:5:proposed
docs/adr/0004-store-tags-with-each-note.md:19:Every store migrates on first open. A tag cannot contain a comma.
docs/adr/0001-use-sqlite-for-storage.md:3:## Status
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
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
---
/tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans:
SKILL.md
implementer-prompt.md
merger-prompt.md
re-review-prompt.md
references
scripts
task-reviewer-prompt.md

/tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans/references:
architecture-decisions.md
batching.md
cannot-verify.md
final-review.md
fix-loop.md
handling-reports.md
inline.md
preflight.md
resuming.md
subagent.md
task-graph.md

/tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans/scripts:
review-package
sdd-workspace
task-brief
task-done
task-start
# Architectural decisions during execution

Part of [executing-plans](../SKILL.md). A project with `docs/architecture/arc42.md` has an
architect, and the architecture is theirs to decide. A decision a task needs that no accepted
ADR settles is a fifth stop: it pauses only the tasks behind it.

## 1. Detect

Before each task, and whenever a step makes a choice its brief does not spell out, apply
[domain-modeling](../../domain-modeling/SKILL.md)'s "When a decision needs an ADR" test,
including the list in the ADR titled "Record architecture decisions". A choice inside one
building block is not architectural: rule on it as usual.

An architectural choice an `accepted` ADR settles → follow the ADR and proceed. Otherwise it is
an open decision. The plan and the ticket do not settle it: they are not accepted ADRs.

Done when every task you start has passed this test, or has its open decision.

## 2. Draft

Call the Skill tool with "domain-modeling" and write the decision as the next ADR in the ADR
directory, Status `proposed`, its Context citing the requirement and quality-goal IDs that
exist. Write the options the plan implies; leave the choice to the architect.

Done when the ADR file exists with five fields and Status `proposed`.

## 3. Pause and continue

Write one ledger line per task that depends on the decision:

```
Paused: Task N — waits for ADR-NNNN (<the question the architect answers>)
```

Leave its code unwritten. Then finish, test and commit every task that does not depend on it.

Done when every independent task has its completion line and every dependent task a `Paused:`
line.

## 4. Who decides

- **Architect in the conversation:** in the message that reports the ADR, ask them at once to
  accep
[... 12475 chars cut]
```

### tool_use Bash

```json
{
 "command": "cd /tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans && P=/tmp/sa-eval-lzdtbq39/project/docs/plans/2026-11-22-search-and-tags.md && bash scripts/sdd-workspace $P && cd /tmp/sa-eval-lzdtbq39/project && git log --oneline -- docs/adr/0004-store-tags-with-each-note.md && cat .gitignore 2>/dev/null; python3 -m unittest 2>&1 | tail -3; cat docs/adr/0002-record-architecture-decisions.md | sed -n 1,40p",
 "description": "Create SDD workspace and check baseline tests"
}
```

### tool_result

```
fatal: not a git repository (or any of the parent directories): .git
/tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans/.skills/sdd/2026-11-22-search-and-tags
6915e14 fixture
Ran 3 tests in 0.065s

OK
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
```

### tool_use Bash

```json
{
 "command": "rm -rf /tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans/.skills && bash /tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans/scripts/sdd-workspace docs/plans/2026-11-22-search-and-tags.md && ls -la .skills/sdd/2026-11-22-search-and-tags/ && git check-ignore -v .skills/sdd || echo \"NOT IGNORED\"; sed -n 1,60p /tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans/scripts/task-start",
 "description": "Create workspace from repo root and inspect helper"
}
```

### tool_result

```
/tmp/sa-eval-lzdtbq39/project/.skills/sdd/2026-11-22-search-and-tags
total 12
drwxr-xr-x 2 root root 4096 Nov 22 15:50 .
drwxr-xr-x 3 root root 4096 Nov 22 15:50 ..
-rw-r--r-- 1 root root   41 Nov 22 15:50 plan-path
NOT IGNORED
#!/usr/bin/env bash
# Begin one task of an inline plan execution in a single call: extract the
# task's brief (via this skill's task-brief, so both execution modes share one
# workspace) and record BASE, the commit the task's review range is cut from.
# One tool call instead of two, because every call in an inline session is a
# turn that re-reads the whole context.
#
# Usage: task-start PLAN_FILE TASK_NUMBER
# Prints:
#   brief: <path to the task's brief file>
#   base:  <full SHA of HEAD>
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "usage: task-start PLAN_FILE TASK_NUMBER" >&2
  exit 2
fi

plan=$1
n=$2
here=$(cd "$(dirname "$0")" && pwd)

out=$("${BASH:-bash}" "$here/task-brief" "$plan" "$n")
brief=$(printf '%s\n' "$out" | sed -n 's/^wrote \(.*\): [0-9][0-9]* lines$/\1/p')
[ -n "$brief" ] || { echo "task-brief did not report a path: $out" >&2; exit 1; }

echo "brief: $brief"
echo "base: $(git rev-parse HEAD)"
```

### tool_use Bash

```json
{
 "command": "echo \".skills/\" >> .git/info/exclude && W=.skills/sdd/2026-11-22-search-and-tags && printf '# SDD ledger — plan: docs/plans/2026-11-22-search-and-tags.md\\n\\n' > $W/progress.md && bash /tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans/scripts/task-start docs/plans/2026-11-22-search-and-tags.md 1 && cat $W/*.md | head -5; ls $W; cat /tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans/scripts/task-done | head -60",
 "description": "Create ledger, start Task 1, inspect task-done"
}
```

### tool_result

```
brief: /tmp/sa-eval-lzdtbq39/project/.skills/sdd/2026-11-22-search-and-tags/task-1-brief.md
base: 6915e14d4ab9c8a53fe5dbcb780fe3a0b9018167
# SDD ledger — plan: docs/plans/2026-11-22-search-and-tags.md

### Task 1: Newest search results first

**Files:** Modify `notes/store.py`, `tests/test_notes.py`.
plan-path
progress.md
task-1-brief.md
#!/usr/bin/env bash
# Close one task of an inline plan execution in a single call: run the task's
# test command, keep its full output in the workspace, print the tail, and —
# only if the command succeeded — append the completion line to the ledger.
# A failing command records nothing: the task is not complete.
#
# Usage: task-done PLAN_FILE TASK_NUMBER BASE -- TEST_COMMAND [ARGS...]
#   BASE is the SHA task-start printed; the completion line records BASE..HEAD.
# Exit: the test command's exit status.
set -euo pipefail

if [ $# -lt 5 ] || [ "$4" != "--" ]; then
  echo "usage: task-done PLAN_FILE TASK_NUMBER BASE -- TEST_COMMAND [ARGS...]" >&2
  exit 2
fi

plan=$1
n=$2
base=$3
shift 4
here=$(cd "$(dirname "$0")" && pwd)

git rev-parse --verify --quiet "$base" >/dev/null || { echo "bad BASE: $base" >&2; exit 2; }

dir=$("${BASH:-bash}" "$here/sdd-workspace" "$plan")
log="$dir/task-${n}-tests.log"
ledger="$dir/progress.md"

# Render the command the way a person would type it, for the ledger line.
cmd=""
for a in "$@"; do
  case "$a" in
    *[[:space:]\"\;\|\&]*) cmd="$cmd '$a'" ;;
    *) cmd="$cmd $a" ;;
  esac
done
cmd=${cmd# }

rc=0
"$@" > "$log" 2>&1 || rc=$?

tail -n 5 "$log"
if [ "$rc" -ne 0 ]; then
  echo "task-done: test command exited $rc; Task $n NOT recorded (full output: $log)" >&2
  exit "$rc"
fi

last=$(grep -v '^[[:space:]]*$' "$log" | tail -n 1) || last="(no output)"
[ -f "$ledger" ] || printf '# SDD ledger — plan: %s\n' "$plan" > "$ledger"
line="Task $n: complete (commits $(git rev-parse --short=7 "$base")..$(git rev-parse --short=7 HEAD), tests: $cmd → $last)"
printf '%s\n' "$line" >> "$ledger"
echo "ledger: $line"
```

### assistant

Task 1, step 1: adding the failing test first.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-lzdtbq39/project/tests/test_notes.py",
 "old_string": "        self.assertEqual([n.text for n in self.store.search(\"mil\")], [\"Buy milk\"])\n",
 "new_string": "        self.assertEqual([n.text for n in self.store.search(\"mil\")], [\"Buy milk\"])\n\n    def test_search_lists_newest_first(self):\n        self.store.add(\"Buy milk\")\n        self.store.add(\"Milk the budget\")\n        self.assertEqual([n.text for n in self.store.search(\"milk\")],\n                         [\"Milk the budget\", \"Buy milk\"])\n"
}
```

### tool_result

```
The file /tmp/sa-eval-lzdtbq39/project/tests/test_notes.py has been updated successfully.
```

### tool_use Bash

```json
{
 "command": "python3 -m unittest 2>&1 | tail -8",
 "description": "Run tests expecting the new test to fail"
}
```

### tool_result

```
- ['Buy milk', 'Milk the budget']
+ ['Milk the budget', 'Buy milk']

----------------------------------------------------------------------
Ran 4 tests in 0.129s

FAILED (failures=1)
```

### assistant

Red confirmed. Now the implementation (step 2).

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-lzdtbq39/project/notes/store.py",
 "old_string": "                                (f\"%{term}%\",))",
 "new_string": "                                (f\"%{term}%\",))  # newest first"
}
```

### tool_result

```
The file /tmp/sa-eval-lzdtbq39/project/notes/store.py has been updated successfully.
```

### assistant

That edit was wrong: it only added a comment and didn't change the ordering. Correcting it.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-lzdtbq39/project/notes/store.py",
 "old_string": "        rows = self._db.execute(\"SELECT id, text, created FROM notes WHERE text LIKE ? ORDER BY id\",\n                                (f\"%{term}%\",))  # newest first",
 "new_string": "        rows = self._db.execute(\"SELECT id, text, created FROM notes WHERE text LIKE ? ORDER BY id DESC\",\n                                (f\"%{term}%\",))"
}
```

### tool_result

```
The file /tmp/sa-eval-lzdtbq39/project/notes/store.py has been updated successfully.
```

### tool_use Bash

```json
{
 "command": "git diff notes/store.py && python3 -m unittest 2>&1 | tail -3",
 "description": "Show store diff and run full test suite"
}
```

### tool_result

```
diff --git a/notes/store.py b/notes/store.py
index eb064d3..ae86270 100644
--- a/notes/store.py
+++ b/notes/store.py
@@ -29,7 +29,7 @@ class Store:
         return [Note(*row) for row in rows]
 
     def search(self, term):
-        rows = self._db.execute("SELECT id, text, created FROM notes WHERE text LIKE ? ORDER BY id",
+        rows = self._db.execute("SELECT id, text, created FROM notes WHERE text LIKE ? ORDER BY id DESC",
                                 (f"%{term}%",))
         return [Note(*row) for row in rows]
 
Ran 4 tests in 0.090s

OK
```

### assistant

Green. Committing, then recording the task through `task-done`.

### tool_use Bash

```json
{
 "command": "git add notes/store.py tests/test_notes.py && git commit -q -m \"feat: list search results newest first\" && git log --oneline -1 && bash /tmp/sa-arm-d6ih7zsg/sa/skills/executing-plans/scripts/task-done docs/plans/2026-11-22-search-and-tags.md 1 6915e14d4ab9c8a53fe5dbcb780fe3a0b9018167 -- python3 -m unittest",
 "description": "Commit Task 1 and record completion in ledger"
}
```

### tool_result

```
8cb0d8c feat: list search results newest first
....
----------------------------------------------------------------------
Ran 4 tests in 0.090s

OK
ledger: Task 1: complete (commits 6915e14..8cb0d8c, tests: python3 -m unittest → OK)
```

### assistant

Task 1 is recorded. Task 2 stops at the architecture gate: ADR-0002 says the on-disk format and CLI options are decided centrally, and ADR-0004 (which covers exactly those) is still `proposed`. Plan text isn't an accepted ADR, so Task 2's code stays unwritten. I'll check whether a remote exists before deciding how to surface the ADR.

### tool_use Bash

```json
{
 "command": "git remote -v; echo \"remotes: $(git remote | wc -l)\"; git status --short; W=.skills/sdd/2026-11-22-search-and-tags; echo 'Paused: Task 2 — waits for ADR-0004 (accept the tags design: a comma-separated `tags` column on `notes`, migrated with ALTER TABLE, and `--tag` on `add` and `list`; ADR-0004 is still `proposed`, and ADR-0002 centrally decides the on-disk format and CLI options)' >> $W/progress.md && cat $W/progress.md",
 "description": "Check remotes and ledger the Task 2 pause"
}
```

### tool_result

```
remotes: 0
?? notes/__pycache__/
?? tests/__pycache__/
# SDD ledger — plan: docs/plans/2026-11-22-search-and-tags.md

Task 1: complete (commits 6915e14..8cb0d8c, tests: python3 -m unittest → OK)
Paused: Task 2 — waits for ADR-0004 (accept the tags design: a comma-separated `tags` column on `notes`, migrated with ALTER TABLE, and `--tag` on `add` and `list`; ADR-0004 is still `proposed`, and ADR-0002 centrally decides the on-disk format and CLI options)
```

### assistant

Task 2 is paused and recorded. Last checks: keep the tree clean of pycache, confirm the suite on the final commit, and confirm the ADR is already committed (so nothing extra to commit for it).

### tool_use Bash

```json
{
 "command": "echo \"__pycache__/\" >> .git/info/exclude && python3 -m unittest -v 2>&1 | tail -8 && git status --short && git log --oneline -3 && git log --oneline -- docs/adr/0004-store-tags-with-each-note.md | head -1 && git show --stat HEAD | tail -4 && echo \"ADR status: $(sed -n 5p docs/adr/0004-store-tags-with-each-note.md)\"",
 "description": "Final test run, status, and commit verification"
}
```

### tool_result

```
test_add_then_list (tests.test_notes.StoreTest.test_add_then_list) ... ok
test_search_lists_newest_first (tests.test_notes.StoreTest.test_search_lists_newest_first) ... ok
test_search_matches_substring (tests.test_notes.StoreTest.test_search_matches_substring) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.090s

OK
8cb0d8c feat: list search results newest first
6915e14 fixture
6915e14 fixture

 notes/store.py      | 2 +-
 tests/test_notes.py | 6 ++++++
 2 files changed, 7 insertions(+), 1 deletion(-)
ADR status: proposed
```

### tool_use Bash

```json
{
 "command": "echo 'Final review: self-review (subagent not requested for this run); diff is 2 files, one SQL ordering change plus one test, no findings' >> .skills/sdd/2026-11-22-search-and-tags/progress.md && tail -2 .skills/sdd/2026-11-22-search-and-tags/progress.md",
 "description": "Record self-review in the ledger"
}
```

### tool_result

```
Paused: Task 2 — waits for ADR-0004 (accept the tags design: a comma-separated `tags` column on `notes`, migrated with ALTER TABLE, and `--tag` on `add` and `list`; ADR-0004 is still `proposed`, and ADR-0002 centrally decides the on-disk format and CLI options)
Final review: self-review (subagent not requested for this run); diff is 2 files, one SQL ordering change plus one test, no findings
```

### assistant

Task 1 is done and committed. Task 2 is paused because it needs an architecture decision that hasn't been made yet, so the plan is only partly executed.

## Final report

**Branch:** `master`, as you asked ("commit on this branch"). There is no remote, so nothing was pushed.

**Completed**
- **Task 1: Newest search results first.** Commit `8cb0d8c feat: list search results newest first`.
  - Added `test_search_lists_newest_first` and watched it fail: `['Buy milk', 'Milk the budget']` was returned in the wrong order.
  - Changed `Store.search` to `ORDER BY id DESC`. The full suite passes (4 tests, OK).
  - The ledger line is `Task 1: complete (commits 6915e14..8cb0d8c, tests: python3 -m unittest → OK)`.

**Paused**
- **Task 2: Tags.** Not implemented. The code is unwritten.
  - ADR-0002 says the on-disk format and CLI options are decided centrally and need an accepted ADR.
  - Task 2 adds a `tags` column (an on-disk change) and `--tag` options (CLI changes). That is exactly what ADR-0004 covers, and ADR-0004 is still `proposed`.
  - The plan is not an accepted ADR, so I stopped at the gate instead of deciding it myself.
  - **To unblock:** accept or reject `docs/adr/0004-store-tags-with-each-note.md`. The ADR is already committed, so no new commit was needed for it. Accepting it unblocks Task 2 only.

**Final review:** I did a self-review of the Task 1 diff (one SQL line and one test) and found nothing. I did not spawn a fresh reviewer because you didn't ask for subagents. A fresh review is worth doing before merge.

**Rulings I made:** none. There were no plan conflicts to decide.

**Deferred minors:** none.

**Notes**
- The workspace is at `.skills/sdd/2026-11-22-search-and-tags/`. I kept it because it holds the ledger that records the Task 2 pause. It is excluded through `.git/info/exclude`, so it is not committed. Delete it once the plan is finished.
- Tomorrow: accept or reject ADR-0004, then rerun `/sa:executing-plans` on the plan to finish Task 2. The ledger lets it resume from there.
- I did not run `finishing-a-development-branch`, because the plan isn't complete and it would make integration decisions on your behalf.

### result (success)
