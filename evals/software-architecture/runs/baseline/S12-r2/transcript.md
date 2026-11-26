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

I'll start by reading the repo: the tracker config, glossary, ADRs, and the note store code the backup touches.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200 && echo --- && cat docs/agents/issue-tracker.md 2>/dev/null; echo \"---tracker-exit=$?\"",
 "description": "Survey repo files and tracker config"
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
---tracker-exit=1
```

### tool_use Bash

```json
{
 "command": "cat README.md GLOSSARY.md docs/adr/*.md && echo ---ARCH && cat docs/architecture/arc42.md",
 "description": "Read README, glossary, ADRs, architecture doc"
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
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
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
# 5. Add a PostgreSQL backend

## Status

proposed

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.
---ARCH
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
| QG-3 | Maintainab
[... 1713 chars cut]
```

### tool_use Bash

```json
{
 "command": "for f in notes/*.py; do echo \"=== $f\"; cat \"$f\"; done",
 "description": "Read the notes package source"
}
```

### tool_result

```
=== notes/__init__.py
"""Keep short notes from the command line."""
=== notes/__main__.py
import sys

from notes.cli import main

sys.exit(main())
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
=== notes/model.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str
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
```

### tool_use Bash

```json
{
 "command": "cat tests/test_notes.py",
 "description": "Read existing tests for prior-art patterns"
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
```

### assistant

Two things stand out before I write. ADR-0004 is still `proposed`, and `Store()` creates the database file if it is missing. I'll check the spec template and the conventions for where specs are published.

### tool_use Bash

```json
{
 "command": "cd /tmp/sa-arm-dufe3fqw/sa/skills/spec-and-plan && cat references/spec-template.md; echo ---; ls /tmp/sa-arm-dufe3fqw/sa/skills/ | head -50; echo ---; cd /tmp/sa-eval-koidg55s/project && ls docs; git -C . log -1 --format=%ad",
 "description": "Read the spec template and repo docs layout"
}
```

### tool_result

```
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
---
code-review
codebase-design
conventional-commits
design-dialogue
dispatching-parallel-agents
domain-modeling
executing-plans
finishing-a-development-branch
handoff
improve-codebase-architecture
openmodelica
prototype
research
retro
setup-pre-commit
setup-project-workflow
setup-ts-deep-modules
spec-and-plan
squash-merge-message
systematic-debugging
teach
test-driven-development
to-questionnaire
triage
using-git-worktrees
verification-before-completion
wait-what
wayfinder
wizard
writing-for-agents
---
adr
architecture
Sun Nov 22 09:14:14 2026 +0100
```

### assistant

No tracker is configured (`docs/agents/issue-tracker.md` is absent), so this goes to a local file under `docs/specs/`. I'll write the spec now and record each gap as a stated assumption, since you are unavailable.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-koidg55s/project/docs/specs/2026-11-22-notes-backup-spec.md",
 "content": "# Notes Backup Spec\n\nStatus: ready-for-agent. Implementation is blocked until ADR-0004 is accepted (see Further Notes, item 1).\nSource: the approved design for `notes backup`, given in the conversation of 2026-11-22.\n\n### Problem Statement\n\nNotes are kept in one SQLite file (ADR-0001). A user who loses that file, or the disk it sits on, loses every note. Users who keep notes for years (R-2) have no supported way to keep a second copy on another disk. They can copy the file by hand, but they do not know that a copy taken while the program writes can be torn, and the program gives them no count to check the copy against.\n\n### Solution\n\n`notes backup PATH` writes a copy of the store to PATH. The copy is complete or absent, never partial. The command prints how many notes the copy holds and exits 0. To restore, the user copies the file back over the store. No restore command exists yet.\n\n### User Stories\n\n1. As a user, I want to run `notes backup PATH`, so that I have a copy of my notes on another disk.\n2. As a user, I want the command to print the number of notes in the copy, so that I can check the copy holds what I expect.\n3. As a user, I want the command to exit 0 when the copy is written, so that scripts can rely on it.\n4. As a user with a previous backup at PATH, I want the new backup to replace that file, so that I do not have to delete it first.\n5. As a user with an empty store, I want the backup to succeed and print 0, so that an empty store is backed up like any other.\n6. As a user with many notes, I want the copy to hold every note, so that restoring it gives back everything.\n7. As a user, I want the copy to be a complete snapshot, so that a note added while the backup runs is either in the copy or not, and the copy always opens.\n8. As a user, I want to restore by copying the backup file over my store path, so that I need no restore command.\n9. As a user whose store is at a path set by `NOTES_DB`, I want the backup to copy that store, so that the setting applies to backup too.\n10. As a user whose store file does not exist yet, I want an error on stderr and exit 1, so that I learn there is nothing to back up and no empty store is created as a side effect.\n11. As a user whose store is unreadable (for example a corrupt file), I want the error on stderr, exit 1, and any existing file at PATH left unchanged, so that a failed backup never destroys a good backup.\n12. As a user whose PATH is in a directory that does not exist, I want an error on stderr and exit 1, so that I can correct the path.\n13. As a user whose PATH is an existing directory, I want an error on stderr and exit 1, so that the directory is not touched.\n14. As a user who gives the store's own path as PATH, I want an error on stderr and exit 1 with the store unchanged, so that the store is never replaced by a copy of itself.\n15. As a user whose disk fills up or whose PATH is not writable during the copy, I want an error on stderr, exit 1, the existing file at PATH unchanged, and no temporary file left in the directory.\n16. As a user, I want the backup file readable only by my account, so that my notes are not exposed by default.\n\n### Implementation Decisions\n\n- **Store module.** The backup operation belongs to the store module. ADR-0003 forbids the CLI from touching the database file. The CLI parses `backup PATH`, calls the store, prints the count, and maps errors as it does for every command.\n- **Consistent snapshot.** The copy is made with SQLite's online backup facility in one step, from the open store. The result is a point-in-time snapshot even if another process writes during the copy.\n- **Atomic write (ADR-0004).** The copy is first written to a temporary file in the same directory as PATH, flushed with `os.fsync`, and moved onto PATH with `os.replace`. The temporary file must be in PATH's directory so the replace stays on one filesystem. The temporary file is removed if any step fails.\n- **File format.** The backup file is a SQLite database with the same schema as the store. Restoring is a plain file copy, so the format must be the store format and nothing else.\n- **Count.** The count printed is the number of rows in the `notes` table of the finished copy, read from the copy, not from the source. Printed alone on stdout followed by a newline, matching how `add` prints its id.\n- **Exit codes and errors.** Success exits 0. Every failure prints `notes: <message>` on stderr and exits 1. The existing error path covers only opening the store; the backup's errors (write, rename, path checks) must go through the same reporting.\n- **No side effects on failure.** On any failure, PATH keeps its previous content (or stays absent) and no temporary file remains in its directory.\n- **Missing store.** The backup does not create the store file. If it does not exist, the command fails with exit 1. This differs from today's open behaviour, which creates an empty store, so the existence check must come before the store is opened.\n- **Same path.** If PATH resolves to the store file, the command fails with exit 1 and changes nothing.\n- **Permissions.** The backup file gets owner-only permissions (0600), the default for a newly created temporary file.\n- **Dependencies.** Standard library only (R-3).\n\n### Testing Decisions\n\n- **Seam.** The CLI entry point `main(argv)` with `NOTES_DB` pointed at a temporary store, as `CliTest.test_add_and_search` does in `tests/test_notes.py`. This is the one seam; all behaviours below are tested through it, with no mocking.\n- **Behaviours to pin:**\n  - `backup` prints the note count and returns 0 (stories 1–3).\n  - The copy, opened with `Store`, holds the same notes as the source (stories 6, 8).\n  - An existing file at PATH is replaced (story 4).\n  - An empty store backs up and prints `0` (story 5).\n  - `NOTES_DB` selects the source store (story 9).\n  - A missing store exits 1, prints to stderr, and creates neither the store nor PATH (story 10).\n  - A corrupt store exits 1, leaves an existing PATH byte-for-byte unchanged, and leaves no temporary file in the directory (story 11).\n  - A PATH in a missing directory exits 1 (story 12).\n  - A PATH that is an existing directory exits 1 and the directory is unchanged (story 13).\n  - A PATH equal to the store exits 1 and the store is unchanged (story 14).\n- **Not unit-tested.** Crash safety (a kill mid-write) and the 0600 mode are checked by inspection of the write sequence and by a manual run. Story 15 (disk full) is not reproducible without mocking, so it is covered by the corrupt-store and unwritable-target cases above.\n- **Prior art.** `tests/test_notes.py`: `StoreTest` for store behaviour and `CliTest` for command behaviour, using `tempfile.mkdtemp()` and `mock.patch.dict(os.environ, ...)`.\n\n### Out of Scope\n\n- A restore command (story 8 covers restore by file copy only).\n- Backup of other stores, such as a PostgreSQL store (ADR-0005 is proposed and not implemented).\n- Scheduling, rotation, or retention of backups.\n- Encryption or compression of the backup file.\n- A text or JSON export format (a separate export decision under ADR-0002).\n- Prompting before replacing an existing file.\n- A directory `fsync` after the rename. ADR-0004 does not require it.\n\n### Further Notes\n\n1. **ADR-0004 is still `proposed`.** This spec relies on its atomic-write rule. ADR-0002 says work depending on an undecided ADR waits until the architect accepts it. Accepting ADR-0004 is the architect's decision; I have not changed its status.\n2. **Central decisions without an ADR.** ADR-0002 lists CLI command names, exit codes, and import/export formats as decisions needing an accepted ADR. The `backup` command, its exit codes, and the backup file format are not recorded in any ADR. They should be recorded (a new ADR, or an amendment to ADR-0004) before implementation.\n3. **Assumptions made without you.** Each is stated in the body and can be reversed:\n   - A missing store is an error, not a reason to create an empty store (story 10).\n   - Backing up onto the store's own path is an error (story 14).\n   - The backup file is owner-only, 0600 (story 16).\n   - The count is printed as a bare number, like `add` prints an id (Implementation Decisions).\n   - The backup file has the store's schema, so restore is a file copy (Implementation Decisions).\n4. **Existing gap, not fixed here.** The CLI reports only store-open errors in the `notes: <message>` form. Errors raised by `add`, `list`, or `search` after the store opens still surface as tracebacks. This spec does not change that.\n5. **Glossary.** \"Backup\" and \"backup file\" are used here but not defined in `GLOSSARY.md`. They should be added through the domain-modeling skill.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-koidg55s/project/docs/specs/2026-11-22-notes-backup-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

The spec is written. Publishing for a repo with no tracker means committing the file, so I'll commit just this file.

### tool_use Bash

```json
{
 "command": "git add docs/specs/2026-11-22-notes-backup-spec.md && git commit -q -m \"docs(specs): add notes backup spec\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2 && git status --short",
 "description": "Commit the spec file only"
}
```

### tool_result

```
f58448a docs(specs): add notes backup spec
e370ee3 fixture
```

### assistant

The spec is written and committed as `docs/specs/2026-11-22-notes-backup-spec.md` (commit `f58448a`). There is no issue tracker configured, so it went to a local file. I wrote only the spec, with no tickets or plan, since you asked for the spec alone.

Implementation is blocked on one item. ADR-0004 is still `proposed`, and it is the rule that makes the backup atomic. ADR-0002 says work that depends on an undecided ADR waits for the architect to accept it. I did not change its status.

**Assumptions I made where I would have asked you** (all listed in the spec's Further Notes):
- A missing store is an error, exit 1. Today's store open creates an empty file, so the backup has to check for the file before opening the store.
- Backing up onto the store's own path is an error, exit 1, and the store is left unchanged.
- The backup file is owner-only (0600), the default for the temporary file it is written to.
- The count is printed as a bare number on stdout, the same way `add` prints an id.
- The backup is a SQLite file with the store's schema, so restoring is a plain copy.

**Other items the spec flags:**
- The `backup` command, its exit codes, and the backup file format are central decisions under ADR-0002. None is recorded in an ADR yet. They need one, or an amendment to ADR-0004, before implementation.
- The CLI reports only store-open errors in the `notes: <message>` form. Errors from `add`, `list`, and `search` still surface as tracebacks. I did not change that.
- "Backup" is not in `GLOSSARY.md` yet. It should be added through the domain-modeling skill.

The spec's testing section uses one seam, `main(argv)` with `NOTES_DB` set, following `CliTest` in `tests/test_notes.py`. Crash safety and file mode are checked by inspection and a manual run, not by unit tests.

### result (success)
