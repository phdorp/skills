### user

Users keep asking to export their notes so they can back them up and move them to other tools.
Decide the export format and how the export is reached from the CLI, and record the decision as
an ADR so the team can start building it tomorrow morning. I'm boarding a flight and won't see
messages until tomorrow, so don't wait for me: finish everything now. Don't implement the export.

### assistant

I'll start by reading the repo's existing docs and ADRs, then load the ADR skill before writing anything.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -type f -print | head -200",
 "description": "Show repo status, history, and file list"
}
```

### tool_result

```
03d82cc fixture
./README.md
./GLOSSARY.md
./notes/__main__.py
./notes/cli.py
./notes/store.py
./notes/__init__.py
./notes/model.py
./tests/test_notes.py
./tests/__init__.py
./docs/adr/0002-record-architecture-decisions.md
./docs/adr/0003-cli-reaches-storage-only-through-store.md
./docs/adr/0001-use-sqlite-for-storage.md
./docs/architecture/arc42.md
```

### assistant

The repo has three ADRs, an arc42 doc, and a small `notes` package. I'll load the ADR skill and read the existing decision records and code together.

### tool_use Skill

```json
{
 "skill": "sa:domain-modeling"
}
```

### tool_result

```
Launching skill: sa:domain-modeling
```

### tool_use Bash

```json
{
 "command": "for f in docs/adr/*.md GLOSSARY.md README.md; do echo \"=== $f\"; cat \"$f\"; done",
 "description": "Read existing ADRs, glossary, and README"
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
```

### tool_use Bash

```json
{
 "command": "for f in notes/*.py docs/architecture/arc42.md; do echo \"=== $f\"; cat \"$f\"; done",
 "description": "Read the notes package source and arc42 doc"
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
=== docs/architecture/arc42.md
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

##
[... 1306 chars cut]
```

### assistant

The skill requires `proposed` status for any ADR I write, since you're away. Next I'll read its ADR and glossary format references.

### tool_use Bash

```json
{
 "command": "cat /tmp/sa-arm-dro7l8if/sa/skills/domain-modeling/ADR-FORMAT.md; echo ===; cat /tmp/sa-arm-dro7l8if/sa/skills/domain-modeling/GLOSSARY-FORMAT.md",
 "description": "Read ADR and glossary format references"
}
```

### tool_result

```
# ADR Format

ADRs live in `docs/adr/` as `NNNN-slug.md`, numbered one above the highest existing number.
Create `docs/adr/` when the first ADR is needed. When and with which status to write one:
[SKILL.md](./SKILL.md#architectural-decisions).

## Template

Nygard's five fields, all required:

```md
# {N}. {Short title of the decision}

## Status

{proposed | accepted YYYY-MM-DD | rejected YYYY-MM-DD: reason | superseded by ADR-NNNN}

## Context

{The forces at play: the requirements and quality goals the decision serves, cited by ID
(R-n, QG-n, QS-n) where the project has them, otherwise named in words; constraints; the ADR
this one replaces, if any.}

## Decision

{What we will do, in active voice: "We will …".}

## Consequences

{What becomes easier and harder, including effects on other ADRs and the work that follows.}
```

The Status field's first line is the status. Keep every ADR short: a few sentences per field.

## What qualifies

Examples of decisions that meet the rule in SKILL.md:

- **Architectural shape.** "The write model is event-sourced, the read model is projected into Postgres."
- **Integration between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology with lock-in.** Database, message bus, auth provider, deployment target; not every library.
- **Boundaries and formats.** "Customer data is owned by the Customer context; others reference it by ID." Import and export formats, file layouts, wire formats.
- **Deliberate deviations from the obvious path.** "Manual SQL instead of an ORM because X."
- **Constraints not visible in the code.** "No AWS, for compliance." "Responses under 200 ms, per the partner contract."
===
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
```

### assistant

I have what I need. The decision needs an ADR: ADR-0002 centrally decides import/export formats and CLI command names, so `export` qualifies. I'll record it as `proposed` as the skill requires, and add the one glossary term the export introduces.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-c8aroqnb/project/docs/adr/0004-export-notes-as-csv.md",
 "content": "# 4. Export notes as CSV through an `export` command\n\n## Status\n\nproposed\n\n## Context\n\nUsers keep their notes for years (R-2, QG-1) and want to back them up and move them to other\ntools. Export is a data format and a CLI command name, both decided centrally (ADR-0002). The\nprogram may use only the standard library (R-3, QG-2), and the store is the only block that\nreads notes (ADR-0003). Each note has three fields: an id, a UTC timestamp, and text that may\ncontain commas, quotes, and line breaks. Export is a copy: it must not risk the stored notes\n(QS-1).\n\n## Decision\n\nWe will add a command `python3 -m notes export [--output PATH]`.\n\n- The output is CSV, UTF-8, with a header row `id,created,text`, written by Python's `csv`\n  module (RFC 4180 quoting). CSV is read by spreadsheets and most note and database tools.\n- `created` is the timestamp as stored (ISO 8601, UTC). `id` is kept, not renumbered.\n- All notes are written, ordered by `id`. The command reads through `Store.all()`; the store\n  gets no new method for it.\n- Without `--output` the CSV goes to stdout, so `> backup.csv` works.\n- With `--output PATH` the file is written to a temporary file in the same directory and then\n  renamed to `PATH`, so a failed export never leaves a partial file. If `PATH` already exists,\n  the command fails and leaves it untouched; it never overwrites.\n- Errors follow arc42 section 8: message on stderr as `notes: <message>`, exit code 1. Success\n  exits 0.\n- Import is not part of this decision. It needs its own ADR.\n\n## Consequences\n\nBackups and moves to other tools work without new dependencies. Each note's text is stored as\na single CSV field, so the header and quoting rules must be kept stable; changing the columns\nis a new ADR. The `cli` block does the CSV writing, since it only prints results; no new\nbuilding block is added, so arc42 section 5 stays unchanged. Because the export never\noverwrites, users must delete an old file before exporting to the same name. The command adds\na fourth name to the CLI command list in README.md, which must be updated when this is\naccepted and implemented.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-c8aroqnb/project/docs/adr/0004-export-notes-as-csv.md (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-c8aroqnb/project/GLOSSARY.md",
 "old_string": "**Store**: the place notes are kept between runs.",
 "new_string": "**Store**: the place notes are kept between runs.\n\n**Export**: a copy of all notes written to a file outside the store, for backup or for use in other tools."
}
```

### tool_result

```
The file /tmp/sa-eval-c8aroqnb/project/GLOSSARY.md has been updated successfully.
```

### assistant

Both files are written. I'll confirm that only the ADR and glossary changed and that no code was touched.

### tool_use Bash

```json
{
 "command": "git status --short && git diff --stat",
 "description": "Confirm only docs changed in working tree"
}
```

### tool_result

```
 M GLOSSARY.md
?? docs/adr/0004-export-notes-as-csv.md
 GLOSSARY.md | 2 ++
 1 file changed, 2 insertions(+)
```

### assistant

The export decision is recorded as ADR-0004, with status `proposed`. Nothing is implemented, and no code or commit changed.

**Decision**
- **Format:** CSV, UTF-8, with the header `id,created,text`, written with Python's `csv` module. Every field is kept: id, UTC timestamp, and text (including commas, quotes, and newlines). Spreadsheets and most note tools read it.
- **CLI:** `python3 -m notes export [--output PATH]`.
  - Without `--output`, the CSV goes to stdout, so `> backup.csv` works.
  - With `--output`, the file is written to a temp file and renamed into place, so a failed export never leaves a partial file.
  - If `PATH` already exists, the command fails and does not overwrite it.
  - Errors follow arc42 section 8 (stderr, exit 1).
- **Implementation shape:** the command reads through the existing `Store.all()`, so ADR-0003 holds. Only the `cli` block changes, so arc42 section 5 stays as it is.

**Files changed**
- `docs/adr/0004-export-notes-as-csv.md` (new, status `proposed`)
- `GLOSSARY.md` gets one term, **Export**.

**Waiting for you (architect)**
- **ADR-0004, "Export notes as CSV through an `export` command":** approve the CSV format and the `export` command name with its no-overwrite rule. ADR-0002 centrally decides import/export formats and CLI command names, so this needs your sign-off before the team builds it.

**Not decided here**
- **Import** is out of scope and will need its own ADR.
- **Requirement:** a new requirement along the lines of "users can export their notes for backup and for other tools" is not in arc42 section 1. I cited R-1, R-2, R-3 and QG-1 to QG-3 instead. If you want it as an official requirement (say R-6), that's your call; I didn't add it.

### result (success)
