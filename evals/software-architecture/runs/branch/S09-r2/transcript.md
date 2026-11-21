### user

/sa:setup-architecture Set up the architecture documentation for pantry. There is none yet: the code is all we have.
My requirements:
1. Users add pantry items with an expiry date and list what expires soon, from the command line.
2. No item is lost if the machine crashes mid-write.
3. Runs with only the Python standard library.
4. A new command touches only cli.py and at most one new module.

### assistant

I'll load the referenced skills and look at the project before writing anything.

### tool_use Skill

```json
{
 "skill": "sa:quality-requirements"
}
```

### tool_result

```
Launching skill: sa:quality-requirements
```

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

### tool_use Skill

```json
{
 "skill": "sa:add-requirements"
}
```

### tool_result

```
Launching skill: sa:add-requirements
```

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -20 && find . -path ./.git -prune -o -type f -print | head -200",
 "description": "Inspect project layout and git history"
}
```

### tool_result

```
2c4ab8a fixture
./README.md
./pantry/__main__.py
./pantry/dates.py
./pantry/cli.py
./pantry/store.py
./pantry/__init__.py
./pantry/model.py
./tests/test_pantry.py
./tests/__init__.py
```

### assistant

The skills are loaded. Next I'll read the project's code and the skill templates.

### tool_use Bash

```json
{
 "command": "for f in README.md pantry/__init__.py pantry/__main__.py pantry/cli.py pantry/store.py pantry/model.py pantry/dates.py tests/test_pantry.py; do echo \"=== $f\"; cat \"$f\"; done",
 "description": "Print README and all Python source and tests"
}
```

### tool_result

```
=== README.md
# pantry

A command-line tool that remembers what is in your pantry and tells you what expires soon.

```sh
python3 -m pantry add "Milk" 2026-11-25
python3 -m pantry add "Yoghurt" +3d
python3 -m pantry list --soon 7
python3 -m pantry remove "Milk"
```

Items are kept in `~/.pantry.jsonl` (override with `PANTRY_FILE`).

Run the tests with `python3 -m unittest`.
=== pantry/__init__.py
"""pantry: remember what is in the pantry and what expires soon."""
=== pantry/__main__.py
import sys

from pantry import cli

sys.exit(cli.main(sys.argv[1:]))
=== pantry/cli.py
"""Command line: add, list, remove. Exit 0 on success, 1 on a user error, 2 on bad usage."""
import argparse
import sys
from datetime import date, timedelta

from pantry import dates, store
from pantry.model import Item


def main(argv):
    ap = argparse.ArgumentParser(prog="pantry")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("name")
    a.add_argument("expires")
    ls = sub.add_parser("list")
    ls.add_argument("--soon", type=int, metavar="DAYS")
    r = sub.add_parser("remove")
    r.add_argument("name")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    if args.cmd == "add":
        try:
            expires = dates.parse(args.expires)
        except ValueError:
            print(f"pantry: not a date: {args.expires}", file=sys.stderr)
            return 1
        store.add(Item(args.name, expires))
    elif args.cmd == "remove":
        if args.name not in {i.name for i in store.items()}:
            print(f"pantry: no such item: {args.name}", file=sys.stderr)
            return 1
        store.remove(args.name)
    else:
        items = sorted(store.items(), key=lambda i: (i.expires, i.name.lower()))
        if args.soon is not None:
            limit = date.today() + timedelta(days=args.soon)
            items = [i for i in items if i.expires <= limit]
        for i in items:
            print(f"{i.expires.isoformat()}  {i.name}")
    return 0
=== pantry/store.py
"""The pantry file: one JSON record per line, only ever appended to."""
import json
import os
from pathlib import Path

from pantry import model


def path():
    return Path(os.environ.get("PANTRY_FILE", Path.home() / ".pantry.jsonl"))


def _append(record):
    with open(path(), "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
        f.flush()
        os.fsync(f.fileno())


def _records():
    p = path()
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            continue  # a line cut short by a crash
    return out


def add(item):
    _append(item.to_record())


def remove(name):
    _append(model.removal(name))


def items():
    return model.replay(_records())
=== pantry/model.py
"""An item in the pantry and the events that change the pantry."""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Item:
    name: str
    expires: date

    def to_record(self):
        return {"op": "add", "name": self.name, "expires": self.expires.isoformat()}


def removal(name):
    return {"op": "remove", "name": name}


def replay(records):
    """The items left after applying add and remove records in order."""
    items = {}
    for r in records:
        if r["op"] == "add":
            items[r["name"]] = Item(r["name"], date.fromisoformat(r["expires"]))
        elif r["op"] == "remove":
            items.pop(r["name"], None)
    return list(items.values())
=== pantry/dates.py
"""Dates as users type them: 2026-11-25, today, tomorrow, +3d, +2w."""
import re
from datetime import date, timedelta

RELATIVE = re.compile(r"^\+(\d+)([dw])$")


def parse(text, today=None):
    today = today or date.today()
    text = text.strip().lower()
    if text == "today":
        return t
[... 2660 chars cut]
```

### tool_use Bash

```json
{
 "command": "cd /tmp/sa-arm-kd2dzkey/sa/skills && ls -R setup-architecture quality-requirements domain-modeling add-requirements && cat setup-architecture/references/arc42-skeleton.md && echo ==== && cat setup-architecture/references/made-centrally-adr.md && echo ==== && cat quality-requirements/references/quality-scenario.md && echo ==== && cat quality-requirements/references/iso-25010.md && echo ==== && cat domain-modeling/ADR-FORMAT.md",
 "description": "Read skill reference templates for arc42 and ADRs"
}
```

### tool_result

```
add-requirements:
SKILL.md

domain-modeling:
ADR-FORMAT.md
GLOSSARY-FORMAT.md
SKILL.md
agents

domain-modeling/agents:
openai.yaml

quality-requirements:
SKILL.md
references

quality-requirements/references:
iso-25010.md
quality-scenario.md

setup-architecture:
SKILL.md
references

setup-architecture/references:
arc42-skeleton.md
made-centrally-adr.md
recovery.md
# arc42 skeleton

Write `docs/architecture/arc42.md` with these twelve sections, in this order, each as a level-2
heading `## <n>. <name>`. The section names and one-line purposes are our own wording of the
arc42 template; for its full explanations and examples see [arc42.org](https://arc42.org) and
[docs.arc42.org](https://docs.arc42.org) (link, do not copy). Leave a section empty until there
is something to write: the document grows with the project.

```markdown
# <project>: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals
## 2. Constraints
## 3. Context and scope
## 4. Solution strategy
## 5. Building block view
## 6. Runtime view
## 7. Deployment view
## 8. Crosscutting concepts
## 9. Architecture decisions
## 10. Quality requirements
## 11. Risks and technical debt
## 12. Glossary
```

| section | holds |
|---|---|
| 1. Introduction and goals | `### Requirements overview` (the R-list), `### Quality goals`, `### Stakeholders`; tables as in `quality-requirements` › Where they live |
| 2. Constraints | what the architect cannot change: platforms, licences, mandated technology |
| 3. Context and scope | the system boundary and everything outside it the system talks to |
| 4. Solution strategy | the few fundamental ideas the solution rests on, each traced to a goal |
| 5. Building block view | the table `\| block \| responsibility \| may use \|`: the parts of the system, what each is responsible for, and which other blocks it may use |
| 6. Runtime view | how the parts work together in the scenarios that matter |
| 7. Deployment view | where it runs and how it gets there |
| 8. Crosscutting concepts | rules every part follows: naming, units, error handling, logging |
| 9. Architecture decisions | one sentence saying where the ADRs are, linked relative to this file (`../adr/` for `docs/adr/`), and a link to the "Record architecture decisions" ADR |
| 10. Quality requirements | the quality scenario table (`quality-requirements` › references/quality-scenario.md) |
| 11. Risks and technical debt | known risks and debt, each with what it threatens |
| 12. Glossary | a link to `GLOSSARY.md`; without one, the line "`GLOSSARY.md` is created with the first resolved term." |

## Existing documents

In a project that already documents its architecture, each section whose content lives in
another document (a README section, a wiki page, a design doc) gets one line linking it, such
as "See README › How it works", linked as `../../README.md#how-it-works`. That document stays where
and as it is; the arc42 file holds the link, never a copy of its content. A section whose
content lives nowhere yet starts empty, as in a fresh project.

## At setup

At setup, sections 1, 5 and 10 get their empty tables and sections 9 and 12 their links in the
first turn. Rows follow once the architect confirms; section 5's rows follow once building
blocks are decided.
====
# "Record architecture decisions" ADR

The ADR that draws the line between decisions the architect makes centrally and decisions left
to whoever builds a block. It takes the next free number in the project's ADR directory (0001 in a
fresh project); skills find it by its title, never by its number. Format and status rules: `domain-modeling`.

```markdown
# <n>. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. <One sentence on
what this product needs from that line, citing the R- and QG-IDs it serves, e.g. "Sightings
must survive crashes (R-2, QG-1) and work 
[... 8126 chars cut]
```

### assistant

The project has source and tests but no architecture documentation: the README covers usage only. So this is the **undocumented** situation. This turn writes only the arc42 skeleton, then sends the proposal and waits for the architect.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md",
 "content": "# pantry: architecture\n\nStructured after the arc42 template (https://arc42.org). Empty sections are filled when needed.\n\n## 1. Introduction and goals\n\n### Requirements overview\n\n| ID | requirement | rank | status | reason |\n|---|---|---|---|---|\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n\n### Stakeholders\n\n## 2. Constraints\n\n## 3. Context and scope\n\n## 4. Solution strategy\n\n## 5. Building block view\n\n| block | responsibility | may use |\n|---|---|---|\n\n## 6. Runtime view\n\n## 7. Deployment view\n\n## 8. Crosscutting concepts\n\n## 9. Architecture decisions\n\nADRs live in `docs/adr/`. The ADR \"Record architecture decisions\" is drafted after the architect confirms the proposal; it is not yet written.\n\n## 10. Quality requirements\n\n| ID | goal | stimulus | environment | response | measure |\n|---|---|---|---|---|---|\n\n## 11. Risks and technical debt\n\n## 12. Glossary\n\n`GLOSSARY.md` is created with the first resolved term.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md (file state is current in your context — no need to Read it back)
```

### assistant

I wrote the skeleton at `docs/architecture/arc42.md`. It is the only file I changed. The project has code and tests but no architecture documentation (the README covers usage only), so this is the undocumented case. Nothing else is written yet, and no requirement, goal or ADR is recorded until you confirm it.

## Triage (proposal)

The R-list is empty, so there are no duplicates. Your four requirements don't conflict with each other, and no constraints or ADRs exist yet to check against. They are numbered R-1 to R-4 in your order; IDs are assigned on your confirmation.

| # | Requirement | Proposed outcome | Reason |
|---|---|---|---|
| R-1 | Add items with an expiry date; list what expires soon, from the CLI | system-level | It is the product's purpose and fixes the storage and CLI shape. |
| R-2 | No item lost if the machine crashes mid-write | system-level | It decides how every write is made durable. |
| R-3 | Standard library only | system-level (or section 2 constraint, your choice) | It limits every block's dependencies. It is a fixed limit, so you may prefer to record it as a constraint. |
| R-4 | A new command touches only `cli.py` and at most one new module | system-level | It sets the module structure and the dependency rule. |

**Tension to watch:** a future command that changes stored data (say, `edit`) would touch `store.py` or `model.py` unless the store API is generic. That conflicts with R-4 only if such a command is planned.

## Rank (proposed)

1. R-2: losing data is the worst failure.
2. R-1: the core function.
3. R-3: a hard limit that shapes everything else.
4. R-4: a change-scope rule.

**Tie-breakers to answer:**
- If only one of R-2 and R-4 can be fully met, which?
- If only one of R-1 and R-3 can be fully met, which?

## Quality goals (candidates)

| Candidate | From | Proposed measure | Question |
|---|---|---|---|
| QG-1 Reliability: recoverability | R-2 | 0 acknowledged items lost in 100 SIGKILL trials during `add` | Is this the right measure? |
| QG-2 Maintainability: modifiability | R-4 | a new command's diff touches only `cli.py` and at most one new module | Is this the right measure? |
| QG-3 Flexibility: installability | R-3 | 0 non-standard-library imports; runs on a fresh Python 3 with no install step | What is the minimum Python version? The code uses `dataclasses` and `date.fromisoformat`, so 3.7 or later. |
| QG-4 Functional suitability: functional correctness | R-1 | every item expiring within N days is listed, none later, sorted by expiry | Is this the right measure? |

Please confirm and rank the top three to five.

**Observed in the code (as found, unconfirmed):** the reader skips any unparseable line, not only a torn last line. So corruption in the middle of the file would be silent. This bears on R-2 and is an open question for you, not a finding I have recorded.

## Gap questions (each asked once)

- **Security: confidentiality.** Did you leave out protecting the pantry file from other users on the machine?
- **Performance efficiency: time behaviour.** Did you leave out list speed for a file with many years of items?
- **Compatibility: interoperability.** Did you leave out importing or exporting the pantry, for example as CSV?
- **Interaction capability: user error protection.** Did you leave out guarding against mistakes, such as confirming before `remove`?

Also missing: stakeholders (section 1) and constraints (section 2). Who uses this, and are there any other fixed limits?

## Decisions made centrally (draft ADR 0001)

The "Record architecture decisions" ADR would be `docs/adr/0001-record-architecture-decisions.md`, since no ADR directory exists. Its draft list:

- **Storage:** a per-user JSON Lines file (`~/.pantry.jsonl`, overridable with `PANTRY_FILE`), append-only add and remove records, replayed on read.
- **Record format:** `{"op", "name", "expires"}` with ISO dates.
- **Date input:** ISO dates, `today`, `tomorrow`, `+Nd`, `+Nw`.
- **CLI interface:** commands `add`, `list --soon`, `remove`; exit codes 0 success, 1 user error, 2 bad usage.
- **Dependency rule:** `cli` may use `store`, `model` and `dates`; `store` may use `model`; `model` and `dates` use nothing internal.
- **Crash safety:** fsync after each append; the reader skips unparseable lines.
- **Error handling:** user errors to stderr.
- **Third-party dependencies:** none; standard library only.

Left to the building blocks: test layout and helpers inside a module.

Legacy ADRs: none. Existing documents: none. The README has no architecture section, so arc42 links nothing.

## What I need from you

1. Confirm or change the triage and the outcome for each requirement.
2. Set the rank and answer the two tie-breakers.
3. Confirm or change QG-1 to QG-4 and their measures.
4. Answer the four gap questions, and give the stakeholders, constraints and minimum Python version.
5. Confirm or change the draft ADR 0001 list.

Once you confirm, I write the R-list, the goals, and the ADR as `proposed`. The ADR's status changes only when you approve its text. Recovering the architecture from the code waits for that approval.

### result (success)

### user

Confirmed as proposed: your triage, your ranking, the quality goals (except any without a
measure: keep those open) and your list of decisions made centrally. To your "did you leave
out" questions: no, nothing is missing. Write it down.

### assistant

Confirmed. I'll write the R-list, the four goals with their scenarios, the decided-out-of-scope answers, and the draft ADR. The ADR stays `proposed` until you approve its text.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md",
 "old_string": "| ID | requirement | rank | status | reason |\n|---|---|---|---|---|\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n\n### Stakeholders",
 "new_string": "| ID | requirement | rank | status | reason |\n|---|---|---|---|---|\n| R-1 | Users add pantry items with an expiry date and list what expires soon, from the command line. | 2 | active | It is the product's purpose and fixes the storage and CLI shape. |\n| R-2 | No item is lost if the machine crashes mid-write. | 1 | active | It decides how every write is made durable. |\n| R-3 | Runs with only the Python standard library. | 3 | active | It limits every block's dependencies. |\n| R-4 | A new command touches only cli.py and at most one new module. | 4 | active | It sets the module structure and the dependency rule. |\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n| QG-1 | Reliability: recoverability | R-2 | QS-1 |\n| QG-2 | Maintainability: modifiability | R-4 | QS-2 |\n| QG-3 | Flexibility: installability | R-3 | QS-3 |\n| QG-4 | Functional suitability: functional correctness | R-1 | QS-4 |\n\n### Stakeholders"
}
```

### tool_result

```
The file /tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md",
 "old_string": "## 3. Context and scope\n\n## 4. Solution strategy",
 "new_string": "## 3. Context and scope\n\n### Out of scope\n\nConfirmed by the architect as not wanted:\n\n- protecting the pantry file from other users on the machine (confidentiality);\n- list speed for large files (time behaviour);\n- importing or exporting the pantry, such as to CSV (interoperability);\n- interactive confirmation before `remove` (user error protection); errors are reported with exit codes and messages only.\n\n## 4. Solution strategy"
}
```

### tool_result

```
The file /tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md",
 "old_string": "ADRs live in `docs/adr/`. The ADR \"Record architecture decisions\" is drafted after the architect confirms the proposal; it is not yet written.\n\n## 10. Quality requirements\n\n| ID | goal | stimulus | environment | response | measure |\n|---|---|---|---|---|---|",
 "new_string": "ADRs live in [`../adr/`](../adr/). The ADR [Record architecture decisions](../adr/0001-record-architecture-decisions.md) is `proposed` and waits for the architect's approval of its text.\n\n## 10. Quality requirements\n\n| ID | goal | stimulus | environment | response | measure |\n|---|---|---|---|---|---|\n| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the interrupted item is either fully stored or absent; items stored before the crash stay readable | 0 acknowledged items lost in 100 SIGKILL trials during `add` |\n| QS-2 | QG-2 | a new command is added to the CLI | normal operation | the change touches `cli.py` and at most one new module | a new command's diff touches only `cli.py` and at most one new module |\n| QS-3 | QG-3 | the tool is run on a fresh Python 3 install with no pip | normal operation | the tool runs with no install step | 0 non-standard-library imports |\n| QS-4 | QG-4 | `list --soon DAYS` is run against items with mixed expiry dates | normal operation | every item expiring within DAYS is listed, none later, sorted by expiry | every item expiring within N days is listed, none later, sorted by expiry |"
}
```

### tool_result

```
The file /tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/sa-eval-xd_cdktr/project/docs/adr",
 "description": "Create the ADR directory"
}
```

### tool_result

```
(Bash completed with no output)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0001-record-architecture-decisions.md",
 "content": "# 1. Record architecture decisions\n\n## Status\n\nproposed\n\n## Context\n\nThe architect decides the architecture; contributors and agents build it. Pantry must not lose an item when the machine crashes mid-write (R-2, QG-1), must run with only the Python standard library (R-3, QG-3), and must keep a new command within `cli.py` plus at most one new module (R-4, QG-2). Storage and the CLI interface are shared by all of these, so they need one decision each (R-1, QG-4).\n\n## Decision\n\nWe record architecture decisions as ADRs in `docs/adr/`, in Nygard form.\n\nDecided centrally (needs an ADR the architect accepts):\n\n- Storage: a per-user JSON Lines file, `~/.pantry.jsonl` (overridable with `PANTRY_FILE`), holding append-only add and remove records that are replayed on read.\n- Record format: `{\"op\", \"name\", \"expires\"}`, with `expires` as an ISO date.\n- Date input: ISO dates, `today`, `tomorrow`, `+Nd`, `+Nw`.\n- CLI interface: commands `add`, `list --soon DAYS`, `remove`; exit codes 0 for success, 1 for a user error, 2 for bad usage.\n- Dependency rule: `cli` may use `store`, `model` and `dates`; `store` may use `model`; `model` and `dates` use no other block.\n- Crash safety: each append is flushed and fsynced; a line that does not parse is skipped on read.\n- Error handling: user errors are reported on stderr with a message naming the input.\n- Third-party dependencies: none; standard library only.\n\nLeft to the building blocks (no ADR):\n\n- Test layout and helper functions inside a module.\n\n## Consequences\n\nWork that depends on a decision on the list waits until this ADR is accepted. A change to storage, the record format or the CLI interface is a new ADR.\n\nBecause a line that does not parse is skipped without a warning, a corrupt record in the middle of the file loses its item silently. Changing that is a new ADR.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/adr/0001-record-architecture-decisions.md (file state is current in your context — no need to Read it back)
```

### assistant

The architecture skeleton is filled in from your confirmed answers. Four files were written in `/tmp/sa-eval-xd_cdktr/project`:

- **`docs/architecture/arc42.md`**: the R-list, the quality goals and scenarios, and the gap answers. Details below.
- **`docs/adr/0001-record-architecture-decisions.md`**: new, status `proposed`.
- Nothing is committed.

**R-list (section 1)**, ranked as you confirmed:

| Rank | ID | Requirement |
|---|---|---|
| 1 | R-2 | No item is lost if the machine crashes mid-write. |
| 2 | R-1 | Add items with an expiry date and list what expires soon, from the CLI. |
| 3 | R-3 | Runs with only the Python standard library. |
| 4 | R-4 | A new command touches only `cli.py` and at most one new module. |

**Quality goals and scenarios (sections 1 and 10)**: all four goals had measures, so none stay open.

- **QG-1** Reliability: recoverability (from R-2), QS-1: 0 acknowledged items lost in 100 SIGKILL trials during `add`.
- **QG-2** Maintainability: modifiability (from R-4), QS-2: a new command's diff touches only `cli.py` and at most one new module.
- **QG-3** Flexibility: installability (from R-3), QS-3: 0 non-standard-library imports.
- **QG-4** Functional suitability: functional correctness (from R-1), QS-4: every item expiring within N days is listed, none later, sorted by expiry.

**Gap answers (section 3, "Out of scope")**: confidentiality of the file, list speed for large files, import/export, and interactive confirmation before `remove` are recorded as not wanted.

**ADR 0001** lists the decisions made centrally: storage as a JSON Lines file, the record format, date input forms, the CLI and exit codes, the dependency rule, crash safety by fsync with skipping of unparseable lines, error reporting on stderr, and no third-party dependencies. Its status is `proposed` until you approve its text. Section 9 links to it.

**Still open for you:**
- **Goal order:** you didn't rank the goals. QG-1 to QG-4 follow the order listed above.
- **Stakeholders and constraints:** sections 1 and 2 are empty; you didn't answer these.
- **Minimum Python version:** the code needs 3.7 or later (`dataclasses`, `date.fromisoformat`), but you haven't confirmed a floor. QG-3 doesn't depend on it.
- **Silent corruption:** I didn't reopen the crash-safety decision. The ADR records the consequence: a corrupt record in the middle of the file is skipped silently.

**Next:** approve or change ADR 0001's text. Only after that do I recover the architecture from the code into sections 2 to 8 and 11. Its report replaces section 4.

### result (success)

### user

I approve the "Record architecture decisions" ADR as written. Now recover the rest of the
architecture from the code. I'm offline after this, so finish without asking me again.

### assistant

I'll read the recovery procedure first.

### tool_use Read

```json
{
 "file_path": "/tmp/sa-arm-kd2dzkey/sa/skills/setup-architecture/references/recovery.md"
}
```

### tool_result

```
1	# Recovery: an undocumented project after the list is approved
2	
3	Recovery turns code into a draft of its as-is architecture for the architect to review. It
4	starts in the turn in which the architect approves the "Record architecture decisions" ADR,
5	because that ADR's list decides which findings become ADRs. Everything you write is *found*,
6	not *decided*: the architect decides it by confirming it, section by section and ADR by ADR.
7	
8	## 1. Accept the approved ADR
9	
10	Mark the "Record architecture decisions" ADR `accepted YYYY-MM-DD` with today's date, as
11	`domain-modeling` describes. Its text stays exactly as the architect approved it; a decision you
12	would add to its list goes into your report as a proposal.
13	
14	Done when its Status is the only line that changed.
15	
16	## 2. Read the code
17	
18	List what the code shows: its modules or blocks, what each one uses, its entry points, its
19	storage and data formats, its dependencies, its conventions (errors, units, naming). For
20	dataflow code (Modelica, Simulink, signal graphs) read it in its own terms with
21	`codebase-design` › Paradigms: blocks, signals and connectors as their interfaces, and coupling
22	through connections and shared parameters or constants.
23	
24	Done when every source file belongs to a block you can name, with what it uses.
25	
26	## 3. Fill arc42 with what you found
27	
28	Fill sections 2–8 and 11 of `docs/architecture/arc42.md` with what the code shows. Section 5
29	gets one row per block in its table. For dataflow code, the table is
30	`| block | responsibility | in | out | may use |`: `in` and `out` name the block's input and
31	output connectors or signals, and a shared parameter or constant two blocks read is a row's
32	`may use` entry and a sentence under the table. Start each section you fill with the line:
33	
34	```markdown
35	*As found, unconfirmed.*
36	```
37	
38	The marker stays until the architect confirms that section. A section the code says nothing
39	about stays empty. Sections 1, 9, 10 and 12 hold what the architect confirmed and carry no marker.
40	
41	Done when every section you filled starts with the marker.
42	
43	## 4. Propose ADRs for listed decisions
44	
45	For each decision on the accepted list that the code has already made, write one ADR in the
46	project's ADR directory, next free number, status `proposed`. Its Context says the decision was
47	found in the code, names where, and cites the R- and QG-IDs it serves; its Decision states what
48	the code does. A decision off the list (an algorithm inside one block, a helper, a test layout,
49	the form of an equation) goes into arc42 only.
50	
51	Done when each listed decision the code made has exactly one proposed ADR, and no ADR covers an
52	off-list decision.
53	
54	## 5. Leave the code as it is
55	
56	Recovery documents the code; it changes no file outside the documentation. What looks wrong (a
57	race, a hidden coupling, a missing check) goes into section 11 as a risk, for the architect to
58	decide on later.
59	
60	Done when `git status` shows changes only under `docs/` (and `GLOSSARY.md`).
61	
62	## 6. Report
63	
64	End with:
65	
66	- the sections marked *as found, unconfirmed*, in the order the architect should review them,
67	  each with one line on what it claims;
68	- the proposed ADRs, each with the question it asks the architect ("keep the append-only file?");
69	- the risks you put in section 11.
70	
71	Done when the architect can confirm or correct each section and approve or reject each ADR from
72	your message.
73	
```

### assistant

The procedure starts by marking ADR 0001 accepted. Before I document the storage code, I want to test one suspicion: the crash-recovery test writes a torn line without a trailing newline, and the next `add` may append onto that partial line. I'll check it in a scratch file outside the repo.

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/pantry-probe && cd /tmp/sa-eval-xd_cdktr/project && PANTRY_FILE=/tmp/pantry-probe/p.jsonl python3 -c '\nfrom datetime import date\nfrom pantry import store\nfrom pantry.model import Item\nstore.add(Item(\"Rice\", date(2027,6,1)))\nwith open(store.path(), \"a\") as f:\n    f.write(\"{\\\"op\\\": \\\"add\\\", \\\"na\")   # torn write: crash mid-line, no newline\nstore.add(Item(\"Milk\", date(2026,11,25)))  # acknowledged after the crash\nprint(\"items:\", [i.name for i in store.items()])\nprint(\"raw:\", repr(open(store.path()).read()))\n'; PANTRY_FILE=/tmp/pantry-probe/p.jsonl python3 -c 'print()' >/dev/null; rm -rf /tmp/pantry-probe",
 "description": "Probe torn-line then append behaviour in scratch file"
}
```

### tool_result

```
items: ['Rice']
raw: '{"op": "add", "name": "Rice", "expires": "2027-06-01"}\n{"op": "add", "na{"op": "add", "name": "Milk", "expires": "2026-11-25"}\n'
```

### assistant

Confirmed: after a torn write, the next `add` is glued onto the partial line, so the acknowledged item "Milk" disappears on read. This matters for R-2 and QS-1. Recovery documents code and doesn't change it, so I'll record it as a risk. Next I'll accept ADR 0001 and write the arc42 sections.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0001-record-architecture-decisions.md",
 "old_string": "## Status\n\nproposed",
 "new_string": "## Status\n\naccepted 2026-11-21"
}
```

### tool_result

```
The file /tmp/sa-eval-xd_cdktr/project/docs/adr/0001-record-architecture-decisions.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md",
 "old_string": "ADRs live in [`../adr/`](../adr/). The ADR [Record architecture decisions](../adr/0001-record-architecture-decisions.md) is `proposed` and waits for the architect's approval of its text.",
 "new_string": "ADRs live in [`../adr/`](../adr/). The ADR [Record architecture decisions](../adr/0001-record-architecture-decisions.md) is `accepted`. The as-found decisions are proposed in ADR 0002 to 0009, each waiting for the architect's approval."
}
```

### tool_result

```
The file /tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md has been updated successfully.
```

### assistant

Next I'll write sections 2 to 8 and 11, each marked *as found, unconfirmed*, and the eight proposed ADRs for the decisions on the list that the code already makes.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md",
 "old_string": "## 2. Constraints\n\n## 3. Context and scope\n\n### Out of scope",
 "new_string": "## 2. Constraints\n\n*As found, unconfirmed.*\n\n- Standard library only: no package outside the standard library is imported anywhere in `pantry/` or `tests/`.\n- Python 3: the code uses `dataclasses` and `date.fromisoformat`, so 3.7 or later. The minimum version is not confirmed.\n- Data lives under the user's home directory (`~/.pantry.jsonl`), overridable with `PANTRY_FILE`.\n\n## 3. Context and scope\n\n*As found, unconfirmed.*\n\nThe pantry command, run from a terminal. Outside it: the file at `store.path()` (`PANTRY_FILE`, or `~/.pantry.jsonl`), the system clock (`date.today()`), and the command line, stdout and stderr. The system makes no network calls.\n\nThe \"Out of scope\" subsection below is the architect's answer and carries no marker.\n\n### Out of scope"
}
```

### tool_result

```
The file /tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md has been updated successfully.
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md",
 "old_string": "## 4. Solution strategy\n\n## 5. Building block view\n\n| block | responsibility | may use |\n|---|---|---|\n\n## 6. Runtime view\n\n## 7. Deployment view\n\n## 8. Crosscutting concepts\n\n## 9. Architecture decisions",
 "new_string": "## 4. Solution strategy\n\n*As found, unconfirmed.*\n\n- **Append-only event log.** Each add and remove is one appended line; the current pantry is the replay of the log (`model.replay`). Serves QG-1: no in-place rewrite that a crash could corrupt.\n- **Flush and fsync each append** before the command returns (`store._append`). Serves QG-1.\n- **One plain file, no database, standard library only.** Serves QG-3.\n- **Dates are parsed once, at input,** and stored as absolute ISO dates. Serves QG-4.\n\n## 5. Building block view\n\n*As found, unconfirmed.*\n\n| block | responsibility | may use |\n|---|---|---|\n| `pantry/__main__.py` | entry point for `python3 -m pantry`; passes argv to `cli.main` and exits with its result | `cli` |\n| `pantry/cli.py` | parses commands and flags, prints results, maps errors to exit codes | `dates`, `store`, `model` |\n| `pantry/store.py` | reads and appends the pantry file; skips lines that do not parse; exposes `add`, `remove`, `items` | `model` |\n| `pantry/model.py` | the `Item` type, the record format, and replay of records into current items | standard library only |\n| `pantry/dates.py` | parses date input: ISO dates, `today`, `tomorrow`, `+Nd`, `+Nw` | standard library only |\n\n`tests/test_pantry.py` exercises these blocks through their functions. It is not a building block.\n\n## 6. Runtime view\n\n*As found, unconfirmed.*\n\n- **`add NAME EXPIRES`:** `cli` parses `EXPIRES` with `dates.parse`; on failure it prints to stderr and exits 1. Otherwise `store.add` appends an add record, flushed and fsynced, and the command exits 0.\n- **`remove NAME`:** `cli` checks `NAME` against `store.items()`; if absent, it prints to stderr and exits 1. Otherwise `store.remove` appends a remove record.\n- **`list [--soon DAYS]`:** `store.items()` replays the whole file. `cli` sorts by expiry, then name case-insensitively, keeps items expiring on or before today plus `DAYS` if given, and prints `ISO-DATE  NAME` per line.\n\n## 7. Deployment view\n\n*As found, unconfirmed.*\n\nRun from the source tree as `python3 -m pantry`. The repository has no packaging file (no `setup.py` or `pyproject.toml`). Tests run with `python3 -m unittest`. Data is on the local disk of the machine, at the path in section 3.\n\n## 8. Crosscutting concepts\n\n*As found, unconfirmed.*\n\n- **Errors:** user errors print `pantry: <message>` to stderr and exit 1. Bad usage exits 2 with the argparse message on stderr.\n- **Durability:** each append is flushed and fsynced. The directory is not fsynced (section 11).\n- **Records:** one JSON object per line, with keys `op`, `name` and `expires`. Dates are ISO calendar dates with no time or zone.\n- **Dates:** the local calendar date from `date.today()`. Relative input is resolved when the item is added and stored as an absolute date.\n- **Names:** item names are exact strings. `remove` and replay match them case-sensitively; `list` sorts them case-insensitively.\n- **Naming:** lowercase module names; `Item` for the item class; `to_record`, `removal` and `replay` in `model`.\n\n## 9. Architecture decisions"
}
```

### tool_result

```
The file /tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md has been updated successfully.
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md",
 "old_string": "## 11. Risks and technical debt\n\n## 12. Glossary",
 "new_string": "## 11. Risks and technical debt\n\n*As found, unconfirmed.*\n\n1. **A new record is glued onto a partial line (verified).** After a crash leaves a partial line with no newline, the next `add` appends onto it. Both records end up on one line, and the new item is lost on read. Threatens R-2 and QS-1. A probe confirmed it: an item acknowledged after a torn write was missing from `store.items()`.\n2. **Corrupt lines in the middle of the file are skipped silently** (`store._records`). Threatens R-2. The architect has already accepted this in ADR 0001's consequences; it is listed here for review.\n3. **A record that is valid JSON but lacks a key raises an error on read** (`model.replay`), so every `list` and `remove` fails until the file is repaired. Threatens R-1. Found by reading; not run.\n4. **The directory is not fsynced when the file is created.** A crash just after the first add may lose the file's directory entry. Threatens R-2. Found by reading; not run.\n5. **Nothing guards against two processes appending at once.** Threatens R-2. Found by reading; not run.\n6. **Technical debt: no compaction.** The file grows with every add and remove, and every command reads all of it. The architect has said list speed is out of scope, so this is debt, not a goal.\n\n## 12. Glossary"
}
```

### tool_result

```
The file /tmp/sa-eval-xd_cdktr/project/docs/architecture/arc42.md has been updated successfully.
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0002-store-the-pantry-as-an-append-only-json-lines-file.md",
 "content": "# 2. Store the pantry as an append-only JSON Lines file\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not decided: `pantry/store.py` (`path`, `_append`, `_records`) writes each add or remove as one line and never rewrites the file. Serves R-2 (QG-1) and R-3 (QG-3, no database).\n\n## Decision\n\nWe will keep the pantry in one JSON Lines file, `~/.pantry.jsonl` or the path in `PANTRY_FILE`, and only ever append to it.\n\n## Consequences\n\nA crash can leave a partial last line, and the next append is glued onto it (arc42 section 11, risk 1). The file grows without bound; there is no compaction. Corrupt lines are handled under ADR 0007.\n\nQuestion for the architect: keep the append-only file?\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/adr/0002-store-the-pantry-as-an-append-only-json-lines-file.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0003-records-are-json-objects-with-op-name-and-expires.md",
 "content": "# 3. Records are JSON objects with op, name and expires\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not decided: `pantry/model.py` (`Item.to_record`, `removal`, `replay`). Serves R-1 (QG-4).\n\n## Decision\n\nWe will record an add as `{\"op\": \"add\", \"name\": NAME, \"expires\": ISO-DATE}` and a remove as `{\"op\": \"remove\", \"name\": NAME}`. Replay applies them in file order, so a later add of the same name replaces the earlier one.\n\n## Consequences\n\nA new op or key changes the file format and needs a new ADR. Replay raises an error on a record that lacks a key (arc42 section 11, risk 3).\n\nQuestion for the architect: keep this record format?\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/adr/0003-records-are-json-objects-with-op-name-and-expires.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0004-date-input-iso-today-tomorrow-and-relative-offsets.md",
 "content": "# 4. Date input: ISO, today, tomorrow, and +Nd or +Nw\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not decided: `pantry/dates.py` (`parse`). Serves R-1 (QG-4).\n\n## Decision\n\nWe will accept an expiry date as an ISO date, `today`, `tomorrow`, `+Nd` or `+Nw`, resolved against the local date when the item is added.\n\n## Consequences\n\nThe stored date is absolute, so later changes of the clock do not move it. Adding another input form is a change to the user interface and needs a new ADR (ADR 0005).\n\nQuestion for the architect: keep these input forms?\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/adr/0004-date-input-iso-today-tomorrow-and-relative-offsets.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0005-cli-commands-and-exit-codes.md",
 "content": "# 5. CLI commands and exit codes\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not decided: `pantry/cli.py` (`main`). Serves R-1 (QG-4); users and scripts depend on these commands.\n\n## Decision\n\nWe will provide `add NAME EXPIRES`, `list [--soon DAYS]` and `remove NAME`. We will exit 0 on success, 1 on a user error, and 2 on bad usage.\n\n## Consequences\n\nChanging a command, flag or exit code changes what users and scripts see, so it needs a new ADR. Date input is governed by ADR 0004.\n\nQuestion for the architect: keep these commands and exit codes?\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/adr/0005-cli-commands-and-exit-codes.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0006-dependency-rule-between-blocks.md",
 "content": "# 6. Dependency rule between blocks\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not decided: the imports in `pantry/`. `cli` imports `dates`, `store` and `model`. `store` imports `model`. `model` and `dates` import only the standard library. Serves R-4 (QG-2).\n\n## Decision\n\nWe will let `cli` use `dates`, `store` and `model`; `store` use `model`; `model` and `dates` use no other block; and `__main__` use only `cli`.\n\n## Consequences\n\nA new command touches `cli.py` and at most one new module, as R-4 requires. A change that needs a new store operation touches `store.py`, which R-4 forbids unless the store API stays generic. This is the tension named in the proposal.\n\nQuestion for the architect: keep this dependency rule?\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/adr/0006-dependency-rule-between-blocks.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0007-crash-safety-by-fsync-per-append-and-skipping-unparseable-lines.md",
 "content": "# 7. Crash safety: fsync per append, skipping unparseable lines\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not decided: `pantry/store.py` (`_append` flushes and fsyncs each record; `_records` skips lines that do not parse). Serves R-2 (QG-1).\n\n## Decision\n\nWe will fsync each appended record before the command returns, and skip any line that does not parse when the file is read.\n\n## Consequences\n\nAn add that returned survives a crash after it returned. Skipping hides corrupt lines, as ADR 0001 records. It does not handle a partial line followed by a new append (arc42 section 11, risk 1), and the directory is not fsynced (risk 4).\n\nQuestion for the architect: keep this crash-safety approach, or change it in a new ADR?\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/adr/0007-crash-safety-by-fsync-per-append-and-skipping-unparseable-lines.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0008-error-reporting-on-stderr-naming-the-input.md",
 "content": "# 8. Error reporting on stderr, naming the input\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not decided: `pantry/cli.py` prints user errors to stderr with the offending input (`not a date`, `no such item`). Serves R-1 (QG-4).\n\n## Decision\n\nWe will report user errors on stderr as `pantry: <message>`, naming the input that caused them.\n\n## Consequences\n\nOutput on stdout stays the list of items, so scripts reading it are unaffected. Exit codes are governed by ADR 0005.\n\nQuestion for the architect: keep this error format?\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/adr/0008-error-reporting-on-stderr-naming-the-input.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-xd_cdktr/project/docs/adr/0009-standard-library-only.md",
 "content": "# 9. Standard library only\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not decided: every module in `pantry/` and `tests/` imports only the standard library. Serves R-3 (QG-3).\n\n## Decision\n\nWe will use only the Python standard library, with no third-party package and no install step.\n\n## Consequences\n\nInstallation stays a copy of the source tree. A richer command-line parser or a TOML reader is unavailable without a new ADR.\n\nQuestion for the architect: keep the standard-library-only rule?\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-xd_cdktr/project/docs/adr/0009-standard-library-only.md (file state is current in your context — no need to Read it back)
```

### assistant

All sections and ADRs are written. Last, I'll confirm that only `docs/` changed, since recovery must not touch code.

### tool_use Bash

```json
{
 "command": "git status --short && git diff --stat && ls docs/adr && grep -n \"^## \\|^\\*As found\" docs/architecture/arc42.md | head -60",
 "description": "Verify changed files and arc42 section markers"
}
```

### tool_result

```
?? docs/
?? pantry/__pycache__/
0001-record-architecture-decisions.md
0002-store-the-pantry-as-an-append-only-json-lines-file.md
0003-records-are-json-objects-with-op-name-and-expires.md
0004-date-input-iso-today-tomorrow-and-relative-offsets.md
0005-cli-commands-and-exit-codes.md
0006-dependency-rule-between-blocks.md
0007-crash-safety-by-fsync-per-append-and-skipping-unparseable-lines.md
0008-error-reporting-on-stderr-naming-the-input.md
0009-standard-library-only.md
5:## 1. Introduction and goals
27:## 2. Constraints
29:*As found, unconfirmed.*
35:## 3. Context and scope
37:*As found, unconfirmed.*
52:## 4. Solution strategy
54:*As found, unconfirmed.*
61:## 5. Building block view
63:*As found, unconfirmed.*
75:## 6. Runtime view
77:*As found, unconfirmed.*
83:## 7. Deployment view
85:*As found, unconfirmed.*
89:## 8. Crosscutting concepts
91:*As found, unconfirmed.*
100:## 9. Architecture decisions
104:## 10. Quality requirements
113:## 11. Risks and technical debt
115:*As found, unconfirmed.*
124:## 12. Glossary
```

### assistant

The probe imports left a `pantry/__pycache__/` directory that I created. I'll remove it so only `docs/` remains as the change.

### tool_use Bash

```json
{
 "command": "rm -rf pantry/__pycache__ && git status --short",
 "description": "Remove cache created by my probe and recheck status"
}
```

### tool_result

```
?? docs/
```

### assistant

The architecture is recovered from the code. Everything under `docs/` is a draft for you to review. The code is unchanged, and nothing is committed.

**Accepted:** ADR 0001, "Record architecture decisions", is now `accepted 2026-11-21`. Its text is unchanged apart from the Status line.

**Sections marked *as found, unconfirmed*** (review in this order):
- **2. Constraints:** standard library only; Python 3.7 or later, since the code uses `dataclasses` and `date.fromisoformat`; data under `~/.pantry.jsonl`, overridable with `PANTRY_FILE`.
- **3. Context and scope:** a terminal command that touches only the local file, the clock and the terminal, with no network. Your "Out of scope" answers stay below it, unmarked.
- **4. Solution strategy:** an append-only log replayed on read, fsync per append, one plain file.
- **5. Building blocks:** `__main__` → `cli` → `dates`, `store` → `model`. The dependency rule holds in the imports. Tests are noted as not a block.
- **6. Runtime view:** what `add`, `remove` and `list --soon` do.
- **7. Deployment:** run as `python3 -m pantry` from the source tree; no packaging file.
- **8. Crosscutting:** error output and exit codes, durability, record and date formats, naming.
- **11. Risks:** listed below.

**Proposed ADRs 0002–0009**, each `proposed` with its question:
- 0002 Append-only JSON Lines file: keep it?
- 0003 Record format `{"op", "name", "expires"}`: keep it?
- 0004 Date input forms: keep them?
- 0005 CLI commands and exit codes: keep them?
- 0006 Dependency rule between blocks: keep it?
- 0007 Crash safety by fsync per append and skipping unparseable lines: keep it, or change it in a new ADR?
- 0008 Error output on stderr naming the input: keep it?
- 0009 Standard library only: keep it?

**Risks (section 11):**
1. **Verified: a new record is glued onto a partial line.** After a crash leaves a partial line, the next `add` appends onto it. The new item is then lost on read. I ran a probe in a scratch file: an item acknowledged after a torn write was missing. This breaks R-2 and QS-1, and it is the most serious finding.
2. Corrupt lines in the middle of the file are skipped silently. This is already in ADR 0001's consequences.
3. Read, not run: a record that is valid JSON but lacks a key makes `list` and `remove` fail.
4. Read, not run: the directory is not fsynced when the file is created.
5. Read, not run: nothing stops two processes appending at once.
6. Technical debt: the file is never compacted.

**Left open:** I didn't change the code, so risk 1 stands. A fix would be a new decision, since it touches the crash-safety approach in ADR 0007. The stakeholders, the Python floor, and the goal order also remain unconfirmed, as before.

### result (success)
