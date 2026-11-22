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

I'll start by reading the repo's tracker config, glossary, ADRs, and the store code the backup touches.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200",
 "description": "List repo files and status"
}
```

### tool_result

```
fb92ab7 fixture
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
 "command": "ls docs docs/* 2>/dev/null; cat docs/agents/issue-tracker.md 2>/dev/null; echo ---; cat GLOSSARY.md 2>/dev/null; echo ---; find . -iname '*adr*' -not -path './.git/*'",
 "description": "Read tracker config, glossary, and locate ADRs"
}
```

### tool_result

```
docs:
adr
architecture

docs/adr:
0001-use-sqlite-for-storage.md
0002-record-architecture-decisions.md
0003-cli-reaches-storage-only-through-store.md
0004-write-notes-atomically.md
0005-add-postgresql-backend.md

docs/architecture:
arc42.md
---
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
---
./docs/adr
```

### assistant

No tracker config exists, so the spec goes to the local form. Next I'll read the ADRs, the store, and the CLI.

### tool_use Bash

```json
{
 "command": "cat docs/adr/0004-write-notes-atomically.md; echo ----; cat docs/adr/0003-cli-reaches-storage-only-through-store.md; echo ----; cat docs/adr/0001-use-sqlite-for-storage.md; echo ----; cat docs/adr/0005-add-postgresql-backend.md; echo ----; cat docs/adr/0002-record-architecture-decisions.md",
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
 "command": "cat notes/store.py; echo ----; cat notes/cli.py; echo ----; cat notes/model.py notes/__main__.py notes/__init__.py",
 "description": "Read store, CLI, and model source"
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
import sys

from notes.cli import main

sys.exit(main())
"""Keep short notes from the command line."""
```

### tool_use Bash

```json
{
 "command": "cat README.md; echo ----; cat docs/architecture/arc42.md; echo ----; cat tests/test_notes.py",
 "description": "Read README, arc42, and existing tests"
}
```

### tool_result

```
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
| QS-2 | QG-2 | a user runs `python3 -m notes list` | fresh Linux or macOS with Python 3.11+ | it works without installing anything | 0 install steps |
| QS-3 | QG-3 | a contributor swaps the storage engine | development | only `notes/store.py` and its tests change | 0 other files changed |

## 11. Risks and technical debt

## 12. Glossary

See [GLOSSARY.md](../../GLOSSARY.md).
----
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
                self.assertEqual(main
[... 257 chars cut]
```

### assistant

The ADRs raise two gating issues I need to handle in the spec: ADR-0004 is still `proposed`, and ADR-0002 says work depending on an unaccepted decision waits. Next I'll read the skill's templates and quality reference.

### tool_use Bash

```json
{
 "command": "cd /tmp/sa-arm-ybchhrsr/sa/skills/spec-and-plan && ls -R . && cat references/spec-template.md && echo ----- && cat references/quality-requirements.md && echo ---- && ls /tmp/sa-arm-ybchhrsr/sa/skills/domain-modeling/ && sed -n 1,200p /tmp/sa-arm-ybchhrsr/sa/skills/domain-modeling/SKILL.md",
 "description": "Read spec template and quality reference"
}
```

### tool_result

```
.:
SKILL.md
references

./references:
plan-template.md
quality-requirements.md
spec-template.md
ticket-template.md
# Spec Template

The body is identical for both publication forms; only the wrapper changes.

## Local file form

Save to `docs/specs/YYYY-MM-DD-<topic>-spec.md`. Start with a status line so a reader knows whether the spec is agreed or still moving:

```markdown
# <Feature> Spec

Status: ready-for-agent
Source: <path to the design doc, or the conversation that produced this>
```

## Tracker issue form

- **Title**: `<Feature>`
- **Labels**: `ready-for-agent` unless the user says otherwise.
- **Body**: the sections below.
- **Parent**: if the source was an existing issue, publish this spec as its sub-issue. Do not modify the parent.

## Body

### Problem Statement

The problem the user is facing, from the user's perspective. What is painful today, who feels it, and what it costs them. No solution language.

### Solution

The solution to the problem, from the user's perspective. What changes for them when this ships.

### User Stories

A long, numbered list. Each one follows:

```
1. As an <actor>, I want <feature>, so that <benefit>
```

Cover every aspect of the feature, not just the happy path. Include:

- first use, returning use, and empty state
- permissions and roles
- failure and recovery
- limits and large inputs
- accessibility and platform differences where they matter
- the cases the user explicitly cares about

Example:

```
1. As a mobile bank customer, I want to see balances on my accounts, so that I can make better-informed decisions about my spending.
```

### Implementation Decisions

The decisions already made, in enough detail that a planner does not reopen them:

- modules to build or modify, and their responsibilities
- interfaces that change, in prose
- technical clarifications from the developer
- architectural decisions
- schema changes
- API contracts
- specific interactions and sequences

Do not include specific file paths or code snippets; they go stale quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo.

### Testing Decisions

- What makes a good test here: external behaviour, through the agreed seams, not implementation details.
- Which modules will be tested, and at which seam.
- Prior art: similar tests already in the codebase, by path or name.

### Out of Scope

What this spec deliberately does not cover, and where that work goes instead if it is planned.

### Further Notes

Anything else the planner or builder needs: open assumptions, links to ADRs or research, rollout notes.
-----
# Quality Requirements in a set-up project

Part of [spec-and-plan](../SKILL.md). A set-up project has `docs/architecture/arc42.md`; the
spec says which of its requirements, quality scenarios and decisions the work rests on.

## Read

The R-list and quality goals in arc42 section 1, the quality scenarios (`QS-n`) in section 10,
and every ADR with its status.

## Write the section

Add this section to the spec after Testing Decisions. Cite by ID; arc42 and the ADRs hold the
text, so a scenario's measure stays there.

```markdown
### Quality Requirements

- **Serves:** <R-n, the parent requirements>
- **Keeps:** <QS-n, the quality scenarios the work must still meet>
- **Builds on:** <ADR-nnnn, the accepted ADRs it relies on>
- **Blocked by:** <ADR-nnnn, each proposed ADR that settles a decision the work needs>
```

A proposed ADR is an open decision: list it under **Blocked by**, mark the spec's status as
blocked on it, and say so in your final message. The spec builds on it once the architect
accepts it.

## Red flags

| Thought | Reality |
|---|---|
| "The design says ADR-0004, so the spec follows it" | A proposed ADR is open. List it under Blocked by until the archi
[... 6275 chars cut]
```

### assistant

Two findings change how I write this. ADR-0004 is still `proposed`, so the spec must list it under Blocked by and not treat it as accepted. The command name `backup` also falls under ADR-0002's centrally decided list. I'll check the glossary format before adding the new term.

### tool_use Bash

```json
{
 "command": "cat /tmp/sa-arm-ybchhrsr/sa/skills/domain-modeling/GLOSSARY-FORMAT.md; echo ----; cat /tmp/sa-arm-ybchhrsr/sa/skills/spec-and-plan/../design-dialogue/SKILL.md | head -80",
 "description": "Read glossary format and design-dialogue format"
}
```

### tool_result

```
# GLOSSARY.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

## Single vs multi-context repos

**Single context (most repos):** One `GLOSSARY.md` at the repo root.

**Multiple contexts:** A `GLOSSARY-MAP.md` at the repo root lists the contexts, where they live, and how they relate to each other:

```md
# Glossary Map

## Contexts

- `src/ordering/GLOSSARY.md` (a module-level glossary): receives and tracks customer orders
- `src/billing/GLOSSARY.md`: generates invoices and processes payments
- `src/fulfillment/GLOSSARY.md`: manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

The skill infers which structure applies:

- If `GLOSSARY-MAP.md` exists, read it to find contexts
- If only a root `GLOSSARY.md` exists, single context
- If neither exists, create a root `GLOSSARY.md` lazily when the first term is resolved

When multiple contexts exist, infer which one the current topic relates to. If unclear, ask.
----
---
name: design-dialogue
description: Use when the user wants to brainstorm a feature or product, grill a plan or decision, or settle what to build before code exists. Triggers include "brainstorm", "grill me", "help me think this through", "what should we build", and any vague request whose intent is still unsettled.
---

# Design Dialogue

You are good at building. The failure mode is building what you assume the user wants. This skill finds out what they actually want and why, then stress-tests every decision until nothing important is silently assumed.

Two movements: **elicit** intent with open questions, then **grill** the design tree in rounds. Both happen before anything is built.

## Look before you ask

Before your first message, read what the user pointed at and the code or material it touches: the project, the spec, earlier conversation, relevant files. Keep reading until you can explain how the relevant parts work today and what this change would touch.

Never ask what the repo, the spec, or the conversation already answers. Facts are your job.

If `docs/architecture/arc42.md` exists, read [references/architecture.md](references/architecture.md) before your first message.

When looking further would help, offer recon: deeper into the codebase, the user's files and data, or the web. Say what you would look for and why it changes the design. Use [research](../research/SKILL.md) for a cited investigation; dispatch a focused explorer subagent when you only need facts from this repo.

## The first message

Pick the shape that matches what they gave you.

**They already gave detail** (a spec, a plan, a handoff, a long request): keep the whole message to about 200 words. Echo t
[... 4995 chars cut]
```

### assistant

I have what I need. I'll add the new domain term to the glossary and check the branch state before committing.

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-zmldc47q/project/GLOSSARY.md"
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

### tool_use Bash

```json
{
 "command": "git branch -a && git config user.name; git config user.email; echo \"$(date +%F)\"",
 "description": "Check branches, git identity, and date"
}
```

### tool_result

```
* master
Philip Dorpmüller
philip.dorpmueller@web.de
2026-11-22
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-zmldc47q/project/GLOSSARY.md",
 "old_string": "**Store**: the place notes are kept between runs.\n",
 "new_string": "**Store**: the place notes are kept between runs.\n\n**Backup**: a copy of the store written to a file the user names, so the user can keep it on another disk.\n"
}
```

### tool_result

```
The file /tmp/sa-eval-zmldc47q/project/GLOSSARY.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### assistant

Now the spec itself, using the local-file form.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-zmldc47q/project/docs/specs/2026-11-22-backup-command-spec.md",
 "content": "# Backup Command Spec\n\nStatus: blocked. Do not implement until ADR-0004 is accepted and the `backup` command name is settled (see Quality Requirements).\nSource: approved design in the conversation of 2026-11-22 (`notes backup PATH`). The architect was not available to answer questions; every gap is stated as an assumption under Further Notes.\n\n## Problem Statement\n\nUsers keep notes for years (arc42 stakeholders) and must not lose any (R-2). The store is one SQLite file in `~/.notes.db` on the same disk as everything else. A user who wants a second copy on another disk has to know where the file is and copy it by hand. Copying a database file while the program may be writing to it can produce a copy that does not open or is missing recent notes, and the tool gives no way to check it.\n\n## Solution\n\nThe user runs `notes backup PATH`. The command writes a complete, readable copy of the store to PATH and prints how many notes it holds. If PATH already holds a file, that file is replaced. If the store cannot be read, or the copy cannot be written, the command says why on stderr and exits 1, and PATH is left as it was. To restore, the user copies the backup file back to the store's location (`NOTES_DB` or `~/.notes.db`). There is no restore command.\n\n## User Stories\n\n1. As a user, I want to run `notes backup PATH` with a path on another disk, so that I have a copy of my notes if the main disk fails.\n2. As a user, I want the command to print the number of notes in the copy, so that I can confirm it is complete.\n3. As a user, I want the command to exit 0 when the copy is written, so that a script can rely on it.\n4. As a user who backs up every week, I want a second run to replace the earlier backup at the same PATH, so that I do not have to delete it first.\n5. As a user with a new, empty store, I want the backup to succeed and print `0`, so that an empty store is not reported as an error.\n6. As a user, I want a backup I can restore by copying the file back to the store's location, so that I need no extra tool to restore.\n7. As a user, I want a failed or interrupted backup to leave the previous backup at PATH intact, so that a failure never leaves me with no usable copy.\n8. As a user whose store cannot be read (missing permission, corrupt file, or not a database), I want an error on stderr and exit 1, so that I know the backup was not made.\n9. As a user who gives a PATH in a directory that does not exist or cannot be written, I want an error on stderr and exit 1 with the store untouched, so that I can fix the path and retry.\n10. As a user who gives a directory as PATH, I want an error on stderr and exit 1, so that no directory is replaced or damaged.\n11. As a user who gives the store's own file as PATH, I want an error on stderr and exit 1, so that the live store is never overwritten by its own copy.\n12. As a user who gives a relative PATH, I want it resolved from the directory I ran the command in, so that it behaves like any other file argument.\n13. As a user with many notes, I want the backup to finish without a size limit, so that a large store can be backed up.\n14. As a user who runs `notes backup` with no PATH, I want the usage message from the argument parser and exit 2, as every command already does for usage errors.\n15. As a user backing up while another `notes` command is writing, I want the copy to contain a consistent set of notes (no half-written note), so that the backup is restorable.\n\n## Implementation Decisions\n\n- **Store owns the copy.** `Store` gains one operation that takes a destination path and returns the number of notes written. Only `notes/store.py` imports `sqlite3` (ADR-0003). The CLI calls this operation and does not touch the database.\n- **CLI gains one subcommand.** `backup` takes one required argument, PATH. It calls the store operation and prints the returned count as a bare integer followed by a newline on stdout, then exits 0. Errors go to stderr as `notes: <message>` and exit 1, as in arc42 section 8.\n- **The copy is a SQLite database.** It has the same format as the store (ADR-0001), so restoring is a file copy and needs no conversion.\n- **Consistent copy.** The copy is made with SQLite's online backup, which reads a consistent snapshot of the store, so a concurrent write cannot produce a half-copied file.\n- **Atomic write, per ADR-0004.** The copy is first written to a temporary file in the same directory as PATH, flushed with `os.fsync`, then moved onto PATH with `os.replace`. The temporary file is removed if any step fails. Any failure leaves PATH as it was.\n- **Count from the file.** The printed count is the number of rows in the notes table of the temporary copy, read before the move. The number printed is therefore the number of notes in the file at PATH.\n- **No new dependency.** Only the standard library is used (R-3). No new third-party package (arc42 section 2).\n- **No new storage engine behaviour.** The command reads the store through the existing open path, so it inherits the existing behaviour for missing or unreadable store files (see Further Notes).\n\n## Testing Decisions\n\nWhat makes a good test here: observable behaviour at the command boundary and at the store's public operation: the return value, the output, the exit code, the stderr text, and whether PATH is replaced or left unchanged. Do not assert on the temporary file name or on SQL text.\n\nSeams (no new seam is proposed; both already exist):\n\n- **`notes.cli.main(argv)`**, the command seam. Tests set `NOTES_DB` to a temporary file (as `CliTest` does) and capture stdout and stderr.\n- **`notes.store.Store`**, the storage seam. Tests open a store in a temporary directory (as `StoreTest` does).\n\nModules tested:\n\n- `notes/cli.py`: the `backup` subcommand: success output and exit 0; store unreadable gives stderr and exit 1; PATH is a directory gives exit 1; PATH is the store file gives exit 1 and the store is unchanged; missing usage argument gives exit 2.\n- `notes/store.py`: the store operation returns the number of notes; the copy opens as a `Store` and lists the same notes in the same order; an existing file at PATH is replaced; with an injected failure during the move (for example `os.replace` raising `OSError`), the previous file at PATH is byte-for-byte unchanged and no temporary file remains in the directory.\n\nPrior art: `tests/test_notes.py`, classes `StoreTest` (store behaviour through `Store`) and `CliTest` (commands through `main` with `NOTES_DB` patched via `mock.patch.dict`).\n\nNot tested automatically: that `os.fsync` reaches the disk. This is verified by reading the code.\n\n## Quality Requirements\n\n- **Serves:** R-2 (no note is lost; a copy protects against loss of the main store), R-3 (standard library only).\n- **Keeps:** QS-1 (a crash during backup leaves PATH either as it was or fully replaced, never partial, and the store still opens). QG-1 applies to the store, not only to `add`.\n- **Builds on:** ADR-0001 (SQLite file format), ADR-0003 (only `store.py` touches the database), ADR-0002 (accepted; its list of centrally decided items includes CLI command names and exit codes).\n- **Blocked by:**\n  - **ADR-0004** (`docs/adr/0004-write-notes-atomically.md`, status `proposed`). The atomic write rule in this spec is ADR-0004's rule. The spec is not built on an unaccepted ADR. The architect must accept ADR-0004.\n  - **A decision for the `backup` command name.** ADR-0002 lists CLI command names and exit codes as central decisions. No ADR records the `backup` command yet. The architect must accept a decision (an ADR, or an amendment) before implementation.\n\n## Out of Scope\n\n- A restore command. Restoring is a file copy by the user (stated requirement).\n- Scheduled or automatic backups.\n- Backup to a remote location or any sync between devices (R-4 is deferred).\n- Compression, encryption, or incremental backups.\n- Backing up the PostgreSQL backend (ADR-0005, proposed). If that backend is accepted, its backup is a separate spec.\n- Verifying the backup beyond the count printed (no integrity check command).\n\n## Further Notes\n\nAssumptions made because the architect was not available. Each is a recommendation the architect should confirm or change before implementation:\n\n1. **Output format.** stdout is the bare count and a newline (for example `3`), mirroring `add`, which prints the new note's id.\n2. **Any failure exits 1.** Both a store read error and a write error to PATH (missing directory, no permission, disk full) print `notes: <message>` on stderr and exit 1. The user named the store-read case; the write case is assumed to follow the same rule.\n3. **Missing store file.** The store opens through the same path as every command, which creates an empty store if the file does not exist. So `notes backup PATH` on a machine with no store writes a copy with zero notes, prints `0`, exits 0, and leaves an empty `~/.notes.db` behind. This is the existing side effect of opening the store, not new behaviour. Recommendation: accept it now. If the architect prefers to refuse, the command would need a check before the store is opened.\n4. **PATH equal to the store file** is refused with exit 1 and the store is left unchanged. Overwriting the live store with its own copy is never wanted.\n5. **Symlink at PATH.** The link is replaced, not the file it points to (the behaviour of `os.replace`).\n6. **Relative PATH** is resolved from the current working directory.\n7. **Argument errors** (no PATH, extra arguments) keep argparse's behaviour, which exits 2 before the store is touched.\n8. **Store with a large number of notes** is copied in one operation with no progress output.\n\nNotes for the builder:\n\n- ADR-0003 and QS-3: QS-3 says that swapping the storage engine changes only `store.py` and its tests. The new operation is part of the store's interface, so a future engine must implement it too. This is expected, not a conflict.\n- Restore is a file copy while no `notes` command is running. The spec does not require the command to refuse while the store is open. If that matters, it is a new requirement.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-zmldc47q/project/docs/specs/2026-11-22-backup-command-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

The spec is written. I'll commit it with the glossary change, as the skill's local-file publish step asks.

### tool_use Bash

```json
{
 "command": "git add docs/specs/2026-11-22-backup-command-spec.md GLOSSARY.md && git commit -q -m \"docs: specify notes backup command\n\nBlocked on ADR-0004 (proposed) and a decision for the backup command name.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2 && git status --short",
 "description": "Commit spec and glossary update"
}
```

### tool_result

```
1db0e2c docs: specify notes backup command
fb92ab7 fixture
```

### assistant

The spec is written and committed as `1db0e2c` on `master`, but implementation is blocked. ADR-0004 is still `proposed`, and ADR-0002 says work that depends on an unaccepted decision waits. The spec's own rule is that the atomic-write requirement comes from ADR-0004, so the architect needs to accept it first. The `backup` command name also falls under ADR-0002's centrally decided list, and no ADR records it yet. I did not accept ADR-0004 or draft a new ADR, since accepting ADRs is the architect's call.

**Files**
- `docs/specs/2026-11-22-backup-command-spec.md`: the spec, with the template's sections and a Quality Requirements block that lists the two blockers.
- `GLOSSARY.md`: added the term **Backup**.

The repo has no tracker configuration, so I used the local-file form. I did not produce tickets or a plan, since you asked only for the spec.

**Assumptions I made where you were unavailable** (listed in the spec's Further Notes for you to confirm):
1. stdout is the bare count and a newline, like `add` printing an id.
2. Any failure, reading the store or writing PATH, prints `notes: <message>` on stderr and exits 1.
3. A missing store file is created empty by the existing open path, so `backup` writes a 0-note copy and exits 0. This is the existing side effect, and you may want to change it.
4. PATH equal to the store file is refused with exit 1.
5. A symlink at PATH is replaced, not followed.
6. Usage errors keep argparse's exit 2.

The spec adds no new test seams. It uses the existing `notes.cli.main` and `Store` seams.

### result (success)
