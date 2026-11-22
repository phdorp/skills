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

I'll start by reading the repo: the docs the skill points to, the ADR the spec cites, and the code the backup command touches.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200",
 "description": "Show repo status, history, and file list"
}
```

### tool_result

```
abf3a9d fixture
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
```

### tool_use Bash

```json
{
 "command": "ls -la docs 2>/dev/null; ls docs/adr docs/agents docs/architecture 2>/dev/null; cat docs/agents/issue-tracker.md 2>/dev/null; cat GLOSSARY.md 2>/dev/null | head -100",
 "description": "Check docs, ADRs, tracker config, glossary"
}
```

### tool_result

```
total 16
drwxr-xr-x 4 root root 4096 Nov 21 11:55 .
drwxr-xr-x 6 root root 4096 Nov 22 09:26 ..
drwxr-xr-x 2 root root 4096 Nov 21 11:55 adr
drwxr-xr-x 2 root root 4096 Nov 21 11:55 architecture
docs/adr:
0001-use-sqlite-for-storage.md
0002-record-architecture-decisions.md
0003-cli-reaches-storage-only-through-store.md
0004-write-notes-atomically.md
0005-add-postgresql-backend.md

docs/architecture:
arc42.md
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
```

### assistant

No tracker config exists, so the spec goes to `docs/specs/` per the skill. Next I'll read the ADR the user cited, the related ADRs, the architecture doc, and the code.

### tool_use Bash

```json
{
 "command": "cat docs/adr/0004-write-notes-atomically.md; echo ----; cat docs/adr/0001-use-sqlite-for-storage.md; echo ----; cat docs/adr/0003-cli-reaches-storage-only-through-store.md; echo ----; cat docs/adr/0005-add-postgresql-backend.md; echo ----; cat docs/adr/0002-record-architecture-decisions.md",
 "description": "Read all ADRs"
}
```

### tool_result

```
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
----
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
----
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
----
# 5. Add a PostgreSQL backend

## Status

proposed

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.
----
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
 "command": "cat notes/store.py; echo ----; cat notes/cli.py; echo ----; cat notes/model.py; echo ----; cat notes/__main__.py notes/__init__.py",
 "description": "Read store, cli, model source"
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
----
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
----
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str
----
import sys

from notes.cli import main

sys.exit(main())
"""Keep short notes from the command line."""
```

### tool_use Bash

```json
{
 "command": "cat tests/test_notes.py; echo ----; cat README.md; echo ----; cat docs/architecture/arc42.md",
 "description": "Read tests, README, architecture doc"
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
----
# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
----
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
| QS-2 | QG-2 | a user runs `python3 -m notes list` | fresh Linux or macOS with Python 3.11+ | it works without installing 
[... 257 chars cut]
```

### assistant

Several things I need to account for before writing:

- ADR-0004 is still `proposed`, not accepted. ADR-0002 says work depending on an unaccepted decision waits.
- `Store` is the only place that may touch SQLite (ADR-0003), so the backup logic belongs there.
- `main()` only catches errors from opening the store, not from reads. That matters for the "exit 1" requirement.

Next I'll read the spec template and the quality-requirements reference the skill mandates, and load the domain-modeling skill for the new term "backup".

### tool_use Read

```json
{
 "file_path": "/tmp/sa-arm-bs8ow5f0/sa/skills/spec-and-plan/references/spec-template.md"
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
 "file_path": "/tmp/sa-arm-bs8ow5f0/sa/skills/spec-and-plan/references/quality-requirements.md"
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
 "args": "Update GLOSSARY.md with the new term \"backup\" (the copy of the store written by `notes backup PATH`). Context: spec for the backup command; the store is a SQLite file per ADR-0001. ADR-0004 is proposed, not accepted."
}
```

### tool_result

```
Launching skill: sa:domain-modeling
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-arm-bs8ow5f0/sa/skills/domain-modeling/GLOSSARY-FORMAT.md"
}
```

### tool_result

```
1	# GLOSSARY.md Format
2	
3	## Structure
4	
5	```md
6	# {Context Name}
7	
8	{One or two sentence description of what this context is and why it exists.}
9	
10	## Language
11	
12	**Order**:
13	{A one or two sentence description of the term}
14	_Avoid_: Purchase, transaction
15	
16	**Invoice**:
17	A request for payment sent to a customer after delivery.
18	_Avoid_: Bill, payment request
19	
20	**Customer**:
21	A person or organization that places orders.
22	_Avoid_: Client, buyer, account
23	```
24	
25	## Rules
26	
27	- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
28	- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
29	- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
30	- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.
31	
32	## Single vs multi-context repos
33	
34	**Single context (most repos):** One `GLOSSARY.md` at the repo root.
35	
36	**Multiple contexts:** A `GLOSSARY-MAP.md` at the repo root lists the contexts, where they live, and how they relate to each other:
37	
38	```md
39	# Glossary Map
40	
41	## Contexts
42	
43	- `src/ordering/GLOSSARY.md` (a module-level glossary): receives and tracks customer orders
44	- `src/billing/GLOSSARY.md`: generates invoices and processes payments
45	- `src/fulfillment/GLOSSARY.md`: manages warehouse picking and shipping
46	
47	## Relationships
48	
49	- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
50	- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
51	- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
52	```
53	
54	The skill infers which structure applies:
55	
56	- If `GLOSSARY-MAP.md` exists, read it to find contexts
57	- If only a root `GLOSSARY.md` exists, single context
58	- If neither exists, create a root `GLOSSARY.md` lazily when the first term is resolved
59	
60	When multiple contexts exist, infer which one the current topic relates to. If unclear, ask.
61	
```

### assistant

The glossary has two entries in a flat list, so I'll add "Backup" in the same style. The entry defines what a backup is and nothing about how it is implemented.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-8gb0m30q/project/GLOSSARY.md",
 "old_string": "**Store**: the place notes are kept between runs.",
 "new_string": "**Store**: the place notes are kept between runs.\n\n**Backup**: a copy of the store, written to a file a user chooses so they can keep it on another disk.\n_Avoid_: export, dump"
}
```

### tool_result

```
The file /tmp/sa-eval-8gb0m30q/project/GLOSSARY.md has been updated successfully.
```

### assistant

Glossary updated. Now I'll write the spec to `docs/specs/2026-11-22-backup-command-spec.md`. The skill's template covers the structure. Since you're unavailable, I'm recording each question I'd otherwise ask as a stated assumption.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-8gb0m30q/project/docs/specs/2026-11-22-backup-command-spec.md",
 "content": "# Backup Command Spec\n\nStatus: blocked (ADR-0004)\nSource: the approved design for `notes backup PATH`, as given in the conversation of 2026-11-22.\n\n## Problem Statement\n\nUsers keep notes for years (arc42 section 2 stakeholders). All of a user's notes live in one\nSQLite file whose location depends on `NOTES_DB` or `~/.notes.db`. The program offers no command\nthat writes a copy of that file to a path the user chooses, so a user who wants a copy on another\ndisk must find the file and copy it by hand. Nothing tells them whether the copy holds all their\nnotes.\n\n## Solution\n\nA user runs `notes backup PATH`. The command writes a complete copy of the store to PATH, replacing\nany file already there, prints the number of notes in the copy, and exits 0. To restore, the user\ncopies the file back to where the store lives. No restore command is added in this change.\n\n## User Stories\n\n1. As a user, I want to run `notes backup PATH` with a path on another disk, so that I keep a copy of my notes outside my main disk.\n2. As a user, I want the command to print the number of notes it backed up, so that I can check the copy is complete.\n3. As a user, I want an existing file at PATH replaced, so that I can repeat the backup to the same place without deleting the old copy first.\n4. As a user on first use with no notes yet, I want the backup to succeed and print `0`, so that I can back up from day one.\n5. As a user, I want a failed or interrupted backup never to leave a partial file at PATH, so that a copy I find there is always a whole store.\n6. As a user whose store cannot be read, I want the reason on stderr and exit code 1, so that I can see why the backup failed and scripts can detect it.\n7. As a user whose store cannot be read, I want the file already at PATH left untouched, so that my previous backup survives a failed attempt.\n8. As a user whose PATH cannot be written (missing directory, no permission, full disk), I want the reason on stderr, exit code 1, and no new or changed file at PATH, so that I know no backup was made.\n9. As a user who gives PATH as the store file itself, I want the command refused with an error and exit code 1, so that my live store is never overwritten.\n10. As a user restoring, I want to copy the backup file back to the store's location and have `notes list` show my notes, so that restore needs no command.\n11. As a user who omits PATH, I want a usage message and nothing written, so that a mistyped command does not create a file.\n12. As a user who gives a relative PATH, I want it resolved from the directory I run the command in, as all paths are on the command line.\n13. As a user on Linux or macOS with only Python's standard library installed, I want backup to need nothing else, so that it works on locked-down machines (R-3).\n14. As a user with a large store, I want the backup to copy every note, with no size limit imposed by the command.\n15. As a contributor, I want the backup logic to live in the store module, so that the CLI never touches the database (ADR-0003).\n\n## Implementation Decisions\n\n- **Command**: `backup` takes one positional argument, PATH. It is added to the command set in `notes/cli.py` beside `add`, `list` and `search`. The CLI calls the store; it does not import `sqlite3`.\n- **Store**: the store module gains one operation, taking the destination path and returning the number of notes written. It is the only code that reads the database file or writes the backup (ADR-0003).\n- **Copy**: the backup is a copy of the whole database file in SQLite's own format (ADR-0001), so restoring is a file copy and the restored file opens with the same store. The copy is taken in a single step from one read of the store, so it is a consistent snapshot even if another process writes during the copy.\n- **Atomic write**: the copy is first written to a temporary file in the same directory as PATH, flushed with `os.fsync`, then moved to PATH with `os.replace`, as ADR-0004 requires. Because the temporary file sits beside PATH, the move stays on one filesystem, so it works when PATH is on another disk. On any failure the temporary file is removed and PATH is left as it was.\n- **Count**: the printed number is the count of notes in the copy as written, not a separate read of the live store. After a successful run, the number printed equals the number of notes in the file at PATH.\n- **Output**: on success, stdout receives the count as a decimal number and a newline, and nothing else. Exit code 0.\n- **Errors**: any failure to read the store or write PATH prints `notes: <message>` on stderr and exits 1, as arc42 section 8 requires. The check must cover the read as well as the open: today `main()` wraps only the open in that handler, so a read error in `list` or `search` is not reported this way (see Further Notes).\n- **Permissions of the copy**: the file at PATH has the permissions of the temporary file it came from, which the standard library creates owner-readable and owner-writable only (assumption A4).\n- **Dependencies**: standard library only (R-3, QG-2). No new third-party package.\n\n## Testing Decisions\n\n- **What makes a good test**: external behaviour through the command line: exit code, stdout, stderr, and the files on disk. A test should not assert how the copy is made.\n- **Seam**: the existing `main(argv)` entry point in `notes/cli.py`, with `NOTES_DB` pointing the store at a temporary file. No new seam is proposed; one seam covers every behaviour in this spec.\n- **Modules tested**: `notes/cli.py` (command wiring, output, exit codes) and `notes/store.py` through the CLI.\n- **Behaviours to test**:\n  - success: count printed, exit 0, and a store opened from the copy lists the same notes;\n  - empty store: prints `0`, exit 0;\n  - an existing file at PATH is replaced;\n  - unreadable store (`NOTES_DB` pointing at a file that is not a database): stderr starts with `notes: `, exit 1, and the existing file at PATH keeps its exact bytes;\n  - unwritable PATH (parent directory missing): stderr message, exit 1, no file created at PATH, and no temporary file left in the directory;\n  - PATH equal to the store file: exit 1, store unchanged;\n  - missing PATH: usage message, exit 2, no file written.\n- **Failure cases without mocks**: use real bad inputs (a non-database file, a missing directory) rather than patching `os.replace` or `os.fsync`, so tests exercise the real code path.\n- **Prior art**: `tests/test_notes.py`, `CliTest.test_add_and_search` (sets `NOTES_DB` with `mock.patch.dict`, calls `main`, captures stdout with `redirect_stdout`) and `StoreTest` (uses `tempfile.mkdtemp`).\n\n### Quality Requirements\n\n- **Serves:** R-2 (no note is lost; a backup is a second copy that survives loss of the main disk)\n- **Keeps:** QS-1 (a crash or kill during backup leaves PATH either as it was or holding a complete copy, and the store still opens); QS-2 (works with no install steps on Linux or macOS); QS-3 (the backup logic stays in `notes/store.py` and its tests; `cli.py` changes only to wire the command)\n- **Builds on:** ADR-0001 (SQLite file format, standard library), ADR-0002 (decision records), ADR-0003 (the CLI reaches storage only through the store)\n- **Blocked by:** ADR-0004 (proposed): it sets the atomic-write rule this command relies on. Implementation waits until the architect accepts it.\n\n## Out of Scope\n\n- A restore command. Restoring is a file copy, as the design states.\n- Scheduled or automatic backups.\n- Encryption or compression of the backup file.\n- Verifying a backup against a checksum after writing it.\n- Backing up the PostgreSQL backend in ADR-0005, which is proposed and not built.\n- Sync between devices (R-4, deferred).\n- Fixing how `list` and `search` report read errors. That is separate work; see Further Notes.\n\n## Further Notes\n\n**Status and blocking**\n\n- Status is `blocked (ADR-0004)`. ADR-0004 is `proposed`. Per ADR-0002, work that depends on an unaccepted decision waits. The architect should accept ADR-0004; the status then changes to `ready-for-agent`.\n- The command name `backup`, its exit codes, and the backup file format sit on the central decision list in ADR-0002 (\"CLI command names and exit codes\", \"import and export formats\"). No ADR records them. The format is covered by ADR-0001, since the copy is the same SQLite file. The command name and exit codes need the architect's approval. The approved design may already cover them; if so, the architect should say so. I have not drafted a new ADR.\n\n**Assumptions**\n\nThese are the questions I would otherwise have asked. The architect may change any of them.\n\n- **A1 (empty or missing store):** the store is opened as every command opens it, so a missing store file is created empty, as `add` and `list` already do. Backup then writes a copy with 0 notes and exits 0.\n- **A2 (PATH is the store file):** refused with `notes: ...` on stderr and exit 1, with the store unchanged. The design did not cover this; overwriting the live store would be silent data loss.\n- **A3 (unwritable PATH):** a missing directory, a permission failure, or a full disk produces `notes: ...` on stderr, exit 1, and no change at PATH.\n- **A4 (permissions):** the copy keeps the owner-only permissions of the temporary file. No group or world access is added.\n- **A5 (output):** stdout is the bare count and a newline, matching how `add` prints a bare id.\n- **A6 (usage errors):** a missing PATH is a usage error, handled by the argument parser, so the exit code is 2 as for other usage errors. The exit-1 rule covers store and write failures only.\n- **A7 (relative PATH):** resolved from the current working directory.\n- **A8 (replacement):** an existing file at PATH is replaced without a prompt, as the design states.\n\n**Pre-existing gap**\n\n- `main()` wraps only `Store(...)` construction in its error handler. A read error in `list` or `search` escapes as a traceback. The process still exits 1, but without the `notes: ...` message. Backup must follow the rule itself. Changing `list` and `search` is separate work and is not part of this spec.\n\n**Glossary**\n\n- `GLOSSARY.md` gained the term **Backup** in this change.\n\n**Open for the architect**\n\n- Accept ADR-0004 (unblocks this spec).\n- Confirm the command name and exit codes, or record them in an ADR.\n- Confirm or change assumptions A1 to A8.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-8gb0m30q/project/docs/specs/2026-11-22-backup-command-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

The spec is written. The skill's publish step for a repo without a tracker is to commit the spec, so I'll commit it along with the glossary change.

### tool_use Bash

```json
{
 "command": "git add docs/specs/2026-11-22-backup-command-spec.md GLOSSARY.md && git commit -q -m \"docs: add backup command spec and glossary term\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2 && git status --short",
 "description": "Commit spec and glossary update"
}
```

### tool_result

```
595bb67 docs: add backup command spec and glossary term
abf3a9d fixture
```

### assistant

I wrote the backup spec at `docs/specs/2026-11-22-backup-command-spec.md` and committed it with a `Backup` glossary entry (commit `595bb67`). The spec is marked **blocked (ADR-0004)**: ADR-0004 is still `proposed`, and the atomic-write rule depends on it. I did not change the ADR. Its status is the architect's to set.

**Needs your decision**
- **Accept ADR-0004.** That unblocks the spec and makes it ready for implementation.
- **Confirm the command name and exit codes.** ADR-0002 puts "CLI command names and exit codes" on the central list, and no ADR records `backup`. Your approved design may already cover this. I have not drafted a new ADR.

**Assumptions I made, since you were unavailable.** Each is listed in the spec's Further Notes and can be changed:
- **A1:** A missing store is created empty, as other commands already do, and backup writes a 0-note copy.
- **A2:** If PATH is the store file itself, the command refuses with exit 1 and leaves the store alone.
- **A3:** An unwritable PATH gives a `notes:` message on stderr and exit 1, and no file is created or changed there.
- **A4:** The copy keeps owner-only permissions (the temp file's default).
- **A5:** Stdout is the bare count and a newline, matching how `add` prints an id.
- **A6:** A missing PATH is a usage error, exit 2, as argparse gives for other usage errors.
- **A7:** A relative PATH resolves from the current directory.
- **A8:** An existing file at PATH is replaced without a prompt.

**Pre-existing gap I found:** `main()` catches errors only when opening the store. A read error in `list` or `search` escapes as a traceback instead of the `notes: ...` message the spec requires. The process still exits 1. Backup has to handle its own read errors; fixing `list` and `search` is separate work and is not in the spec.

I added `Backup` to `GLOSSARY.md` with `export` and `dump` listed under *Avoid*. The commit message includes the Co-Authored-By line from the attribution reminder.

### result (success)
