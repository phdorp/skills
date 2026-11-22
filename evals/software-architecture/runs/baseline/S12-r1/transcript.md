### user

/sa:spec-and-plan Here is the approved design for a backup command. Write the spec.

`notes backup PATH` copies the note store to PATH so a user can keep a copy on another disk.
- PATH is a file path; an existing file at PATH is replaced.
- The command prints the number of notes backed up and exits 0.
- If the store cannot be read, it reports the error on stderr and exits 1, as every command does.
- No restore command yet; a user restores by copying the file back.
- The backup file is written atomically, as ADR-0004 says.

Write the spec. I'm not available: where you would ask me, state the assumption in the spec.

### assistant

I'll start by reading the repo's tracker config, glossary, ADRs, and the spec template.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200 && echo --- && cat docs/agents/issue-tracker.md 2>/dev/null; echo \"exit=$?\"",
 "description": "List repo files and check tracker config"
}
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-arm-x0l35aht/sa/skills/spec-and-plan/references/spec-template.md"
}
```

### tool_result

```
e370ee3 fixture
./README.md
./GLOSSARY.md
./notes/__main__.py
./notes/cli.py
./notes/store.py
./notes/__init__.py
./notes/model.py
./tests/test_notes.py
./tests/__init__.py
./docs/adr/0004-write-notes-atomically.md
./docs/adr/0002-record-architecture-decisions.md
./docs/adr/0005-add-postgresql-backend.md
./docs/adr/0003-cli-reaches-storage-only-through-store.md
./docs/adr/0001-use-sqlite-for-storage.md
./docs/architecture/arc42.md
---
exit=1
```

### tool_result

```
1	# Spec Template
2	
3	The body is identical for both publication forms; only the wrapper changes.
4	
5	## Local file form
6	
7	Save to `docs/specs/YYYY-MM-DD-<topic>-spec.md`. Start with a status line so a reader knows whether the spec is agreed or still moving:
8	
9	```markdown
10	# <Feature> Spec
11	
12	Status: ready-for-agent
13	Source: <path to the design doc, or the conversation that produced this>
14	```
15	
16	## Tracker issue form
17	
18	- **Title**: `<Feature>`
19	- **Labels**: `ready-for-agent` unless the user says otherwise.
20	- **Body**: the sections below.
21	- **Parent**: if the source was an existing issue, publish this spec as its sub-issue. Do not modify the parent.
22	
23	## Body
24	
25	### Problem Statement
26	
27	The problem the user is facing, from the user's perspective. What is painful today, who feels it, and what it costs them. No solution language.
28	
29	### Solution
30	
31	The solution to the problem, from the user's perspective. What changes for them when this ships.
32	
33	### User Stories
34	
35	A long, numbered list. Each one follows:
36	
37	```
38	1. As an <actor>, I want <feature>, so that <benefit>
39	```
40	
41	Cover every aspect of the feature, not just the happy path. Include:
42	
43	- first use, returning use, and empty state
44	- permissions and roles
45	- failure and recovery
46	- limits and large inputs
47	- accessibility and platform differences where they matter
48	- the cases the user explicitly cares about
49	
50	Example:
51	
52	```
53	1. As a mobile bank customer, I want to see balances on my accounts, so that I can make better-informed decisions about my spending.
54	```
55	
56	### Implementation Decisions
57	
58	The decisions already made, in enough detail that a planner does not reopen them:
59	
60	- modules to build or modify, and their responsibilities
61	- interfaces that change, in prose
62	- technical clarifications from the developer
63	- architectural decisions
64	- schema changes
65	- API contracts
66	- specific interactions and sequences
67	
68	Do not include specific file paths or code snippets; they go stale quickly.
69	
70	Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo.
71	
72	### Testing Decisions
73	
74	- What makes a good test here: external behaviour, through the agreed seams, not implementation details.
75	- Which modules will be tested, and at which seam.
76	- Prior art: similar tests already in the codebase, by path or name.
77	
78	### Out of Scope
79	
80	What this spec deliberately does not cover, and where that work goes instead if it is planned.
81	
82	### Further Notes
83	
84	Anything else the planner or builder needs: open assumptions, links to ADRs or research, rollout notes.
85	
```

### assistant

No tracker config exists, so the spec goes to a local file. Next I'll read the ADR, glossary, code, and tests.

### tool_use Bash

```json
{
 "command": "for f in docs/adr/0004-write-notes-atomically.md docs/adr/0003-cli-reaches-storage-only-through-store.md docs/adr/0001-use-sqlite-for-storage.md docs/adr/0005-add-postgresql-backend.md GLOSSARY.md README.md notes/cli.py notes/store.py notes/model.py notes/__main__.py; do echo \"=== $f\"; cat \"$f\"; done",
 "description": "Read ADRs, glossary, README, and notes source"
}
```

### tool_result

```
=== docs/adr/0004-write-notes-atomically.md
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
=== docs/adr/0003-cli-reaches-storage-only-through-store.md
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
=== docs/adr/0001-use-sqlite-for-storage.md
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
=== docs/adr/0005-add-postgresql-backend.md
# 5. Add a PostgreSQL backend

## Status

proposed

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.
=== GLOSSARY.md
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
=== README.md
# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
=== notes/cli.py
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
=== notes/store.py
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
                         "(id INTEGER PRIMARY KEY, text TEXT N
[... 974 chars cut]
```

### tool_use Bash

```json
{
 "command": "echo \"=== tests\" && cat tests/test_notes.py && echo \"=== arc42\" && cat docs/architecture/arc42.md && echo \"=== adr0002\" && cat docs/adr/0002-record-architecture-decisions.md",
 "description": "Read tests and architecture docs"
}
```

### tool_result

```
=== tests
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
=== arc42
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
=== adr0002
# 2. Record architecture decisions

## Status

acc
[... 762 chars cut]
```

### assistant

The ADR-0004 status is "proposed", not accepted, and ADR-0002 says work depending on an unaccepted decision waits. I'll note that in the spec. Before writing, I'll check the glossary rules and branch state.

### tool_use Bash

```json
{
 "command": "git branch -a && git remote -v; echo \"---\"; cat /tmp/sa-arm-x0l35aht/sa/skills/domain-modeling/SKILL.md 2>/dev/null | head -80; echo \"--- conv\"; cat /tmp/sa-arm-x0l35aht/sa/skills/conventional-commits/SKILL.md 2>/dev/null | head -40",
 "description": "Check branches, remotes, and skill guidance"
}
```

### tool_result

```
* master
---
---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
--- conv
---
name: conventional-commits
description: Use when writing or amending a git commit message, or when a repository enforces commit conventions. Triggers include "commit this", "write a commit message", "amend the commit", and "which type should this commit be".
---

# Conventional Commits

Every commit message names its type and states what changed, in a shape changelogs and release tools parse. The specification is Conventional Commits 1.0.0: <https://www.conventionalcommits.org/en/v1.0.0/>.

For the commit a squash merge lands on the default branch, also follow [squash-merge-message](../squash-merge-message/SKILL.md): it decides which parts of the message reach the changelog.

## The format

```
<type>[(<scope>)][!]: <description>

<body>

<fo
[... 1078 chars cut]
```

### assistant

I have what I need. The design is clear, but three points need to be in the spec: ADR-0004 still reads "proposed", a missing store would be silently created by today's `Store` constructor, and a `PATH` that points at the live store could destroy it. I'll write the spec and record the assumptions for each.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-zscf6ndb/project/docs/specs/2026-11-22-backup-command-spec.md",
 "content": "# Backup Command Spec\n\nStatus: ready-for-agent (blocked on ADR-0004 acceptance; see Further Notes)\nSource: the approved design in the conversation of 2026-11-22, which this spec restates.\nRelated: ADR-0002 (decisions reserved for the architect), ADR-0003 (CLI reaches storage only through `Store`), ADR-0004 (atomic writes), arc42 QG-1 / QS-1 (no note lost).\n\n### Problem Statement\n\nA user's notes live in one file on one disk. If that disk fails, is lost, or is replaced, every note is gone, and the user has no copy to fall back on. Users who want a second copy on another disk must find the store file themselves, know where `notes` keeps it, and copy it while no command is writing to it. Most do not, so their notes are only one disk failure away from loss.\n\n### Solution\n\n`notes backup PATH` writes a copy of the note store to PATH. The user points PATH at a file on another disk, runs the command, and gets a count of the notes in the copy. Running the command again replaces the earlier copy at the same PATH. A failed backup never damages the previous copy or the live store. To restore, the user copies the backup file back over the store file. No restore command exists yet.\n\n### User Stories\n\n1. As a user, I want to run `notes backup PATH` and get a copy of my notes at PATH, so that I have a second copy on another disk.\n2. As a user, I want the command to print how many notes it backed up, so that I can confirm the copy holds every note I expect.\n3. As a user with a store that has no notes yet, I want the backup to succeed and print `0`, so that a scheduled backup script does not fail on a new store.\n4. As a user who backs up to the same path each time, I want an existing file at PATH replaced, so that I do not have to delete the old copy first.\n5. As a user, I want the backup file to be either the complete new copy or the untouched old one, so that an interrupted backup never leaves a damaged file in place of my last good copy.\n6. As a user whose store cannot be read (corrupt, not a notes store, or unreadable permissions), I want an error on stderr and exit code 1, so that a script can detect the failed backup, and my previous copy at PATH is left as it was.\n7. As a user whose PATH cannot be written (directory missing, no write permission, or PATH is a directory), I want an error on stderr and exit code 1, and any existing file at PATH unchanged.\n8. As a user who runs `backup` before ever adding a note, I want an error and exit code 1 instead of a new empty store being created at the store path, so that backup never silently creates files in my home directory.\n9. As a user who accidentally gives the store's own path as PATH, I want the command to refuse with an error and exit code 1, so that my live store is not overwritten by its own copy.\n10. As a user restoring after data loss, I want to copy the backup file over my store file and find every note again, so that restore needs no command of its own.\n11. As a user who runs `backup` while another `notes` command is adding a note, I want the backup to hold a consistent snapshot, so that the copy is never a torn mix of states.\n12. As a user on a shared machine, I want the backup file readable only by me, so that other accounts cannot read my notes.\n13. As a user who omits PATH, I want the usage error that every other command gives, with exit code 2, so that the command behaves like the rest of the CLI.\n\n### Implementation Decisions\n\n- **Command**: a new subcommand `backup` with one required positional argument, `PATH`. Its help text describes it as copying the store to PATH. The CLI decides the output and exit code; the store decides the copy.\n- **Storage boundary**: the copy is made by the `store` block, not by `cli` (ADR-0003). `store` exposes one operation that takes a destination path and returns the number of notes it wrote. `cli` calls only that operation and prints the result.\n- **Snapshot**: the copy is taken through SQLite's online backup mechanism, so it is a consistent snapshot even if another process writes during the copy. A plain byte copy of the store file is not used.\n- **Atomic write**: follows ADR-0004 exactly. The snapshot is written to a temporary file in the same directory as PATH, the temporary file is flushed with `os.fsync`, and it is moved to PATH with `os.replace`. The temporary file is created in PATH's directory so the rename stays on one filesystem.\n- **Note count**: the number printed is the count of notes in the temporary file, after the snapshot is written and before the rename. The count describes exactly what was copied.\n- **Output**: on success, stdout gets the count as a bare integer and a newline, with no other text. This matches `add`, which prints the new id and nothing else. Exit code 0.\n- **Errors**: any failure prints one line to stderr in the form `notes: <message>` and exits with code 1, as every command does (arc42 section 8). On failure the temporary file is removed and PATH is not changed.\n- **Missing store**: if the store file does not exist, the command fails with exit code 1 and creates neither the store nor PATH. The check happens before the store is opened, because opening a store creates its file.\n- **Self-copy refusal**: if PATH resolves to the same file as the store, the command fails with exit code 1 before writing anything.\n- **Format**: the backup file is a SQLite database file in the same format as the store. It is not a new export format.\n- **Permissions**: the backup file has owner read and write only, the default for a temporary file created this way.\n- **Schema**: no change. The backup copies the existing `notes` table as it is.\n- **Restore**: no code. Restore is a file copy that the user performs while no `notes` command is running.\n- **Backend**: the command reads the SQLite store. It has no branch for other backends; ADR-0005 is only proposed and no other backend exists.\n\n### Testing Decisions\n\n- **Seam**: the existing CLI entry point, `main(argv)`, with the store location set through the `NOTES_DB` environment variable, as `CliTest.test_add_and_search` does. This is the highest seam that proves the behaviour: it covers argument parsing, the output, the exit code, and the store. One further test patches the rename step inside `notes/store.py` to fail, because nothing above that seam can show that an interrupted write leaves the old file in place. No new seam is introduced.\n- **Good tests** check what a user can observe: the return value, stdout, stderr, the files on disk, and whether a copied store opens and lists the same notes. They do not assert which SQLite calls were made.\n- **Tests to write** (each in `tests/test_notes.py`, in the `CliTest` class or a new `BackupTest` class beside it):\n  - Backup copies every note: two notes added, then `main([\"backup\", p])` returns 0, stdout is `2\\n`, and `Store(p).all()` returns both notes with the same ids, text, and timestamps.\n  - Empty store: `main([\"backup\", p])` returns 0 and stdout is `0\\n`.\n  - Existing file replaced: `p` holds `junk`; after a successful backup, `p` is a valid store with the notes.\n  - Repeat backup replaces the earlier copy: a second backup after one more note prints the new count.\n  - Unreadable store: `NOTES_DB` points at a file of non-SQLite bytes; the command returns 1, stderr starts with `notes: `, and `p` is not created.\n  - Missing store: `NOTES_DB` points at a path that does not exist; the command returns 1, neither that path nor `p` is created.\n  - Self-copy refused: `p` is the store path; the command returns 1 and the store is unchanged.\n  - Unwritable PATH: PATH's directory does not exist, and separately PATH is an existing directory; each returns 1 with a stderr message, and nothing is created or changed.\n  - Failed rename leaves old file: `p` holds a valid old copy; `notes.store.os.replace` is patched to raise `OSError`; the command returns 1, `p` still holds the old copy, and no temporary file remains in the directory.\n  - Restore by copy: back up, then copy `p` over the store path; a fresh `Store` lists the same notes.\n  - Missing PATH: `main([\"backup\"])` raises `SystemExit` with code 2, as argparse does for the other commands.\n- **Prior art**: `tests/test_notes.py`, `StoreTest` and `CliTest`. Use `tempfile.mkdtemp()` for paths, as they do.\n- **Not tested here**: a real SIGKILL during backup, as QS-1 does for `add`. It is a useful later check, but it is not required for this spec.\n\n### Out of Scope\n\n- A restore command. Restore is a file copy until a later spec adds one.\n- Scheduled or automatic backups, and backup rotation or retention.\n- Compression, encryption, or checksums of the backup file.\n- Listing, verifying, or reading back backups.\n- Backing up several stores in one run.\n- Sync between devices (R-4, deferred).\n- A PostgreSQL backend (ADR-0005, proposed). If it is accepted, backup for that backend is a separate spec.\n- A size limit or progress output for large stores.\n\n### Further Notes\n\n**Blocker: ADR-0004 status.** `docs/adr/0004-write-notes-atomically.md` reads `proposed`. ADR-0002 says work that depends on an unaccepted decision waits until the ADR is accepted. This spec depends on ADR-0004 for its atomic-write rule. The architect should accept ADR-0004 before implementation starts. The command name `backup`, its exit codes, and the fact that the output is a SQLite file are on ADR-0002's list of centrally decided items. They are covered by this spec, which the approved design restates. No separate ADR is written for them.\n\n**Assumptions made without asking** (the owner was not available to answer these; each is the most likely reading of the approved design and can be changed by editing this section):\n\n1. A missing store file is an error (exit 1), not an empty backup. The current `Store` opens and creates its file, so the backup must check for the store before opening it.\n2. A PATH that resolves to the store file is refused (exit 1). Without this check, `os.replace` would overwrite the live store.\n3. Any write failure after the store is read (missing directory, no permission, PATH is a directory, disk full) is an error with exit 1, and PATH is left unchanged.\n4. Output is the bare integer and a newline, not a sentence. A user who wants a sentence can wrap the command.\n5. PATH is taken as given: relative paths are relative to the working directory, and `~` is expanded by the shell.\n6. A usage error (missing PATH) exits 2 through argparse, as the other commands do today. Exit 1 is used only for store and write errors.\n7. The backup file is private (owner read and write only). This follows from the temporary-file default and is stated so it is a deliberate choice.\n8. The count comes from the file that was written, not from a second read of the store, so the printed count always matches the copy.\n\n**Glossary.** The term **Backup** is added to `GLOSSARY.md`.\n\n**Rollout.** No migration. The command is new and does not change the store format.\n\n**Open for the architect.** Whether the backup file counts as an export format under ADR-0002. This spec treats it as a copy of the store, not an export. If the architect disagrees, an ADR is needed before implementation.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-zscf6ndb/project/docs/specs/2026-11-22-backup-command-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

Next I'll add the new term to the glossary, following its existing format, then commit both files.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-zscf6ndb/project/GLOSSARY.md",
 "old_string": "**Store**: the place notes are kept between runs.",
 "new_string": "**Store**: the place notes are kept between runs.\n\n**Backup**: a copy of the store, written to a file the user names so it can be kept on another disk."
}
```

### tool_result

```
The file /tmp/sa-eval-zscf6ndb/project/GLOSSARY.md has been updated successfully.
```

### tool_use Bash

```json
{
 "command": "git add docs/specs/2026-11-22-backup-command-spec.md GLOSSARY.md && git commit -q -F - <<'EOF'\ndocs: add spec for notes backup command\n\nSpec for `notes backup PATH`: copies the store to PATH through an\natomic temporary-file write (ADR-0004), prints the note count, and\nexits 1 on store or write errors. Records assumptions made where the\ndesign left a choice open. Implementation waits for ADR-0004 to be\naccepted.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\nEOF\ngit log --oneline | head -2 && git status --short",
 "description": "Commit spec and glossary update"
}
```

### tool_result

```
8fcee00 docs: add spec for notes backup command
e370ee3 fixture
```

### assistant

The spec is written at `docs/specs/2026-11-22-backup-command-spec.md` and committed on `master` (8fcee00), along with a new **Backup** entry in `GLOSSARY.md`. I wrote only the spec. The work is one slice, so I skipped tickets and the implementation plan.

**Blocker:** ADR-0004 is still marked `proposed`. ADR-0002 says work that depends on an unaccepted decision waits, and the atomic-write rule depends on ADR-0004. The architect should accept it before implementation starts. The spec's status line says so.

**Assumptions I made where you would have been asked.** They are listed in the spec's Further Notes, and you can change any of them there:

1. **Missing store** → exit 1, and nothing is created. Today's `Store` creates its file when opened, so the check has to happen before opening.
2. **PATH equals the store path** → refused with exit 1. Without this, the rename would overwrite the live store.
3. **Any write failure** (missing directory, no permission, PATH is a directory, disk full) → exit 1, with PATH unchanged.
4. **Stdout** is the bare integer and a newline, matching how `add` prints its id.
5. **Missing PATH** → exit 2 from argparse, as the other commands already do.
6. **Backup file permissions** are owner-only, which is the temporary-file default.
7. **The count** comes from the file that was written, so it always matches the copy.

**Other notes:**
- The spec puts the copy in `store.py` and keeps the CLI calling only `Store`, as ADR-0003 requires.
- The copy uses SQLite's online backup so a concurrent `add` cannot tear it.
- Tests go through the existing `main(argv)` seam with `NOTES_DB`, following `CliTest`. One test patches the rename step to check that a failed write leaves the old file intact.
- The spec does not change any existing code. I have not run the test suite, since no code changed.
- The commit went on `master`. The repo's configured main branch is `main`, which does not exist locally.

### result (success)
