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

I'll start by reading the repo: the tracker config, glossary, ADRs, and the existing store and command code.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200 && echo --- && cat docs/agents/issue-tracker.md 2>/dev/null; echo \"--- glossary\"; cat GLOSSARY.md 2>/dev/null; echo \"--- adr\"; ls docs/adr 2>/dev/null",
 "description": "Survey repo files, tracker doc, glossary, ADRs"
}
```

### tool_result

```
5ee4fe7 fixture
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
--- glossary
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.
--- adr
0001-use-sqlite-for-storage.md
0002-record-architecture-decisions.md
0003-cli-reaches-storage-only-through-store.md
0004-write-notes-atomically.md
0005-add-postgresql-backend.md
```

### tool_use Bash

```json
{
 "command": "for f in docs/adr/*.md; do echo \"=== $f\"; cat \"$f\"; done; echo \"=== arc42\"; cat docs/architecture/arc42.md",
 "description": "Read all ADRs and architecture doc"
}
```

### tool_result

```
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
| Contributors | change
[... 1479 chars cut]
```

### tool_use Bash

```json
{
 "command": "for f in README.md notes/*.py; do echo \"=== $f\"; cat \"$f\"; done; echo \"=== tests\"; cat tests/test_notes.py",
 "description": "Read source, README and tests"
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

[... 199 chars cut]
```

### assistant

The spec depends on two things I need to check before writing: ADR-0004 is still `proposed`, and ADR-0002 says work that depends on an unaccepted decision waits. I'll read the spec template and quality-requirements reference the skill points to, and check the branch.

### tool_use Bash

```json
{
 "command": "cd /tmp/sa-arm-izrs660r/sa/skills/spec-and-plan && cat references/spec-template.md; echo \"=== QR\"; cat references/quality-requirements.md; echo \"=== branches\"; cd /tmp/sa-eval-o__w81c6/project && git branch -a && ls docs",
 "description": "Read spec template, quality reference, and branches"
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
=== QR
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

A proposed ADR is an open decision: list it under **Blocked by**, and say so in your final
message. While **Blocked by** lists an ADR, the spec's status line reads
`Status: blocked (ADR-nnnn)`, and a tracker issue gets the blocked marking instead of
`ready-for-agent`. The spec builds on the decision once the architect accepts the ADR.

## Red flags

| Thought | Reality |
|---|---|
| "The design relies on a proposed ADR, so the spec follows it" | A proposed ADR is open. 
[... 261 chars cut]
```

### assistant

Two findings change how I write the spec. ADR-0004 is only `proposed`, so the spec's status has to be `blocked (ADR-0004)`. The repo has no tracker config, so the spec goes to `docs/specs/` and gets committed. The spec also introduces a new term, "backup", so the glossary update goes through domain-modeling. I'll load that skill first.

### tool_use Skill

```json
{
 "skill": "sa:domain-modeling",
 "args": "Add the term \"Backup\" to GLOSSARY.md: a copy of the store written to a path the user chooses, made with `notes backup PATH`. Only glossary work for this spec; no ADR changes."
}
```

### tool_result

```
Launching skill: sa:domain-modeling
```

### assistant

The glossary has a fixed style, and the rules say no implementation details. I'll add the entry in that style, defining the term by what it is for the user.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-o__w81c6/project/GLOSSARY.md",
 "old_string": "**Store**: the place notes are kept between runs.",
 "new_string": "**Store**: the place notes are kept between runs.\n\n**Backup**: a copy of the store that a user keeps somewhere else, such as on another disk, at a path the user chooses."
}
```

### tool_result

```
The file /tmp/sa-eval-o__w81c6/project/GLOSSARY.md has been updated successfully.
```

### assistant

The glossary entry is in. Next I'll write the spec to `docs/specs/`. It is blocked on ADR-0004 and records each assumption where you would have been asked.

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/sa-eval-o__w81c6/project/docs/specs && cat > /tmp/sa-eval-o__w81c6/project/docs/specs/2026-11-22-backup-spec.md <<'EOF'\n# Backup Spec\n\nStatus: blocked (ADR-0004)\nSource: the approved design for `notes backup`, given in the conversation of 2026-11-22.\n\n## Problem Statement\n\nUsers keep notes for years (R-2), but the only copy of their notes is the single store file on\nthe machine they use. A disk failure or a lost laptop loses everything. A user who wants a second\ncopy on another disk has no supported way to make one that is guaranteed to be whole.\n\n## Solution\n\nA user runs `notes backup PATH`. The command writes a complete copy of the store to PATH and\nprints how many notes the copy holds. The user keeps that file on another disk. The copy is the\nstore itself, so restoring is copying the file back to the store location. A restore command is\nnot part of this work.\n\n## User Stories\n\n1. As a user, I want to run `notes backup PATH`, so that I get a copy of all my notes at PATH.\n2. As a user, I want the command to print the number of notes in the backup, so that I can check it\n   against the number I expect.\n3. As a user, I want the command to exit 0 when the backup succeeds, so that a script can rely on it.\n4. As a user, I want an existing file at PATH replaced by the backup, so that I can reuse one\n   backup name for each run.\n5. As a user, I want a backup to contain every note the store holds at that moment, so that no note\n   is missing from the copy.\n6. As a user, I want a backup taken while the store is in use by another `notes add` to be a\n   consistent copy, so that it never holds half of a change.\n7. As a user, I want a backup of an empty store to succeed and print `0`, so that a fresh install\n   can be backed up without special cases.\n8. As a user, I want a backup to be a valid store, so that I can copy it back and run `notes list`\n   on it.\n9. As a user, I want the store to be left unchanged by a backup, so that backing up never costs me\n   a note.\n10. As a user, I want a failed backup to report the error on stderr and exit 1, so that I know the\n    copy was not made.\n11. As a user, I want a failed backup to leave any existing file at PATH exactly as it was, so that\n    a bad run does not destroy my previous backup.\n12. As a user, I want a backup killed partway through (for example by a power cut) to leave PATH\n    either as it was or as a complete new backup, never as a partial file, so that a crash cannot\n    corrupt my backup (ADR-0004).\n13. As a user, I want the command to refuse when the store file does not exist, so that a backup\n    does not create an empty store as a side effect.\n14. As a user, I want the command to refuse when PATH is the store file itself, so that a backup\n    cannot overwrite the notes it copies.\n15. As a user, I want the command to refuse when the directory of PATH does not exist or PATH is a\n    directory, so that I get a clear error instead of a partial result.\n16. As a user, I want the command to report an unreadable or corrupt store on stderr and exit 1, so\n    that I know the store, not the backup, is the problem.\n17. As a user, I want the command to work with `NOTES_DB` set, so that a backup copies the store I\n    am actually using.\n18. As a user, I want a missing PATH argument to get the usual usage message, so that the command\n    behaves like the others.\n19. As a user on Linux or macOS, I want the backup to need no installed packages, so that it works\n    on the same locked-down machines as the rest of the program (R-3).\n20. As a user, I want the backup file to be a normal file that I can copy to another disk with\n    ordinary tools, so that I do not need the program to move it.\n\n## Implementation Decisions\n\n- **Store block**: a new method on `Store` writes the backup and returns the number of notes in it.\n  It is the only code that touches the database, so the rule that only the store block uses the\n  storage engine holds (ADR-0003).\n- **Consistent copy**: the copy is made with the SQLite online backup facility, which the standard\n  library provides. It copies one consistent snapshot, so a concurrent writer cannot produce a torn\n  copy. A plain file copy of the store file is rejected because it can copy a half-written store.\n- **Atomic write (ADR-0004)**: the copy is first written to a temporary file in the same directory\n  as PATH, flushed to disk, and then moved over PATH. This applies to the backup file as ADR-0004\n  requires for every file the store writes. The temporary file must be in the same directory so the\n  final move stays on one filesystem.\n- **Store must exist**: the backup does not create the store. If the store file is missing, the\n  command fails with an error and writes nothing. Opening the store for backup must not run the\n  table creation that `Store` runs on a normal open.\n- **Refuse PATH equal to the store**: if PATH names the store file (after resolving the path), the\n  command fails with an error and changes nothing.\n- **CLI**: a new subcommand `backup` takes one positional argument, PATH. It is dispatched in the\n  CLI block alongside `add`, `list` and `search`. The CLI block reaches storage only through `Store`\n  (ADR-0003).\n- **Output**: on success, the command prints the note count alone on one line to stdout, as a\n  decimal integer, and exits 0. Nothing else is printed to stdout.\n- **Errors**: every failure prints `notes: <message>` on stderr and exits 1, as arc42 section 8\n  requires. Usage errors keep argparse's current behaviour (exit 2) and are not changed.\n- **Store path**: the store is located as it is for every other command, through `NOTES_DB` or the\n  default path. PATH is taken as given and is not affected by `NOTES_DB`.\n- **No schema or format change**: the backup is the store's own SQLite file (ADR-0001). No new\n  format is introduced.\n- **Quality requirements**: a backup must keep QS-1's guarantee for the backup file: a crash\n  during the backup leaves PATH readable as the old file or the complete new one.\n\n## Testing Decisions\n\nWhat makes a good test here: external behaviour through the seams below. Check what the user sees\n(stdout, stderr, exit code) and what is on disk afterwards (the store and PATH). Do not check which\nSQLite calls were made.\n\nSeams:\n\n- **Command seam**: `notes.cli.main([\"backup\", PATH])`, with `NOTES_DB` pointing at a temporary\n  store, as the existing CLI test does. This proves output, exit codes, refusal cases, and that the\n  store is unchanged. Most behaviour in the user stories is tested here.\n- **Store seam**: `Store.backup(path)`, called directly. This proves the returned count, the copy's\n  contents, and the atomic-replace behaviour. For the failure cases (the write or the final move\n  fails), inject the failure at the point where the store flushes or moves the temporary file, and\n  assert that PATH still holds its previous content and no temporary file is left behind. The\n  existing store tests are prior art for setup and teardown.\n- No new seam is proposed. Both tests above use seams that already exist (`main` and `Store`).\n\nModules tested: the store block (`Store`) and the CLI block (`main`). The test for a killed process\n(SIGKILL during backup) follows the QS-1 test pattern if one exists; if not, it is out of scope for\nthe first version and the in-process failure test stands in for it.\n\nPrior art: `tests/test_notes.py`, class `StoreTest` for store behaviour and class `CliTest` for\ncommand behaviour, including the `NOTES_DB` setup.\n\n## Quality Requirements\n\n- **Serves:** R-2 (no note is lost), R-3 (standard library only)\n- **Keeps:** QS-1 (a crash leaves the store and the backup readable), QS-3 (only the store block and\n  its tests change for the storage engine)\n- **Builds on:** ADR-0001 (SQLite file, atomic transactions), ADR-0003 (CLI reaches storage only\n  through `Store`)\n- **Blocked by:** ADR-0004 (write notes atomically via a temporary file and rename; currently\n  `proposed`). The atomic write in this spec depends on it. Implementation waits until the architect\n  accepts ADR-0004.\n\n## Out of Scope\n\n- A restore command. A user restores by copying the file back. A restore command is a later spec.\n- Automatic or scheduled backups, and backup rotation or retention.\n- Compression or encryption of the backup file.\n- Verifying the backup beyond the count printed. The command does not reopen the copy to check it.\n- Backups of the PostgreSQL backend (ADR-0005 is `proposed`). This spec covers the SQLite store only.\n- Sync between devices (R-4, deferred).\n\n## Further Notes\n\nOpen assumptions, stated because the author could not ask. Each one is a choice the architect can\nchange before implementation starts:\n\n1. **Missing store**: a missing store file is an error, not an empty backup (story 13).\n2. **Output format**: stdout is the count alone on one line (story 2). The brief said \"prints the\n   number\" and did not give a format.\n3. **Refuse PATH = store** (story 14). The brief did not cover this case.\n4. **Symlink at PATH**: the move replaces the symlink itself, not what it points to.\n5. **Existing PATH**: replaced whatever its content, since the command does not read it.\n6. **Leftover temporary file**: a crash can leave a temporary file beside PATH. Later runs do not\n   clean it up. This matches ADR-0004 (the target is never partial) and is not a bug.\n7. **Count source**: the count comes from the same snapshot that is copied, not from a second read.\n8. **Command name and exit codes**: ADR-0002 lists CLI command names and exit codes as decided\n   centrally. No ADR records `backup` yet. The approved design is taken as the architect's decision.\n   The architect should record it in an ADR, or confirm it in ADR-0004's review.\n\nOpen decisions: none left to the implementer. Items 1 to 8 above are stated assumptions, not\ndeferred decisions. The architect should confirm or change them before implementation.\n\nBlocking: ADR-0004 must be accepted before implementation starts. Writing this spec does not depend\non it.\n\nGlossary: \"Backup\" added to `GLOSSARY.md`.\nEOF\ncd /tmp/sa-eval-o__w81c6/project && git add docs/specs/2026-11-22-backup-spec.md GLOSSARY.md && git commit -q -m \"docs: add backup spec and glossary term\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2 && git status --short",
 "description": "Write spec file and commit spec and glossary"
}
```

### tool_result

```
4e04ce7 docs: add backup spec and glossary term
5ee4fe7 fixture
```

### assistant

The spec is written and committed at `docs/specs/2026-11-22-backup-spec.md` (commit `4e04ce7`, on `master`). The spec's status is `blocked (ADR-0004)`.

**Blocker:** ADR-0004 (atomic write via temp file and rename) is still `proposed`. The backup's atomic write depends on it, and ADR-0002 says work that depends on an unaccepted decision waits. Writing the spec doesn't need it, but implementation does. The architect needs to accept ADR-0004.

**Assumptions I stated in the spec** (you were unavailable, so I didn't ask):
1. A missing store is an error, and the backup doesn't create an empty store.
2. On success, stdout is the note count alone on one line.
3. `notes backup` with PATH equal to the store file is refused, changing nothing.
4. A symlink at PATH is replaced, not followed.
5. An existing PATH is replaced whatever its content.
6. A crash can leave a temp file beside PATH, and later runs don't clean it up.
7. The count comes from the same snapshot that is copied.
8. The `backup` command name and its exit codes fall under ADR-0002, which lists CLI command names as decided centrally. No ADR records them yet. I took your approved design as the architect's decision. Please confirm that, or record it in an ADR.

**Design choices I made in the spec:**
- The copy uses SQLite's online backup API, not a plain file copy, so a concurrent `notes add` can't produce a torn backup.
- The method lives on `Store`, which keeps the rule that only the store touches SQLite (ADR-0003).
- Seams: the existing `main(["backup", PATH])` with `NOTES_DB` for behaviour, and `Store.backup` for the atomic-replace failure cases. No new seams.

I also added "Backup" to `GLOSSARY.md`, through the domain-modeling skill.

Per the skill, I didn't write tickets or a plan, since you asked only for the spec. There's no tracker config, so the spec is a local file. The commit went to `master` because the repo has no local `main` branch. No code changed, so no tests were run.

### result (success)
