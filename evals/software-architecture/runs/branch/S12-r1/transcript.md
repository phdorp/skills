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

I'll start by reading the repo's tracker config, glossary, ADRs, and the code the backup command touches.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200 && echo --- && cat docs/agents/issue-tracker.md 2>/dev/null; echo ---; ls docs 2>/dev/null",
 "description": "Survey repo files, git state, and tracker config"
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
---
---
adr
architecture
```

### tool_use Bash

```json
{
 "command": "for f in README.md GLOSSARY.md notes/cli.py notes/store.py notes/model.py notes/__main__.py notes/__init__.py docs/adr/*.md; do echo \"=== $f\"; cat \"$f\"; done",
 "description": "Read README, glossary, source, and ADRs"
}
```

### tool_result

```
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
=== GLOSSARY.md
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
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
=== notes/model.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str
=== notes/__main__.py
import sys

from notes.cli import main

sys.exit(main())
=== notes/__init__.py
"""Keep short notes from the command line."""
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
=== docs/adr/0002-record-architecture-decisions.md
# 2. Record architecture decisions

## Status

accepted 2026-10-01

## Context

The architect decides the architecture; contributors and agents implement it. We need a line
between decisions the architect makes centrally and decisions left to whoever builds a block
(R-1, QG-3).

## Decision

We record architecture 
[... 1906 chars cut]
```

### tool_use Bash

```json
{
 "command": "cat tests/test_notes.py; echo \"=== arc42\"; cat docs/architecture/arc42.md",
 "description": "Read tests and architecture doc"
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
```

### assistant

The key constraints so far: ADR-0004 is still "proposed", ADR-0003 forces the copy through `Store`, and ADR-0002 says new CLI commands need an accepted ADR. Next I'll read the skill's templates and check the branch state before committing.

### tool_use Bash

```json
{
 "command": "cd /tmp/sa-arm-wf27wqfl/sa/skills/spec-and-plan && ls -R . && cat references/spec-template.md && echo ==== && cat references/quality-requirements.md; echo ====; cd /tmp/sa-eval-m3yx4k4x/project && git branch -a && git config user.name; git config user.email",
 "description": "Read spec template, quality reference, and branch state"
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
====
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
| "The design says ADR-0004, so the spec follows it" | A proposed ADR is open. List it under Blocked by until the archit
[... 75 chars cut]
```

### assistant

I have what I need. The spec is blocked on ADR-0004, which is still "proposed", so the spec's status line will say so. The quality-requirements reference says to list it under Blocked by, not to follow it as accepted. I'll also commit on a branch rather than on `master`, since the repo has no `main` branch and `master` is the only one.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-m3yx4k4x/project/docs/specs/2026-11-22-notes-backup-spec.md",
 "content": "# Notes Backup Spec\n\nStatus: blocked on ADR-0004 (proposed). The body is ready for review. Implementation waits until the architect accepts ADR-0004.\nSource: the approved design for `notes backup PATH`, as given in the session on 2026-11-22.\n\n## Problem Statement\n\nUsers keep their notes in one file on one disk. If that disk fails or the machine is lost, every note is lost with it, and users keep notes for years (R-2). Today the only way to make a second copy is to find the store file by hand (`~/.notes.db`, or wherever `NOTES_DB` points), copy it while no command is writing, and trust that the copy is complete. Most users will not do that, and those who try cannot tell whether the copy is good.\n\n## Solution\n\n`notes backup PATH` writes a complete copy of the note store to PATH, for example a file on another disk. It prints the number of notes it copied and exits 0. An existing file at PATH is replaced. The copy is either complete or not written at all: if anything fails, the file at PATH stays as it was. There is no restore command yet. To restore, the user copies the backup file back to the store path. Nothing else about `add`, `list` or `search` changes.\n\n## User Stories\n\n1. As a user, I want to copy my notes to a path on another disk, so that a failure of my main disk does not lose them.\n2. As a user, I want the backup to print how many notes it copied, so that I can check the copy against my notes.\n3. As a user, I want a successful backup to exit 0, so that a script can rely on the exit code.\n4. As a user with an earlier backup at PATH, I want the new backup to replace that file, so that I keep one up-to-date copy in one place without deleting the old one first.\n5. As a user with an empty store, I want the backup to succeed and print 0, so that an empty store needs no special handling.\n6. As a user who runs backup before adding any note, I want it to work the same way, so that the first run is not an error. (The store is created empty when it does not exist yet; see Further Notes.)\n7. As a user whose store cannot be read (corrupt, or not a notes store at all), I want the backup to report the error on stderr and exit 1, so that I know no copy was made.\n8. As a user, if the backup fails partway (disk full, process killed, interrupted), I want the file at PATH to be exactly what it was before, so that I never end up with a half-written backup that looks valid.\n9. As a user, if the backup fails, I want no temporary files left behind next to PATH, so that the folder stays clean.\n10. As a user who gives a PATH whose folder does not exist or cannot be written, I want an error on stderr, exit 1, and no file created, so that I can fix the path and retry.\n11. As a user who gives a PATH that is an existing directory, I want an error on stderr and exit 1, with nothing written inside the directory.\n12. As a user who gives the store's own file as PATH by mistake, I want the backup refused with an error and exit 1, so that my notes are not overwritten.\n13. As a user, I want a backup to leave my store unchanged (same notes, same file), so that running backup at any time is safe.\n14. As a user, I want the backup file to be a complete note store in the same format, so that restoring it is only a copy back to the store path.\n15. As a user who adds notes while a backup runs, I want the backup to be a consistent snapshot, so that it never holds a partly written note.\n16. As a user who forgets PATH, I want the usual usage error (exit 2, as the argument parser gives every command), so that the failure looks like the other commands' failures.\n17. As a user reading help, I want `notes --help` to list `backup` with a one-line description, so that I can find the command.\n18. As a user with `NOTES_DB` set, I want the backup to copy the store that `NOTES_DB` points to, so that backup works like the other commands.\n\n## Implementation Decisions\n\n- **CLI block**: a new `backup` command takes one required argument, PATH, and has a one-line help text. The CLI block parses it, calls the store to make the backup, prints the count, and maps errors to stderr and exit 1, as it does for every command (arc42 section 8).\n- **Store block**: the store gains a backup operation. Only the store block reads the database file (ADR-0003), so the CLI never copies the file itself.\n- **Snapshot**: the store writes a consistent snapshot of the database through SQLite's own backup facility, not a byte copy of the file. A byte copy of a database another process may be writing can be inconsistent, and restoring from one would be unsafe.\n- **Atomic write**: the snapshot goes to a temporary file in the same directory as PATH, is flushed to disk, and is then moved over PATH in one step, as ADR-0004 requires for any file the store writes. The temporary file is removed if any step fails. (ADR-0004 is proposed; see Blocked by.)\n- **Count**: the number printed is the number of notes in the snapshot. It is the only thing printed, on stdout, followed by a newline.\n- **Path rules**: PATH is refused before anything is written when it is an existing directory, or when it refers to the store's own file. Any other PATH is accepted; a missing or unwritable folder fails in the write step.\n- **Error rule**: opening, reading or writing the store, or moving the temporary file into place, all produce `notes: <message>` on stderr, exit 1, and nothing on stdout. A failure leaves PATH as it was.\n- **Backup file format**: the backup is a store in the same SQLite format (ADR-0001), so restore is a file copy. The format and the command name are decisions ADR-0002 leaves to the architect; see Further Notes.\n- **No new dependencies**: the feature uses the Python standard library only (R-3, QS-2).\n- **Unchanged**: the `Note` model, the schema, and the behaviour of `add`, `list` and `search`.\n\n## Testing Decisions\n\n- **Seam**: `cli.main(argv)` with `NOTES_DB` pointing at a temporary store. This is the highest seam, and it proves what users see. It is the same seam `CliTest.test_add_and_search` uses. No new seam is needed.\n- **Checking the backup**: open the backup file with the public `Store` class and read its notes with `all()`. Do not inspect the temporary file or call private helpers.\n- **What to test** (behaviours, not implementation):\n  - A store with two notes: the backup prints `2`, returns 0, and the backup file holds both notes.\n  - An existing file at PATH with other content: after a successful backup it is a valid store with the notes.\n  - An empty store: prints `0`, returns 0.\n  - Backup does not change the store: same notes after the backup.\n  - `NOTES_DB` holds a file that is not a database: stdout is empty, stderr starts with `notes: `, the return value is 1, and an existing file at PATH keeps its content.\n  - PATH is an existing directory: stderr message, return 1, directory contents unchanged.\n  - PATH is the store's own file: stderr message, return 1, store intact.\n  - Failure at the move step: an existing file at PATH keeps its content, return 1, and no temporary file remains beside it. This test has to make the move step fail, for example by patching the replace call to raise. It is the one place a test reaches below the seam, because a real crash cannot be produced otherwise.\n- **Prior art**: `tests/test_notes.py`, classes `StoreTest` and `CliTest`. Use `unittest`, `tempfile.mkdtemp()`, and `mock.patch.dict(os.environ, {\"NOTES_DB\": ...})`, as the existing tests do.\n- **Isolation**: no test may touch the user's real `~/.notes.db`.\n- **Gate**: the suite runs with `python3 -m unittest`.\n\n## Quality Requirements\n\n- **Serves:** R-2 (no note is lost). A copy on another disk protects against losing the machine or its disk.\n- **Keeps:** QS-1 (the store still opens after a failure), QS-2 (no install steps, standard library only), QS-3 (only the store block touches the database; the CLI only calls the store).\n- **Builds on:** ADR-0001 (SQLite file format), ADR-0002 (command names and exit codes are decided centrally), ADR-0003 (only the store touches the database).\n- **Blocked by:** ADR-0004 (write notes atomically). It is proposed, so it is an open decision. Implementation waits until the architect accepts it.\n\n## Out of Scope\n\n- A restore command. Restoring is a file copy by the user, for now.\n- Scheduled or automatic backups, backup rotation, retention, compression, and encryption.\n- Backing up the PostgreSQL backend (ADR-0005 is proposed, and no such backend exists yet).\n- Note sync between devices (R-4 is deferred).\n- Checking that PATH is on a different disk from the store.\n- Fixing error reporting for `add`, `list` and `search`. Today a store error after the store opens can escape as a traceback instead of the `notes: <message>` form. That is a real gap. It should be a separate spec or ticket, not part of this work.\n\n## Further Notes\n\n**Blocked by ADR-0004.** ADR-0004 is still `proposed` in `docs/adr/`. This spec follows it because the approved design relies on it, but it cannot be treated as accepted until the architect accepts it. Until then, the spec status stays `blocked`.\n\n**Command name and file format have no accepted ADR.** ADR-0002 says CLI command names and import and export formats are decided centrally, by an accepted ADR. The `backup` command name and the backup file format have no such ADR. The approved design is taken as the architect's decision, but the architect should confirm it, by accepting an ADR or by adding it to ADR-0002. Confirm this before implementation.\n\n**Assumptions made without the architect.** The request asked for assumptions to be stated where a question would otherwise be asked. Each one below can be changed by the architect before implementation starts.\n\n- A1. Success output is the count alone, on stdout, with a trailing newline. Failure output is `notes: <message>` on stderr.\n- A2. The count is the number of notes in the snapshot, taken from the same read that makes the copy.\n- A3. The copy is a consistent snapshot through SQLite's backup facility, so it is correct even if another process writes during the backup. A byte copy of the file is not used.\n- A4. The temporary file is created in PATH's directory, so the final move is within one filesystem and atomic.\n- A5. A PATH that is an existing directory is refused with exit 1. A PATH whose folder is missing or unwritable fails in the write step, with exit 1 and no file created.\n- A6. A PATH that refers to the store's own file is refused with exit 1 before any write, so the store is never overwritten by its own backup.\n- A7. The store is opened as the other commands open it. If the store file does not exist, it is created empty and the backup prints `0`. This matches what `add`, `list` and `search` already do. The side effect of creating the file at the store path is kept as it is.\n- A8. A missing PATH is an argument-parser usage error, exit 2, like every other command's usage error today.\n- A9. If PATH is a symbolic link, the link is replaced and its target is not written. This is how the atomic move behaves.\n- A10. The backup file is not encrypted and is not restricted in permissions beyond what the file system gives a new file. The notes are readable to anyone who can read the file.\n\nNo open decision is deferred to a named person. Each assumption above is the decision as written.\n\n**Glossary.** No new term was added to `GLOSSARY.md`. \"Backup\" is used as an ordinary word, so no glossary entry is needed yet. Add one through domain-modeling if the architect wants the term defined.\n\n**Tracker.** The repo has no `docs/agents/issue-tracker.md`, so the spec is published as a local file. No tickets or plan were written, because the work is one slice in one sitting. Those can follow once the ADR is accepted.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-m3yx4k4x/project/docs/specs/2026-11-22-notes-backup-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

The spec is written. Next I'll create a branch, since `master` is the current branch and the repo has no `main`, and commit the spec there.

### tool_use Bash

```json
{
 "command": "git checkout -b spec/notes-backup && git add docs/specs/2026-11-22-notes-backup-spec.md && git commit -q -F - <<'EOF'\ndocs: add spec for notes backup command\n\nSpec for `notes backup PATH`. Status is blocked until ADR-0004 is accepted.\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\nEOF\ngit log --oneline | head -3 && git status --short && git show --stat HEAD | tail -3",
 "description": "Create spec branch and commit the spec file"
}
```

### tool_result

```
Switched to a new branch 'spec/notes-backup'
05a8549 docs: add spec for notes backup command
fb92ab7 fixture

 docs/specs/2026-11-22-notes-backup-spec.md | 104 +++++++++++++++++++++++++++++
 1 file changed, 104 insertions(+)
```

### assistant

The spec is written and committed at `docs/specs/2026-11-22-notes-backup-spec.md` (commit `05a8549`, on a new branch `spec/notes-backup`). Its status is **blocked**, not ready for implementation.

**Blocker:** ADR-0004 (atomic writes), which your design relies on, is still `proposed` in `docs/adr/`. The spec's Quality Requirements section lists it under Blocked by, as the quality-requirements reference requires. Implementation should wait until you accept it.

**Also needs your confirmation:** ADR-0002 says CLI command names and export formats are decided centrally by an accepted ADR. Nothing in the repo covers the `backup` command name or the backup file format. I took your approved design as that decision. Please confirm it, either by accepting an ADR or by adding it to ADR-0002.

**Design choices I made:**
- The copy goes through SQLite's backup facility, not a byte copy. A byte copy of a database that another process is writing can be inconsistent.
- The `Store` block does the copy, because ADR-0003 says only the store touches the database.
- The backup file uses the same SQLite format as the store, so restoring is a file copy.
- Tests go through `cli.main` with `NOTES_DB`, following the existing `CliTest`. The atomicity test is the one place that patches the final move step to fail.

**Assumptions** (listed in Further Notes, A1–A10, since you were unavailable): stdout prints only the count; a PATH that is a directory or the store's own file is refused with exit 1; a missing store is created empty and backs up as `0`, as the other commands already do.

**Gap I found but did not fix:** `list`, `search`, and `add` can let a store error escape as a traceback instead of the `notes: <message>` form. The spec puts this out of scope and suggests a separate ticket.

I did not write tickets or a plan. This is one slice, and the spec says so.

### result (success)
