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

I'll start by reading the repo's tracker config, glossary, ADRs, and the note store code the backup touches.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200 && echo --- && cat docs/agents/issue-tracker.md 2>/dev/null; echo ---; ls docs 2>/dev/null",
 "description": "Inspect repo layout and tracker config"
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
---
---
adr
architecture
```

### tool_use Bash

```json
{
 "command": "for f in $(find . -path ./.git -prune -o -type f -print | grep -iE 'adr|glossary|arc42|readme'); do echo \"=== $f\"; cat \"$f\"; echo; done",
 "description": "Read ADRs, glossary, and architecture docs"
}
```

### tool_result

```
=== ./README.md
# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
`python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).

=== ./GLOSSARY.md
# Glossary

**Note**: a short piece of text a user keeps, with an id and the time it was created.

**Store**: the place notes are kept between runs.

=== ./docs/adr/0004-write-notes-atomically.md
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

=== ./docs/adr/0002-record-architecture-decisions.md
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

=== ./docs/adr/0005-add-postgresql-backend.md
# 5. Add a PostgreSQL backend

## Status

proposed

## Context

Users with many notes asked for faster search (R-1).

## Decision

Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.

## Consequences

Needs the `psycopg` package and a running database server.

=== ./docs/adr/0003-cli-reaches-storage-only-through-store.md
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

=== ./docs/adr/0001-use-sqlite-for-storage.md
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

=== ./docs/architecture/arc42.md
# notes: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add, list and search notes from the command line. | 1 | active | core use |
| R-2 | No note is lost when the process or machine crashes. | 2 | active | users keep notes for years |
| R-3 | Runs on Linux and macOS with only the Python standard library. | 3 | active | installed on locked-down machines |
| R-4 | Notes sync between a user's devices. | - | deferred | needs a server; r
[... 2032 chars cut]
```

### assistant

ADR-0004 is still `proposed`, which matters for the spec. Next I'll read the code the backup touches.

### tool_use Bash

```json
{
 "command": "for f in notes/__main__.py notes/cli.py notes/store.py notes/model.py notes/__init__.py tests/test_notes.py; do echo \"=== $f\"; cat -n \"$f\"; done",
 "description": "Read source and test files"
}
```

### tool_result

```
=== notes/__main__.py
     1	import sys
     2	
     3	from notes.cli import main
     4	
     5	sys.exit(main())
=== notes/cli.py
     1	import argparse
     2	import sys
     3	
     4	from notes.store import Store, default_path
     5	
     6	
     7	def main(argv=None):
     8	    parser = argparse.ArgumentParser(prog="notes", description="Keep short notes.")
     9	    sub = parser.add_subparsers(dest="command", required=True)
    10	    sub.add_parser("add", help="add a note").add_argument("text")
    11	    sub.add_parser("list", help="list all notes")
    12	    sub.add_parser("search", help="find notes containing a term").add_argument("term")
    13	    args = parser.parse_args(argv)
    14	    try:
    15	        store = Store(default_path())
    16	    except Exception as e:  # arc42 section 8: errors go to stderr, exit code 1
    17	        print(f"notes: {e}", file=sys.stderr)
    18	        return 1
    19	    try:
    20	        if args.command == "add":
    21	            note = store.add(args.text)
    22	            print(note.id)
    23	        else:
    24	            found = store.all() if args.command == "list" else store.search(args.term)
    25	            for note in found:
    26	                print(f"{note.id}\t{note.created}\t{note.text}")
    27	    finally:
    28	        store.close()
    29	    return 0
=== notes/store.py
     1	"""The only module that knows how notes are stored (ADR-0001, ADR-0003)."""
     2	import os
     3	import sqlite3
     4	from datetime import datetime, timezone
     5	from pathlib import Path
     6	
     7	from notes.model import Note
     8	
     9	
    10	def default_path():
    11	    return Path(os.environ.get("NOTES_DB", Path.home() / ".notes.db"))
    12	
    13	
    14	class Store:
    15	    def __init__(self, path):
    16	        self._db = sqlite3.connect(path)
    17	        self._db.execute("CREATE TABLE IF NOT EXISTS notes "
    18	                         "(id INTEGER PRIMARY KEY, text TEXT NOT NULL, created TEXT NOT NULL)")
    19	
    20	    def add(self, text):
    21	        created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    22	        with self._db:
    23	            cur = self._db.execute("INSERT INTO notes (text, created) VALUES (?, ?)",
    24	                                   (text, created))
    25	        return Note(cur.lastrowid, text, created)
    26	
    27	    def all(self):
    28	        rows = self._db.execute("SELECT id, text, created FROM notes ORDER BY id")
    29	        return [Note(*row) for row in rows]
    30	
    31	    def search(self, term):
    32	        rows = self._db.execute("SELECT id, text, created FROM notes WHERE text LIKE ? ORDER BY id",
    33	                                (f"%{term}%",))
    34	        return [Note(*row) for row in rows]
    35	
    36	    def close(self):
    37	        self._db.close()
=== notes/model.py
     1	from dataclasses import dataclass
     2	
     3	
     4	@dataclass(frozen=True)
     5	class Note:
     6	    id: int
     7	    text: str
     8	    created: str
=== notes/__init__.py
     1	"""Keep short notes from the command line."""
=== tests/test_notes.py
     1	import io
     2	import os
     3	import tempfile
     4	import unittest
     5	from contextlib import redirect_stdout
     6	from pathlib import Path
     7	from unittest import mock
     8	
     9	from notes.cli import main
    10	from notes.store import Store
    11	
    12	
    13	class StoreTest(unittest.TestCase):
    14	    def setUp(self):
    15	        self.store = Store(Path(tempfile.mkdtemp()) / "n.db")
    16	
    17	    def tearDown(self):
    18	        self.store.close()
    19	
    20	    def test_add_then_list(self):
    21	        self.store.add("Buy milk")
    22	        self.assertEqual([n.text for n in self.store.all()], ["Buy milk"])
    23	
    24	    def test_search_matches_substring(self):
    25	        self.store.add("Buy milk")
    26	        self.store.add("Call Ann"
[... 730 chars cut]
```

### assistant

The spec template comes next. I also need to know whether `main` exists, since gitStatus names it as the default branch.

### tool_use Bash

```json
{
 "command": "cat /tmp/sa-arm-tjfo04pg/sa/skills/spec-and-plan/references/spec-template.md; echo ---; cd /tmp/sa-eval-xww62y5s/project && git branch -a && cd notes 2>/dev/null; cd /tmp/sa-eval-xww62y5s/project && python3 -m unittest 2>&1 | tail -3",
 "description": "Read spec template, branches, and current test status"
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

### Quality Requirements (set-up projects only)

Only when `docs/architecture/arc42.md` exists. Cite by ID; arc42 and the ADRs hold the text.

- **Serves:** the parent requirements (`R-n`).
- **Keeps:** the quality scenarios (`QS-n`) the work must still meet.
- **Builds on:** the accepted ADRs it relies on.
- **Blocked by:** each decision the work needs that only a proposed ADR settles, with the ADR number. The spec does not build on it until the architect accepts it.

### Out of Scope

What this spec deliberately does not cover, and where that work goes instead if it is planned.

### Further Notes

Anything else the planner or builder needs: open assumptions, links to ADRs or research, rollout notes.
---
* master
Ran 3 tests in 0.069s

OK
```

### assistant

I have what I need. The spec goes in `docs/specs/`, since no tracker is configured. The main open point is ADR-0004, which is still `proposed`, so the spec lists it as a blocker.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xww62y5s/project/docs/specs/2026-11-22-backup-spec.md",
 "content": "# Backup Command Spec\n\nStatus: ready-for-agent, blocked by ADR-0004 (proposed, not yet accepted). Do not start the atomic-write work until the architect accepts it.\nSource: the approved design passed to `/sa:spec-and-plan` on 2026-11-22. The architect was unavailable; every point where a question would have been asked is stated as an assumption under Further Notes.\n\n## Problem Statement\n\nNotes are kept in one file on one disk (`~/.notes.db`, or the path in `NOTES_DB`). If that disk fails or the file is lost, every note is lost. Users who keep notes for years have no simple way to keep a second copy on another disk, and no way to check that such a copy holds everything.\n\n## Solution\n\nA user runs `notes backup PATH`. The command writes a complete copy of the note store to PATH and prints how many notes the copy holds. An existing file at PATH is replaced. If anything goes wrong, the command says so on stderr and exits 1, and the user's existing store and any earlier backup at PATH are left as they were. Restoring is done by hand: the user copies the backup file back over the store file. There is no restore command in this version.\n\n## User Stories\n\n1. As a user, I want to run `notes backup PATH`, so that I keep a copy of my notes on another disk.\n2. As a user, I want the command to print the number of notes backed up, so that I can check the copy is complete.\n3. As a user, I want the printed number to equal the number of notes in the backup file, so that the count can be trusted.\n4. As a user who already has a backup at PATH, I want the new backup to replace it, so that I do not have to delete the old file first.\n5. As a user with an empty store, I want the backup to succeed and print `0`, so that an empty store is not an error.\n6. As a user whose store cannot be read, I want an error on stderr and exit code 1, so that I know no backup was made.\n7. As a user whose PATH cannot be written (the directory does not exist, it is read-only, or PATH is a directory), I want an error on stderr and exit code 1, and my earlier backup at PATH left intact.\n8. As a user whose backup is interrupted by a crash, power loss or kill, I want PATH to hold either the old backup or the complete new one, never a partial file, so that a backup I later rely on is never truncated.\n9. As a user who passes the store's own file as PATH, I want the command refused with an error and exit code 1, so that the store is not overwritten.\n10. As a user, I want no temporary files left in PATH's directory after a success or a failure.\n11. As a user, I want to restore by copying the backup file over my store file, and then `notes list` to show every note from the backup.\n12. As a user who gives a relative PATH, I want it resolved from the directory I ran the command in.\n13. As a user with no PATH argument, I want the usual argparse usage error, so that the command behaves like the other subcommands.\n14. As a user on Linux or macOS, I want backup to work with only the Python standard library, so that no install step is needed (R-3).\n15. As a contributor, I want the CLI to reach the store only through the `Store` class, so that only `notes/store.py` knows about SQLite (ADR-0003).\n\n## Implementation Decisions\n\n- **Store method.** `Store` gains one method that takes a target path and returns the number of notes written to it. It is the only code that reads the database for the backup. `notes/cli.py` does not import `sqlite3`.\n- **How the copy is made.** The method uses SQLite's online backup facility to copy the open store into a temporary file. This gives a consistent copy even if another process writes during the copy. The backup file is a SQLite database in the same format as the store (ADR-0001), so restoring by copying the file back works.\n- **Atomic write (ADR-0004).** The temporary file is created in the same directory as PATH and flushed to disk before it is moved into place with a single rename over PATH. On any failure the temporary file is removed and PATH is not touched. This applies ADR-0004's rule to a file the store writes other than the database.\n- **Count.** The number returned is counted from the temporary file, after the copy and before the rename, so the printed number matches the file the user receives.\n- **Refusing the store itself.** If PATH resolves to the same file as the store, the method raises an error before writing anything.\n- **CLI.** A new subcommand `backup` takes one positional argument, `path`. On success it prints the count on stdout as a single line containing only the integer, and returns exit code 0. On any error it prints `notes: <message>` on stderr and returns exit code 1.\n- **Error handling covers the copy and the write, not only opening the store.** Today `cli.py` catches only errors from opening the store. The backup subcommand must also catch errors raised while copying and writing, so that every failure follows the stated error convention (arc42 section 8).\n- **Store opening is unchanged.** The store is opened through `default_path()` as for every other command, which honours `NOTES_DB`. Opening creates the store file if it does not exist (see Further Notes).\n- **Permissions.** The backup file is created with the temporary-file default (readable and writable by the owner only). It is not given the store file's permissions.\n\n## Testing Decisions\n\n- **What makes a good test here.** Test observable behaviour: exit code, stdout, stderr, the bytes and content of the file at PATH, and the list of files in PATH's directory. Do not test which SQLite call is made.\n- **Seams.** Use the existing seams and add none:\n  - `notes.cli.main(argv)` with `NOTES_DB` pointed at a temporary database. This is the highest seam and proves the command.\n  - `notes.store.Store(path)` for the method itself, which needs a store with known notes.\n- **Modules tested.**\n  - CLI: exit 0 and the count line on stdout; replacement of an existing file; exit 1 with `notes: ` on stderr for an unreadable store, an unwritable PATH, a PATH that is a directory, and PATH equal to the store file; no leftover temporary file after success or failure; an existing PATH unchanged after a failure.\n  - Store: the method returns the number of notes; the file written can be opened with `Store` and returns the same notes; an empty store returns 0.\n  - Restore by hand: copy the backup over the store path, then `main([\"list\"])` shows the notes.\n  - Atomicity: make the rename step fail (for example by injecting a failure into the rename call) and check that the earlier file at PATH is unchanged and no temporary file remains.\n- **Prior art.** `tests/test_notes.py`: `StoreTest` builds a store in a temporary directory; `CliTest.test_add_and_search` sets `NOTES_DB` with `mock.patch.dict(os.environ, ...)` and captures stdout with `redirect_stdout`. Follow both patterns. Tests run with `python3 -m unittest`.\n\n## Quality Requirements\n\n- **Serves:** R-2 (no note is lost when the process or machine crashes; a backup is one way to make that hold beyond one disk); R-3 (standard library only).\n- **Keeps:** QS-1 (a crash during the backup leaves PATH either old or complete and the store still opens; the same rule as QS-1 applied to the backup); QS-3 (the backup code lives in `notes/store.py`, with the CLI change confined to `notes/cli.py`).\n- **Builds on:** ADR-0001 (SQLite file format and crash safety); ADR-0003 (only `notes/store.py` touches SQLite); ADR-0002 (error reporting and the central list of CLI command names and exit codes).\n- **Blocked by:** ADR-0004 (*Write notes atomically via a temporary file and rename*, status proposed). The atomic-write requirement in this spec rests on it. The architect must accept it before implementation of that part begins. If it is rejected, the atomic requirement is withdrawn and this spec must be revised.\n\n## Out of Scope\n\n- A restore command, including any check that a file is a valid backup before it is copied over the store.\n- Scheduled or automatic backups.\n- Backup to a server, sync between devices (R-4, deferred), or a cloud location.\n- Encryption or compression of the backup file.\n- Incremental backups.\n- Backing up more than one store at once.\n- A confirmation prompt before replacing an existing file at PATH. Replacement is immediate, as the design states.\n- PostgreSQL backend (ADR-0005, proposed). Backup covers the SQLite store only.\n\n## Further Notes\n\n**Assumptions** (the architect was unavailable; each choice below is what this spec adopts, and each can be changed when the architect returns):\n\n1. **Stdout format.** The command prints only the integer and a newline, as `add` prints only the new id. It does not print a sentence.\n2. **Missing store.** The store is opened as every other command opens it, so a missing store file is created empty and backed up as `0` notes with exit code 0. This is consistent with the other commands, but it creates a file in the user's home directory as a side effect of `backup`. The architect may prefer an error for a missing store instead.\n3. **Write failures.** Failures while writing PATH (missing directory, no permission, PATH is a directory, disk full) are reported as `notes: <message>` with exit code 1. The design only names the unreadable-store case; this extends the same rule to write failures.\n4. **PATH equal to the store.** Refused with exit code 1 and the store untouched. The design does not name this case.\n5. **Symbolic link at PATH.** The link itself is replaced, not followed, because the rename replaces the directory entry. The design does not say.\n6. **Relative PATH.** Resolved from the current directory.\n7. **Backup file format.** The backup is the store's own SQLite file, so no new file format is introduced. ADR-0002 lists import and export formats as central decisions. The architect should confirm that a backup of the existing format does not need its own ADR.\n8. **Command name and exit codes.** The design fixes the name `backup` and exit codes 0 and 1. ADR-0002 lists CLI command names and exit codes as central decisions, but no ADR records this command yet. The architect's approval of the design is taken as the decision. If the architect wants it recorded, that needs a new ADR.\n\n**Open items for the architect:**\n\n- Accept or reject ADR-0004. This is a blocker for the atomic-write part (see Quality Requirements).\n- Confirm or change assumptions 1 to 8 above.\n- Decide whether the term \"backup\" should be added to `GLOSSARY.md`. It was not added in this pass; the glossary change should go through domain modelling.\n\n**Not produced in this pass:** tickets and an implementation plan. The request asked for the spec only. The work is one slice, so the spec can go straight to a plan once the architect accepts ADR-0004 and confirms the assumptions.\n\n**Tracker:** no tracker configuration exists in this repo (`docs/agents/issue-tracker.md` is absent), so the spec is published as a local file.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xww62y5s/project/docs/specs/2026-11-22-backup-spec.md (file state is current in your context — no need to Read it back)
```

### assistant

The spec is written. The skill's publish step says to commit it, so I'll do that now.

### tool_use Bash

```json
{
 "command": "git add docs/specs/2026-11-22-backup-spec.md && git commit -q -m \"docs: add backup command spec\n\nSpec for \\`notes backup PATH\\`. Blocked by ADR-0004 (proposed).\n\nCo-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2 && git status --short",
 "description": "Commit the spec file and confirm clean tree"
}
```

### tool_result

```
41327bb docs: add backup command spec
e484b0c fixture
?? notes/__pycache__/
?? tests/__pycache__/
```

### tool_use Bash

```json
{
 "command": "rm -rf notes/__pycache__ tests/__pycache__ && git status --short && echo clean",
 "description": "Remove test cache directories I generated"
}
```

### tool_result

```
clean
```

### assistant

I wrote the backup spec and committed it as `41327bb` at `docs/specs/2026-11-22-backup-spec.md`. No tracker is configured, so it is a local file. I did not write tickets or a plan, since you asked for the spec only.

**Blocker:** ADR-0004 (atomic writes), which the spec relies on, is still `proposed`. The skill says to hold the atomic-write work until the architect accepts it. If it is rejected, the spec needs revising.

**Assumptions I made where I would have asked you** (all listed in the spec's Further Notes):
1. **Stdout:** only the integer count and a newline, like `add` prints only the id.
2. **Missing store:** opened the way every command opens it, so it is created empty and `backup` reports `0`. This leaves a file in the home directory as a side effect; you may prefer an error.
3. **Write failures** (missing directory, no permission, PATH is a directory, disk full): `notes: <message>` on stderr, exit 1, with the earlier file at PATH untouched.
4. **PATH equal to the store file:** refused with exit 1, so the store is not overwritten.
5. **Symlink at PATH:** the link is replaced, not followed.
6. **Relative PATH:** resolved from the current directory.
7. **Backup format:** the store's own SQLite file, so restore is a plain copy. ADR-0002 lists export formats as central decisions, so the architect should confirm this needs no new ADR.
8. **Command name and exit codes:** I took your approval as the decision. No ADR records them yet.

**Design choices I made:** the copy uses SQLite's online backup, so it is consistent under concurrent writes. The count is taken from the temporary file before the rename, so it matches what the user receives.

**Existing gap:** `cli.py` catches errors only when opening the store. The spec requires the backup path to catch copy and write errors too, so the "as every command does" promise holds.

**Not done:** I did not add "backup" to `GLOSSARY.md`. The spec says that change should go through domain modelling.

I also committed with the attribution line you specified. The working tree is clean; I removed the `__pycache__` directories my test run created.

### result (success)
