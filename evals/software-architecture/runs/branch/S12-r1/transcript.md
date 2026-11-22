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

I'll start by reading the repo: its layout, the docs the skill says to check, and ADR-0004, which the spec depends on.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -20 && find . -path ./.git -prune -o -type f -print | head -200",
 "description": "Show git state and list project files"
}
```

### tool_result

```
e484b0c fixture
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
 "command": "ls -la docs 2>/dev/null; ls -la docs/agents docs/adr docs/architecture 2>/dev/null; cat docs/agents/issue-tracker.md 2>/dev/null; cat GLOSSARY.md 2>/dev/null; cat CONTEXT.md 2>/dev/null; echo ---; cat docs/adr/0004* 2>/dev/null",
 "description": "Read tracker config, glossary, and ADR-0004"
}
```

### tool_result

```
total 16
drwxr-xr-x 4 root root 4096 Nov 21 11:55 .
drwxr-xr-x 6 root root 4096 Nov 22 09:18 ..
drwxr-xr-x 2 root root 4096 Nov 21 11:55 adr
drwxr-xr-x 2 root root 4096 Nov 21 11:55 architecture
docs/adr:
total 28
drwxr-xr-x 2 root root 4096 Nov 21 11:55 .
drwxr-xr-x 4 root root 4096 Nov 21 11:55 ..
-rw-r--r-- 1 root root  478 Nov 21 11:55 0001-use-sqlite-for-storage.md
-rw-r--r-- 1 root root  817 Nov 21 11:55 0002-record-architecture-decisions.md
-rw-r--r-- 1 root root  419 Nov 21 11:55 0003-cli-reaches-storage-only-through-store.md
-rw-r--r-- 1 root root  552 Nov 21 11:55 0004-write-notes-atomically.md
-rw-r--r-- 1 root root  291 Nov 21 11:55 0005-add-postgresql-backend.md

docs/architecture:
total 12
drwxr-xr-x 2 root root 4096 Nov 21 11:55 .
drwxr-xr-x 4 root root 4096 Nov 21 11:55 ..
-rw-r--r-- 1 root root 2674 Nov 21 11:55 arc42.md
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

ADR-0004 is still `proposed`, and the skill says a proposed ADR blocks the spec until it's accepted. I'll read the architecture doc, the other ADRs, and the code before deciding how to handle that.

### tool_use Bash

```json
{
 "command": "cat docs/architecture/arc42.md; echo ---ADRs; for f in docs/adr/0001* docs/adr/0002* docs/adr/0003* docs/adr/0005*; do echo \"== $f\"; cat \"$f\"; echo; done",
 "description": "Read arc42 doc and the other ADRs"
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
---ADRs
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

Work that 
[... 880 chars cut]
```

### tool_use Bash

```json
{
 "command": "for f in notes/*.py; do echo \"== $f\"; cat \"$f\"; echo; done; echo \"== README\"; cat README.md",
 "description": "Read the notes package source and README"
}
```

### tool_result

```
== notes/__init__.py
"""Keep short notes from the command line."""

== notes/__main__.py
import sys

from notes.cli import main

sys.exit(main())

== notes/cli.py
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

== notes/model.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str

== notes/store.py
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

== README
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
 "command": "cat tests/test_notes.py; ls /tmp/sa-arm-gfgpasyg/sa/skills/spec-and-plan/references/ 2>/dev/null && cat /tmp/sa-arm-gfgpasyg/sa/skills/spec-and-plan/references/spec-template.md",
 "description": "Read tests and the spec template"
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
plan-template.md
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

### Quality Requirements (set-up projects only)

Only when `docs/architecture/arc42.md` exists. Cite by ID; arc42 and the ADRs hold the text.

- **Serves:** the parent requirements (`R-n`).
- **Keeps:** the quality scenarios (`QS-n`) the work mus
[... 464 chars cut]
```

### assistant

The repo has no tracker config, so the spec goes to a local file. Before writing I need two things. ADR-0002 says CLI command names are decided centrally, so `backup` needs an ADR or the architect's acceptance. Also, the spec adds a new term, "backup", and glossary edits go through domain-modeling. I'll load both skills.

### tool_use Skill

```json
{
 "skill": "sa:domain-modeling",
 "args": "Add the new term \"backup\" to GLOSSARY.md for the `notes backup PATH` command. Context: the user approved a design where `notes backup PATH` copies the store to PATH; a backup is restored by copying the file back. No other glossary changes."
}
```

### tool_result

```
Launching skill: sa:domain-modeling
```

### tool_use Skill

```json
{
 "skill": "sa:conventional-commits"
}
```

### tool_result

```
Launching skill: sa:conventional-commits
```

### assistant

Both skills loaded. The glossary already uses the `**Term**: definition` form, so I'll add "backup" in that style. I need to read the file with the Read tool before editing it.

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-gfng5laj/project/GLOSSARY.md"
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
 "file_path": "/tmp/sa-eval-gfng5laj/project/GLOSSARY.md",
 "old_string": "**Store**: the place notes are kept between runs.\n",
 "new_string": "**Store**: the place notes are kept between runs.\n\n**Backup**: a copy of the store, made by `notes backup PATH`, that a user keeps on another disk. A backup is restored by copying it back over the store.\n"
}
```

### tool_result

```
The file /tmp/sa-eval-gfng5laj/project/GLOSSARY.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### assistant

The glossary entry is in. Next I'll create the specs directory and write the spec. The user is unavailable, so every open question goes into the spec as a numbered assumption, and the ADR-0004 dependency is marked blocking.

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/sa-eval-gfng5laj/project/docs/specs && ls /tmp/sa-eval-gfng5laj/project/docs",
 "description": "Create the specs directory"
}
```

### tool_result

```
adr
architecture
specs
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-gfng5laj/project/docs/specs/2026-11-22-backup-command-spec.md",
 "content": "# notes backup Spec\n\nStatus: draft, blocked until ADR-0004 is accepted and the `backup` command name has an accepted decision (see Quality Requirements)\nSource: the approved design for a backup command, as given in the conversation of 2026-11-22\n\n## Problem Statement\n\nA user's notes live in one file on one disk: the store. If that disk fails, or the file is deleted, every note is lost (R-2). Today the only way to keep a copy elsewhere is to copy the file by hand. That means knowing where the store is, and a hand copy taken while the program is writing can be incomplete. Nothing tells the user whether the copy holds all their notes.\n\n## Solution\n\nA new command, `notes backup PATH`, writes a complete copy of the store to PATH. An existing file at PATH is replaced. On success the command prints the number of notes in the copy and exits 0. On failure it prints the reason on stderr, exits 1, and leaves whatever was at PATH unchanged. The user keeps the copy on another disk. To restore, the user copies the backup file back over the store. There is no restore command yet.\n\n## User Stories\n\n1. As a user, I want to run `notes backup PATH` with a path on another disk, so that a copy of my notes survives a failure of this disk.\n2. As a user, I want the command to print how many notes it backed up, so that I can check the copy has the notes I expect.\n3. As a user, I want the command to exit 0 on success, so that a script can rely on it.\n4. As a user, I want an existing file at PATH replaced without a prompt, so that I can repeat the backup to the same location.\n5. As a user, I want the copy to contain every note committed before the command started, so that it is complete and not a half-written snapshot.\n6. As a user, I want the backup file to open as a store by itself (for example by setting `NOTES_DB` to it), so that I can check it with the existing commands.\n7. As a user, I want a backup of an empty store to succeed and print 0, so that an empty store is not an error.\n8. As a user, I want a backup to be either fully written or not written at all. If the command is killed or the disk fills while it runs, the file already at PATH is still the previous file, so a failed backup never destroys an earlier good one.\n9. As a user, I want a failed backup to leave no temporary file in PATH's directory, so that the directory stays clean.\n10. As a user, I want an unreadable store reported on stderr as `notes: <message>` with exit 1, like every other command's errors.\n11. As a user, I want a PATH that is a directory, or whose parent directory does not exist, reported on stderr with exit 1, so that I learn the path is wrong.\n12. As a user, I want PATH refused when it is the store file itself, so that a backup cannot overwrite the live store.\n13. As a user, I want to restore by a plain file copy, so that recovery needs no extra command.\n14. As a user, I want `notes backup` to work on Linux and macOS with only the standard library, so that nothing new is installed (R-3).\n15. As a contributor, I want the backup logic in the store module, so that swapping the storage engine changes only the store module and its tests (QS-3).\n\n## Implementation Decisions\n\n- The `cli` block gains one command, `backup`, with one required argument, PATH. It parses the argument, asks the store block for the copy, prints the count, and reports errors on stderr with exit 1 as every command does. It does not use the storage library directly (ADR-0003).\n- The `store` block gains the operation that writes the backup, and returns the number of notes in the copy it wrote. It is the only block that knows the storage.\n- Snapshot: the copy holds exactly the notes committed before the operation starts. A writer active during the copy must not produce a torn file. The mechanism is left to the plan. The storage library's online backup facility meets this with the standard library; a raw byte copy of a live file does not.\n- Format: the backup is the store's own file format (ADR-0001). No new format is introduced, so no export-format decision is needed.\n- Atomic write (ADR-0004, proposed): the copy is written to a temporary file in PATH's directory, flushed to disk, then moved over PATH with an atomic replace. Any failure removes the temporary file and leaves PATH as it was.\n- Opening the store follows existing behaviour, the same as every other command.\n- Output: on success, one line on stdout containing only the integer count (assumption A2).\n- Errors: `notes: <message>` on stderr, exit 1.\n- No new third-party dependency (R-3).\n\n## Testing Decisions\n\n- Seam: the command entry point, called in-process, with the store path set through the existing environment variable and stdout captured. This is one seam (assumption A1, not confirmed with the user). The atomic-write failure is injected at the replace step, reached through the same entry point.\n- Good tests check external behaviour: exit code, stdout, stderr, and the contents of files on disk. A backup is verified by opening it as a store and listing its notes, not by inspecting internals.\n- Modules: the command entry point and, through it, the store block. No tests of SQLite internals.\n- Behaviours to pin:\n  - (a) success: notes copied, count printed, exit 0;\n  - (b) an existing file at PATH is replaced;\n  - (c) an empty store prints 0;\n  - (d) unreadable store: `notes: ` message on stderr, exit 1, PATH untouched;\n  - (e) replace fails mid-write: PATH keeps its old content and no temporary file is left behind;\n  - (f) PATH is a directory, or its parent is missing: exit 1;\n  - (g) PATH equals the store file: refused, exit 1, store unchanged;\n  - (h) restore by copy: copying the backup over the store, then listing, shows the same notes.\n- Prior art: `tests/test_notes.py`, `CliTest.test_add_and_search` (store path via environment variable, redirected stdout), and `StoreTest.setUp` (temporary store path).\n\n## Quality Requirements\n\n- **Serves:** R-2 (no note is lost; a copy on another disk survives the loss of this one), QG-1, and the stakeholder expectation that users keep notes for years without losing any.\n- **Keeps:**\n  - QS-1: the atomic-write rule for every file the store writes, and the store still opens after a crash.\n  - QS-2: `python3 -m notes backup` needs no install step.\n  - QS-3: the backup logic sits in the store block; no other block touches the storage.\n- **Builds on:** ADR-0001 (SQLite file, which the backup copies), ADR-0003 (only the store touches the database), ADR-0002 (dependency and command decisions are central).\n- **Blocked by:**\n  - **ADR-0004**, \"Write notes atomically via a temporary file and rename\", status `proposed`. The atomic-write requirement rests on it. This spec does not build on it until the architect accepts it.\n  - **The `backup` command name.** ADR-0002 lists CLI command names as decided centrally. No accepted ADR records `backup`. The architect must accept an ADR for it, or record acceptance of this spec's command name.\n- **Affected by, not blocking:** ADR-0005, \"Add a PostgreSQL backend\", status `proposed`. A PostgreSQL store is not one file, so \"copy the store to PATH\" would need a new definition if ADR-0005 is accepted. See Further Notes.\n\n## Out of Scope\n\n- A restore command. A later spec adds it. This spec only ensures the backup file is restorable by copying and opens as a store.\n- Scheduled or automatic backups, retention, rotation, and incremental backups.\n- Encrypting or compressing the backup.\n- Backing up to a remote or synced location (R-4 is deferred).\n- Backing up a PostgreSQL store (ADR-0005, proposed).\n- Verifying backup contents beyond the count printed.\n\n## Further Notes\n\n**Assumptions.** The user was unavailable, so these were stated rather than asked. The architect should confirm or change each.\n\n- **A1 Seam.** The command entry point, with the store path set through the environment. Not agreed with the user.\n- **A2 Output.** A bare integer on one line on stdout, as `add` prints a bare id. The approved design says only \"prints the number of notes\".\n- **A3 Missing store.** Opening follows existing behaviour, which creates an empty store file at the store path. So `notes backup` with no store creates one, writes a backup of 0 notes, and exits 0. The side effect creates a file; the architect may prefer an error.\n- **A4 PATH equals the store file.** Refused with exit 1; the store is untouched. The approved design does not cover this case.\n- **A5 Relative PATH.** Resolved against the current working directory, as for any path argument.\n- **A6 Directory or missing parent.** Exit 1 with a message on stderr.\n- **A7 Restore by copy.** The user must not copy over the store while a `notes` command is running. The spec does not guard against it.\n- **A8 Command name and argument.** `backup` with one positional PATH, as approved. It still needs the architect's recorded decision (see Quality Requirements).\n- **A9 ADR-0004.** Used as the user stated (\"as ADR-0004 says\"). Its status is still `proposed`, so the blocked-by rule applies until it is accepted.\n- **A10 Snapshot mechanism.** Not fixed by the design. The spec requires a consistent snapshot; the plan chooses how.\n\n**Glossary.** \"Backup\" was added to `GLOSSARY.md`.\n\n**ADR-0005.** If the PostgreSQL backend is accepted, the definition of a backup for that engine must be written before this command supports it.\n\n**Pending for the architect, in order:**\n1. Accept ADR-0004, which this spec's atomic-write rule rests on.\n2. Record the `backup` command name, per ADR-0002.\n3. Confirm assumptions A1 to A4, which the design left open.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-gfng5laj/project/docs/specs/2026-11-22-backup-command-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

The spec is written. Publishing to a local file means committing it, so I'll commit the spec and the glossary change together as one docs commit.

### tool_use Bash

```json
{
 "command": "git add GLOSSARY.md docs/specs/2026-11-22-backup-command-spec.md && git commit -q -F - <<'EOF'\ndocs: spec the notes backup command\n\nSpecify `notes backup PATH`: copy the store to PATH atomically, print\nthe number of notes copied, and exit 0; on failure print the error on\nstderr, exit 1, and leave PATH unchanged. Add \"backup\" to the glossary.\n\nThe spec is blocked until ADR-0004 (atomic writes) is accepted and the\n`backup` command name has an accepted decision. The user was unavailable,\nso the open points are stated as assumptions A1-A10 for the architect.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\nEOF\ngit log --oneline | head -3 && git status --short",
 "description": "Commit the spec and glossary change"
}
```

### tool_result

```
0ac7baf docs: spec the notes backup command
e484b0c fixture
```

### assistant

The spec is written and committed at `docs/specs/2026-11-22-backup-command-spec.md`, with "backup" added to `GLOSSARY.md`. Commit `0ac7baf` contains both. The spec is blocked, not ready for implementation.

**Blocked until the architect acts:**
1. **ADR-0004 (atomic writes) is `proposed`.** The spec's atomic-write rule rests on it. You wrote "as ADR-0004 says", but the process treats a proposed ADR as blocking until it's accepted, so I marked it that way.
2. **The `backup` command name has no accepted decision.** ADR-0002 lists CLI command names as central, and no ADR records `backup`.

**Assumptions I stated in the spec, since you were unavailable:**
- **A1 Seam:** the command entry point, with the store path set through the environment, following the existing `CliTest` pattern.
- **A2 Output:** a bare integer on one line on stdout, mirroring how `add` prints an id.
- **A3 Missing store:** existing behaviour creates an empty store on open, so `notes backup` with no store creates one and writes a 0-note backup. This is a side effect you may want to turn into an error.
- **A4 PATH equals the store:** refused with exit 1, store untouched.
- **A10 Snapshot mechanism:** the spec requires a consistent snapshot and leaves the mechanism to the plan. A raw byte copy of a live file does not guarantee one.

The spec puts the backup logic in the store module, because ADR-0003 keeps SQLite access there. It also lists ADR-0005 (PostgreSQL, proposed) as affecting this design without blocking it.

I did not write a plan or tickets, since you asked only for the spec. The repo has no tracker config, so the spec went to a local file. I committed it because the spec skill's publish step calls for it. Say if you'd rather I hadn't.

### result (success)
