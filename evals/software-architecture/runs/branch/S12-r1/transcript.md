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

I'll start by reading the repo's tracker config, glossary, ADRs, and the note store code.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200 && echo --- && cat docs/agents/issue-tracker.md 2>/dev/null; echo \"--- exit $?\"",
 "description": "List repo files and check tracker config"
}
```

### tool_result

```
88d3d4e fixture
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
--- exit 1
```

### tool_use Bash

```json
{
 "command": "ls docs 2>/dev/null; find docs -type f 2>/dev/null; echo ---; cat GLOSSARY.md 2>/dev/null; echo ---; cat docs/adr/0004*.md 2>/dev/null",
 "description": "Read glossary and ADR-0004"
}
```

### tool_result

```
adr
architecture
docs/adr/0004-write-notes-atomically.md
docs/adr/0002-record-architecture-decisions.md
docs/adr/0005-add-postgresql-backend.md
docs/adr/0003-cli-reaches-storage-only-through-store.md
docs/adr/0001-use-sqlite-for-storage.md
docs/architecture/arc42.md
---
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
---
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
```

### assistant

ADR-0004 is still "proposed", and `arc42.md` exists, so the quality-requirements reference applies. Next I'll read the code, the other ADRs, and the architecture doc.

### tool_use Bash

```json
{
 "command": "cat notes/store.py; echo ----CLI; cat notes/cli.py; echo ----MODEL; cat notes/model.py; echo ----MAIN; cat notes/__main__.py notes/__init__.py; echo ----README; cat README.md",
 "description": "Read store, CLI, model, and README"
}
```

### tool_result

```
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
----CLI
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
----MODEL
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str
----MAIN
import sys

from notes.cli import main

sys.exit(main())
"""Keep short notes from the command line."""
----README
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
 "command": "cat docs/adr/0001*.md; echo ----0003; cat docs/adr/0003*.md; echo ----0005; cat docs/adr/0005*.md; echo ----0002; cat docs/adr/0002*.md",
 "description": "Read ADRs 0001, 0002, 0003, 0005"
}
```

### tool_result

```
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
----0003
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
----0005
# 5. Add a PostgreSQL backend

## Status

proposed

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.
----0002
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
 "command": "cat docs/architecture/arc42.md; echo ----TESTS; cat tests/test_notes.py",
 "description": "Read architecture doc and tests"
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
----TESTS
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
```

### assistant

The code and ADRs raise several points the spec must handle: the backup must go through `Store` (ADR-0003), its file must be a valid store file for restore, and ADR-0004 is still "proposed". Next I'll read the spec template, the quality-requirements reference, and the domain-modeling skill for the glossary step.

### tool_use Read

```json
{
 "file_path": "/tmp/sa-arm-fcm8csln/sa/skills/spec-and-plan/references/spec-template.md"
}
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

### tool_use Read

```json
{
 "file_path": "/tmp/sa-arm-fcm8csln/sa/skills/spec-and-plan/references/quality-requirements.md"
}
```

### tool_result

```
1	# Quality Requirements in a set-up project
2	
3	Part of [spec-and-plan](../SKILL.md). A set-up project has `docs/architecture/arc42.md`; the
4	spec says which of its requirements, quality scenarios and decisions the work rests on.
5	
6	## Read
7	
8	The R-list and quality goals in arc42 section 1, the quality scenarios (`QS-n`) in section 10,
9	and every ADR with its status.
10	
11	## Write the section
12	
13	Add this section to the spec after Testing Decisions. Cite by ID; arc42 and the ADRs hold the
14	text, so a scenario's measure stays there.
15	
16	```markdown
17	### Quality Requirements
18	
19	- **Serves:** <R-n, the parent requirements>
20	- **Keeps:** <QS-n, the quality scenarios the work must still meet>
21	- **Builds on:** <ADR-nnnn, the accepted ADRs it relies on>
22	- **Blocked by:** <ADR-nnnn, each proposed ADR that settles a decision the work needs>
23	```
24	
25	A proposed ADR is an open decision: list it under **Blocked by**, and say so in your final
26	message. While **Blocked by** lists an ADR, the spec's status line reads
27	`Status: blocked (ADR-nnnn)`, and a tracker issue gets the blocked marking instead of
28	`ready-for-agent`. The spec builds on the decision once the architect accepts the ADR.
29	
30	## Red flags
31	
32	| Thought | Reality |
33	|---|---|
34	| "The design relies on a proposed ADR, so the spec follows it" | A proposed ADR is open. List it under Blocked by until the architect accepts it. |
35	| "Blocked is in the notes, so the status can say ready-for-agent" | The status line is what an agent reads first. It says blocked until **Blocked by** is empty. |
36	
```

### tool_use Skill

```json
{
 "skill": "sa:domain-modeling",
 "args": "Add the term \"Backup\" to GLOSSARY.md for the notes backup command: a copy of the store written to a user-chosen file by `notes backup PATH`, restorable by copying the file back. Keep the entry short; no ADR is needed for the term itself."
}
```

### tool_result

```
Launching skill: sa:domain-modeling
```

### tool_use Bash

```json
{
 "command": "git branch -a && git config user.name; git config user.email; python3 --version",
 "description": "Check branches, git identity, Python version"
}
```

### tool_result

```
* master
Philip Dorpmüller
philip.dorpmueller@web.de
Python 3.13.5
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-zivubzwd/project/GLOSSARY.md"
}
```

### tool_result

```
1	# Glossary
2	
3	**Note**: a short piece of text a user keeps, with an id and the time it was created.
4	
5	**Store**: the place notes are kept between runs.
6	
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-zivubzwd/project/GLOSSARY.md",
 "old_string": "**Store**: the place notes are kept between runs.\n",
 "new_string": "**Store**: the place notes are kept between runs.\n\n**Backup**: a copy of the store that a user writes to a file of their choice, to keep on another disk. Restoring it means copying the file back over the store.\n"
}
```

### tool_result

```
The file /tmp/sa-eval-zivubzwd/project/GLOSSARY.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### assistant

The glossary entry is in. Now the spec. ADR-0004 is still `proposed`, so the status line reads blocked, and I'm recording the assumptions in Further Notes since you're not available to confirm them.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-zivubzwd/project/docs/specs/2026-11-22-backup-spec.md",
 "content": "# Notes Backup Spec\n\nStatus: blocked (ADR-0004)\nSource: the approved design for `notes backup`, given in conversation on 2026-11-22\n\n## Problem Statement\n\nA user's notes live in one store file on one disk. If that disk fails or is lost, every note is\ngone, and the user has no copy to restore from. Users who keep notes for years (R-2) want a\nsecond copy on another disk, but today the only way to make one is to copy the store file by\nhand, which risks copying it while a command is writing to it.\n\n## Solution\n\nA user runs `notes backup PATH`. The command writes a complete, consistent copy of the store to\nPATH, replacing any file already there, and prints how many notes it backed up. The user keeps\nthat file on another disk. To restore, the user copies the file back to the store's location.\nThere is no restore command yet.\n\n## User Stories\n\n1. As a user, I want to run `notes backup PATH`, so that I have a copy of my notes on another disk.\n2. As a user, I want the command to print the number of notes backed up, so that I can confirm the copy holds what I expect.\n3. As a user, I want the command to exit 0 when the backup succeeds, so that scripts can rely on it.\n4. As a user, I want a backup to replace an older backup at the same PATH, so that I can reuse one file name for each backup.\n5. As a user with no notes yet, I want a backup to succeed and report 0, so that an empty store is still backed up.\n6. As a user, I want a backup taken while another `notes` command is writing to the store to be a consistent copy, so that the backup never contains half of a write.\n7. As a user, I want a backup to be restorable by copying the file back over the store, so that I need no extra tool to restore.\n8. As a user, I want a failed backup to leave any existing file at PATH unchanged, so that a failed run never destroys my previous backup.\n9. As a user, I want a crash or kill during a backup to leave PATH holding either the old file or the complete new one, so that I never find a partial backup (QS-1).\n10. As a user whose store cannot be read, I want the error on stderr and exit code 1, so that I know the backup did not happen.\n11. As a user who gives a PATH whose directory does not exist, or that is not writable, or that is a directory, I want an error on stderr and exit code 1, so that I know where the problem is.\n12. As a user who gives PATH equal to the store's own file, I want the command refused with an error and exit code 1, so that the store is never overwritten by its own copy.\n13. As a user who runs `notes backup` without a PATH, I want the usual usage message, so that I learn the command needs a PATH.\n14. As a user on a locked-down Linux or macOS machine, I want the command to work with only the Python standard library, so that I install nothing new (R-3, QS-2).\n15. As a user whose backup target is on another disk, I want the backup to land there complete, so that the other disk can be unplugged afterwards.\n\n## Implementation Decisions\n\n- **Backup format.** The backup is a SQLite database file with the same schema as the store, so that copying it back over the store yields a working store. It is produced with SQLite's own backup facility, which copies a consistent snapshot even while another process writes. This is the store's existing on-disk format (ADR-0001); it is not a new format. See Further Notes, assumption A1.\n- **Where the logic lives.** The store block performs the backup: it reads the store and writes the backup file. The CLI block parses the `backup` subcommand, calls the store, prints the count, and maps errors to stderr and exit code 1. The CLI block does not touch the database directly (ADR-0003).\n- **Count.** The number printed is the number of notes in the snapshot the backup was taken from, as an integer on its own line on stdout.\n- **Atomic write.** The backup file is written to a temporary file, flushed to disk, and moved onto PATH in one step, as ADR-0004 requires for every file the store writes. The temporary file is created in the same directory as PATH, not in the store's directory, so the final move works when PATH is on another disk. ADR-0004 is `proposed`; see Quality Requirements.\n- **Store not created by backup.** Backup reads an existing store. If the store file does not exist, backup fails with an error. This differs from `list` and `add`, which create an empty store on first use. See A4.\n- **Refusals.** Backup refuses, with an error and exit code 1, when PATH is the store's own file, when PATH is a directory, and when PATH's directory is missing or not writable. In each refusal, no file at PATH is created, changed, or removed.\n- **Error reporting.** Every failure prints `notes: <message>` on stderr and exits 1, as arc42 section 8 requires. A missing `PATH` argument is a usage error and exits with the argument parser's usual code (2), as it does for every command today.\n- **Permissions.** The backup file has owner-only read and write permission. See A7.\n- **Interfaces that change.** The store gains one operation: back up to a given path, returning the note count. The CLI gains one subcommand, `backup`, taking one positional PATH. No existing command changes its output or exit codes.\n\n## Testing Decisions\n\n- **What makes a good test.** Test what a user or a restoring user can observe: the file at PATH, the printed count, the exit code, the stderr message, and whether the backup can be used as a store. Do not test which SQLite calls were made.\n- **Seams.**\n  - The highest seam is the existing CLI entry point, called with an argument list, with the store location set through the existing environment variable. It proves the command, output, exit codes, and error messages. It is the main seam.\n  - The existing store seam (a `Store` opened on a temporary file) proves the backup operation itself and the count.\n  - One failure-injection test at the store seam proves the atomic-write guarantee: a failure at the final move leaves the previous file at PATH unchanged. This test replaces the move step with a failing stand-in. It is the only test that reaches below the public behaviour, because a kill cannot be staged reliably in a unit test.\n- **Modules tested.** The store block (backup operation, refusals, atomic write) and the CLI block (subcommand, printed count, exit codes, stderr messages).\n- **Cases that must have a test:**\n  - backup then restore by copying the file back: `list` on the restored store shows all notes;\n  - the printed count equals the number of notes; exit code 0;\n  - an existing file at PATH is replaced;\n  - an empty store backs up with count 0 and exit code 0;\n  - a missing store: stderr message, exit code 1, no file created at PATH;\n  - PATH's directory missing: stderr message, exit code 1;\n  - PATH is the store's own file: refused, exit code 1, store unchanged;\n  - PATH is a directory: stderr message, exit code 1;\n  - a failure at the final move: the previous file at PATH is byte-for-byte unchanged;\n  - `backup` without PATH: exit code 2.\n- **Prior art.** `tests/test_notes.py`: `StoreTest` (temporary-file store, `add`/`all`/`search`) and `CliTest.test_add_and_search` (environment-variable store location, `main` with an argument list, captured stdout). New tests follow these patterns in the same file or a sibling file.\n- **Standard library only.** Tests use `unittest` and the standard library, as the rest of the suite does.\n\n## Quality Requirements\n\n- **Serves:** R-2 (no note is lost; a backup is the copy that survives a lost disk), R-3 (standard library only, Linux and macOS).\n- **Keeps:** QS-1 (a crash during the backup leaves PATH either as it was or as a complete backup, and the store still opens; measure: 0 unreadable files in 100 trials), QS-2 (works on a fresh machine with no install steps), QS-3 (the backup logic sits in the store block; only the store block, the CLI block, and their tests change).\n- **Builds on:** ADR-0001 (one SQLite file as the storage format), ADR-0003 (the CLI reaches storage only through the store).\n- **Blocked by:** ADR-0004 (write notes atomically via a temporary file and rename). It is `proposed`. The atomic-write rule in this spec depends on it. Implementation waits until the architect accepts ADR-0004. Per ADR-0002, work that depends on a decision on the centrally decided list waits for its ADR.\n\n## Out of Scope\n\n- A restore command. Restore is copying the file back, as the design states. A restore command, if wanted, is a separate spec.\n- Scheduled or automatic backups.\n- Compression, encryption, or a backup format other than the SQLite file.\n- Verifying a backup beyond the printed count (no checksum or integrity command).\n- Backing up the PostgreSQL backend. ADR-0005 is `proposed` and no such backend exists.\n- Incremental backups, backup rotation, or pruning old backups.\n\n## Further Notes\n\nAssumptions made because the author was not available to confirm them. Each one is for the architect to confirm or change before implementation.\n\n- **A1. Format is the store's own format, so no new ADR.** ADR-0002 lists import and export formats as centrally decided. This spec treats a backup as a copy in the existing on-disk format (ADR-0001), not a new export format, so it needs no new ADR. If the architect sees a backup as an export format, a new ADR is needed before implementation.\n- **A2. PATH equal to the store's file is refused.** The design does not say. Refusing keeps the store from being replaced by its own copy while another connection has it open.\n- **A3. Failures are reported, not retried.** PATH's directory missing, not writable, or PATH being a directory each give an error and exit 1. No directory is created for the user.\n- **A4. A missing store is an error for backup.** The design says only \"if the store cannot be read\". Backup does not create an empty store as a side effect, because that would write a store file the user did not ask for. Confirm this differs from `list`/`add` behaviour as intended.\n- **A5. Output format.** The count is printed as a bare integer on its own line on stdout. The design says \"prints the number of notes backed up\" and does not fix a wording. The count is an integer, with no prefix text, so scripts can read it directly.\n- **A6. Temporary file location.** The temporary file is in PATH's directory, so the final move stays on one disk. ADR-0004 says \"in the same directory\"; this spec reads that as the destination's directory.\n- **A7. Permissions.** The backup holds all notes, so it is owner-only (0600), the default for a temporary file. The design does not say.\n- **A8. Crash leftovers.** If the process is killed during a backup, a temporary file may remain in PATH's directory. PATH itself is never partial. Cleanup of such leftovers is not required; handled errors remove their temporary file.\n- **A9. Concurrent writers.** A backup started while another process writes to the store gives a consistent snapshot of some point in time, not necessarily the latest note. The design does not say which point.\n- **A10. The count** is the number of notes in that snapshot, so it matches what the backup file holds.\n\nOpen until the architect answers: A1 (whether a new ADR is needed) and the acceptance of ADR-0004. The rest can be changed at implementation review without reopening the design.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-zivubzwd/project/docs/specs/2026-11-22-backup-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

The spec is written. Per the spec-and-plan skill, this repo has no tracker, so the spec gets committed. I'll commit on a new branch since we're on `master`.

### tool_use Bash

```json
{
 "command": "git checkout -b spec/notes-backup && git add GLOSSARY.md docs/specs/2026-11-22-backup-spec.md && git commit -q -F - <<'EOF'\ndocs: specify notes backup command\n\nAdd the spec for `notes backup PATH` and the Backup glossary term.\nBlocked until ADR-0004 (atomic writes) is accepted.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\nEOF\ngit log --oneline | head -2 && git status --short",
 "description": "Create branch and commit spec and glossary"
}
```

### tool_result

```
Switched to a new branch 'spec/notes-backup'
49bc8a3 docs: specify notes backup command
88d3d4e fixture
```

### assistant

The spec is written and committed on a new branch, `spec/notes-backup` (commit `49bc8a3`), at `docs/specs/2026-11-22-backup-spec.md`. I also added a short **Backup** entry to `GLOSSARY.md` in the same commit.

**The spec is blocked on ADR-0004.** It is still `proposed`, and the atomic-write rule in your design depends on it. Per ADR-0002, implementation waits until the architect accepts it. I can't accept it, so the spec's status line reads `blocked (ADR-0004)`.

**Decision waiting for the architect:**
- **ADR-0004, "Write notes atomically via a temporary file and rename":** approve it as written. The backup file is one of the files it covers.

**Assumptions I made where the design was silent.** Each is listed in Further Notes for you to confirm:
- **A1 (most important):** The backup is a SQLite file in the store's existing format (ADR-0001), so no new ADR is needed. If you see a backup as a new export format, ADR-0002 requires an ADR first.
- **A2:** `notes backup` refuses a PATH that is the store's own file.
- **A4:** A missing store is an error. Backup doesn't create an empty store, unlike `list` and `add`.
- **A5:** The count prints as a bare integer on its own line on stdout.
- **A6:** The temporary file sits next to PATH, not in the store's directory, so the final move works across disks.
- **A7:** The backup file is owner-only (0600).
- **A9:** A backup taken during a concurrent write is a consistent snapshot of some point in time, not necessarily the latest note.

The rest of the spec covers the design's cases: the count, exit codes, stderr messages, replacing an existing file, and a failed backup leaving the old file unchanged. Testing goes through the existing CLI and store test seams in `tests/test_notes.py`.

I did not write code or run tests, since this was a spec-only request. No tickets or plan were written, since you asked only for the spec.

### result (success)
