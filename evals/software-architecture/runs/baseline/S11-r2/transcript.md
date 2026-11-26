### user

/sa:design-dialogue I want a `notes export DIR` command that writes every note as a Markdown file, so people can
open their notes in other editors. The exported files should be encrypted with a passphrase,
so a lost USB stick exposes nothing. Help me think this through before anything gets built.

### assistant

I'll read the project first so I know how notes are stored today before asking anything.

### tool_use Bash

```json
{
 "command": "git log --oneline | head -20 && echo --- && git ls-files | head -200 && echo --- && cat README* 2>/dev/null | head -150",
 "description": "Survey repo files, history, and README"
}
```

### tool_result

```
e370ee3 fixture
---
GLOSSARY.md
README.md
docs/adr/0001-use-sqlite-for-storage.md
docs/adr/0002-record-architecture-decisions.md
docs/adr/0003-cli-reaches-storage-only-through-store.md
docs/adr/0004-write-notes-atomically.md
docs/adr/0005-add-postgresql-backend.md
docs/architecture/arc42.md
notes/__init__.py
notes/__main__.py
notes/cli.py
notes/model.py
notes/store.py
tests/__init__.py
tests/test_notes.py
---
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
 "command": "grep -rniE \"notes|export|encrypt|passphrase|crypt\" --exclude-dir=.git . | head -100",
 "description": "Search repo for notes, export, and encryption references"
}
```

### tool_result

```
GLOSSARY.md:5:**Store**: the place notes are kept between runs.
notes/__init__.py:1:"""Keep short notes from the command line."""
notes/__main__.py:3:from notes.cli import main
notes/cli.py:4:from notes.store import Store, default_path
notes/cli.py:8:    parser = argparse.ArgumentParser(prog="notes", description="Keep short notes.")
notes/cli.py:11:    sub.add_parser("list", help="list all notes")
notes/cli.py:12:    sub.add_parser("search", help="find notes containing a term").add_argument("term")
notes/cli.py:17:        print(f"notes: {e}", file=sys.stderr)
docs/adr/0004-write-notes-atomically.md:1:# 4. Write notes atomically via a temporary file and rename
docs/adr/0004-write-notes-atomically.md:10:store writes besides the database (for example an export) must meet the same rule.
README.md:1:# notes
README.md:3:Keep short notes from the command line.
README.md:6:python3 -m notes add "Buy milk"
README.md:7:python3 -m notes list
README.md:8:python3 -m notes search milk
README.md:11:Notes are stored in `~/.notes.db` (set `NOTES_DB` to use another file). Run the tests with
docs/adr/0003-cli-reaches-storage-only-through-store.md:13:Only `notes/store.py` imports `sqlite3` or touches the database file. `notes/cli.py` uses the
docs/adr/0003-cli-reaches-storage-only-through-store.md:18:Any new command that reads or writes notes goes through `Store`.
tests/test_notes.py:9:from notes.cli import main
tests/test_notes.py:10:from notes.store import Store
tests/test_notes.py:33:        with mock.patch.dict(os.environ, {"NOTES_DB": str(db)}):
docs/adr/0001-use-sqlite-for-storage.md:9:Notes must survive crashes (R-2, QG-1, QS-1) and the program may use only the Python standard
docs/adr/0001-use-sqlite-for-storage.md:14:Store all notes in one SQLite database file, by default `~/.notes.db`.
notes/store.py:1:"""The only module that knows how notes are stored (ADR-0001, ADR-0003)."""
notes/store.py:7:from notes.model import Note
notes/store.py:11:    return Path(os.environ.get("NOTES_DB", Path.home() / ".notes.db"))
notes/store.py:17:        self._db.execute("CREATE TABLE IF NOT EXISTS notes "
notes/store.py:23:            cur = self._db.execute("INSERT INTO notes (text, created) VALUES (?, ?)",
notes/store.py:28:        rows = self._db.execute("SELECT id, text, created FROM notes ORDER BY id")
notes/store.py:32:        rows = self._db.execute("SELECT id, text, created FROM notes WHERE text LIKE ? ORDER BY id",
docs/adr/0002-record-architecture-decisions.md:21:- import and export formats;
docs/adr/0005-add-postgresql-backend.md:9:Users with many notes asked for faster search (R-1).
docs/adr/0005-add-postgresql-backend.md:13:Offer PostgreSQL as a second storage engine, chosen with `NOTES_BACKEND=postgres`.
docs/architecture/arc42.md:1:# notes: architecture
docs/architecture/arc42.md:11:| R-1 | Users add, list and search notes from the command line. | 1 | active | core use |
docs/architecture/arc42.md:12:| R-2 | No note is lost when the process or machine crashes. | 2 | active | users keep notes for years |
docs/architecture/arc42.md:14:| R-4 | Notes sync between a user's devices. | - | deferred | needs a server; revisit next year |
docs/architecture/arc42.md:30:| Users | keep notes for years without losing any |
docs/architecture/arc42.md:46:| `store` | keep notes between runs; the only block that knows the storage | `model` |
docs/architecture/arc42.md:55:- Errors: reported on stderr as `notes: <message>`, exit code 1.
docs/architecture/arc42.md:67:| QS-2 | QG-2 | a user runs `python3 -m notes list` | fresh Linux or macOS with Python 3.11+ | it works without installing anything | 0 install steps |
docs/architecture/arc42.md:68:| QS-3 | QG-3 | a contributor swaps the storage engine | development | only `notes/store.py` and its tests change | 0 other files changed |
```

### tool_use Bash

```json
{
 "command": "cat docs/architecture/arc42.md && echo ---ADR && cat docs/adr/0001*.md docs/adr/0002*.md docs/adr/0003*.md docs/adr/0004*.md docs/adr/0005*.md && echo ---GLOSS && cat GLOSSARY.md && echo ---CODE && cat notes/store.py notes/cli.py notes/model.py",
 "description": "Read architecture doc, ADRs, glossary, and core code"
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
---ADR
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
# 3. CLI reaches storage onl
[... 3799 chars cut]
```

### assistant

Your request has a conflict in it, and it's worth settling before anything else. Here is what I found and the one question I need answered.

You want `notes export DIR` to write each note as a Markdown file, encrypted with a passphrase, so a lost USB stick reveals nothing.

What the repo already says:
- Notes live in one SQLite file (ADR-0001) as an id, text, and created time. There is no edit or delete command yet.
- Export belongs in `Store` (ADR-0003). Any file the store writes must use a temp file, fsync, and rename (ADR-0004, still "proposed").

Two things your request runs into:
1. **Encryption conflicts with a stated constraint.** Requirement R-3 says standard library only. Python's standard library hashes but cannot encrypt files. Passphrase encryption needs a third-party package or an external tool such as `openssl` or `gpg`. Either choice needs an accepted ADR, because third-party dependencies and export formats are decided centrally (ADR-0002).
2. **Encrypted files cannot be opened directly in an editor.** So "open their notes in other editors" needs a decrypt step somewhere.

Also, "exposes nothing" is stronger than encryption alone delivers. File names, the note count, and file sizes stay visible unless you hide them.

Tell me if I have any of this wrong. The question that matters most: when someone wants to read a note in another editor, what should happen between the USB stick and that editor? The answer decides whether the passphrase only protects the stick, or whether the files are protected at all times.

### result (success)

### user

One Markdown file per note, the title as the heading, the date in a small header. The user
names the folder. I'm offline after this: lay out the ways to build it and recommend one. I'll
pick tomorrow.

### assistant

Got it: one Markdown file per note, the title as the heading, the date in a small header, and you name the folder. Two things are still open, and the approaches below depend on them.

**Gaps in what you've decided**
- Notes have no title field, only text. I'd use the first line of the note, cut at about 60 characters, as the title.
- Filenames aren't decided. Using the note id (`0007.md`) reveals only the count. Using the title reveals content in the names, which undercuts "exposes nothing."

**The open question**
Encrypted files can't be opened in another editor directly. You haven't said whether readers should decrypt first, or whether plain files on the stick are acceptable. The three approaches differ on exactly this.

**Approaches**

1. **Encrypt each note with a third-party package** (`cryptography`, key from scrypt, AES-GCM). Each file is `.md.enc`, and the passphrase is required to read it.
   - Fits your request fully.
   - Needs an accepted ADR, since it changes R-3 (standard library only) and adds a dependency.
   - Editors need a decrypt step, so you'd also need a `notes decrypt` command. That is scope you didn't ask for.
   - Import the package only inside `export`, so `list`, `add`, and `search` still need no install (QS-2).

2. **Encrypt by shelling out to `openssl` or `gpg`.** No Python dependency.
   - Still needs an ADR, because it adds an external binary.
   - Passphrase handling through a subprocess is fragile, and availability differs across machines (R-3's locked-down case).
   - Decrypt has the same editor problem as option 1.

3. **Write plain Markdown and let the stick do the encrypting.** You encrypt the USB volume yourself with VeraCrypt, LUKS, or an encrypted disk image.
   - Standard library only, no new ADR, editors open the files directly, and it is the least code.
   - The tool does not enforce encryption, and any file copied off the stick is plaintext.
   - It does not meet "encrypted with a passphrase" as you wrote it.

Writing our own cipher from `hashlib` is not on the list. Hand-rolled encryption isn't safe to ship.

**My recommendation: option 1**, with a lazy import and a `notes decrypt` command. It's the only option that gives you the passphrase guarantee in the tool, and it keeps the core commands install-free. If you want readers to open files without a decrypt step, the honest answer is option 3, because a passphrase-encrypted file can't be read that way.

**For tomorrow, I need from you:**
1. Option 1, 2, or 3. If 1 or 2, do you accept changing R-3 and writing the ADR?
2. Is `notes decrypt` in scope?
3. Filenames: by id (my pick), or by title?
4. If the target folder already has files: overwrite, skip, or refuse? I'd refuse by default and add a flag to overwrite.

Once you pick, I'll write the design doc and the builder check. Nothing gets built until you approve it.

### result (success)
