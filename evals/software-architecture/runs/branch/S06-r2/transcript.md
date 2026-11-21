### user

/sa:setup-architecture Set up the architecture for birdlog, a command-line tool for logging bird sightings.
My requirements:
1. Birders log a sighting (species, place, time, count) from the command line.
2. No sighting is ever lost, even if the laptop dies mid-write.
3. Runs offline on Linux, macOS and Windows with nothing but Python installed.
4. Sightings export to the eBird CSV format.
5. It must be fast.
6. `birdlog list` shows the latest sighting first.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head -5 && find . -path ./.git -prune -o -print | head -100",
 "description": "Inspect project contents and git state"
}
```

### tool_result

```
d8f3160 fixture
.
./README.md
```

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

### assistant

The project holds only a `README.md`, so this is a fresh project. I'll read the README and the setup references before writing anything.

### tool_use Bash

```json
{
 "command": "cat README.md; echo ----; S=/tmp/sa-arm-klj2jrab/sa/skills; ls $S/setup-architecture/references $S/quality-requirements/references $S/domain-modeling; echo ----; cat $S/setup-architecture/references/arc42-skeleton.md; echo ----; cat $S/setup-architecture/references/made-centrally-adr.md",
 "description": "Read README and setup reference templates"
}
```

### tool_result

```
# birdlog

A command-line tool for logging bird sightings. Nothing is built yet.
----
/tmp/sa-arm-klj2jrab/sa/skills/domain-modeling:
ADR-FORMAT.md
GLOSSARY-FORMAT.md
SKILL.md
agents

/tmp/sa-arm-klj2jrab/sa/skills/quality-requirements/references:
iso-25010.md
quality-scenario.md

/tmp/sa-arm-klj2jrab/sa/skills/setup-architecture/references:
arc42-skeleton.md
made-centrally-adr.md
----
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
| 9. Architecture decisions | one sentence saying decisions are ADRs in `docs/adr/`, linked as `../adr/` from this file, and a link to the "Record architecture decisions" ADR |
| 10. Quality requirements | the quality scenario table (`quality-requirements` › references/quality-scenario.md) |
| 11. Risks and technical debt | known risks and debt, each with what it threatens |
| 12. Glossary | a link to `GLOSSARY.md`; without one, the line "`GLOSSARY.md` is created with the first resolved term." |

At setup, sections 1, 5 and 10 get their empty tables and sections 9 and 12 their links in the
first turn. Rows follow once the architect confirms; section 5's rows follow once building
blocks are decided.
----
# "Record architecture decisions" ADR

The ADR that draws the line between decisions the architect makes centrally and decisions left
to whoever builds a block. It takes the next free number (0001 in a fresh project); skills find
it by its title, never by its number. Format and status rules: `domain-modeling`.

```markdown
# <n>. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. <One sentence on
what this product needs from that line, citing the R- and QG-IDs it serves, e.g. "Sightings
must survive crashes (R-2, QG-1) and work everywhere with only Python (R-3, QG-2)".>

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- <items from the default list below, made concrete for this product>

Left to the building blocks (no ADR):

- <internal helpers, structure inside one block, test layout, …>

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
```

## Default list

A decisio
[... 488 chars cut]
```

### tool_use Bash

```json
{
 "command": "S=/tmp/sa-arm-klj2jrab/sa/skills; cat $S/domain-modeling/ADR-FORMAT.md; echo ----; cat $S/quality-requirements/references/quality-scenario.md; echo ----; cat $S/quality-requirements/references/iso-25010.md",
 "description": "Read ADR format and quality references"
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
----
# Quality scenario

A quality goal is testable only through a scenario (Bass, Clements and Kazman, *Software
Architecture in Practice*; arc42 section 10). Each part answers one question:

| part | answers | example (QG: Reliability: fault tolerance, from R-2) |
|---|---|---|
| source | who or what causes the stimulus (when it matters) | the operating system |
| stimulus | what happens | the process is killed with SIGKILL during `add` |
| artifact | which part is affected (when it matters) | the note store |
| environment | under which conditions | normal operation |
| response | what the system does | the note is either fully stored or absent; the store still opens |
| measure | the number that decides whether the goal is met | 0 unreadable stores in 100 trials |

The measure is a count, a time, a share or a limit someone can check. "Fast", "robust" or
"easy" is not a measure: ask the architect for the number, or for the observation that would
show the goal is met, and keep the goal open until they give one.

## arc42 section 10 row

```markdown
| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the note is either fully stored or absent; the store still opens | 0 unreadable stores in 100 trials |
```

Fold source and artifact into the stimulus when they need saying. Each `QS-n` names its
`QG-n`, and the goal's row in section 1 names its `QS-n` back.
----
# ISO/IEC 25010:2023 product quality model

Nine characteristics, each with its sub-characteristics. Use it as a checklist so no kind of
quality is forgotten; a goal names one characteristic and, where it helps, one
sub-characteristic ("Reliability: fault tolerance"). The meanings below are short paraphrases;
the standard is the authority. Worked examples of goals and scenarios:
[quality.arc42.org](https://quality.arc42.org/) (link, do not copy).

| characteristic | sub-characteristic | the degree to which … |
|---|---|---|
| Functional suitability | functional completeness | the functions cover the specified tasks and objectives |
| | functional correctness | results are correct and precise |
| | functional appropriateness | the functions help users reach their objectives |
| 
[... 2899 chars cut]
```

### assistant

The project is fresh: only a README that describes the idea. I'll write the skeleton, which is the only file this turn writes, then send the proposal.

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/sa-eval-qt4e1wl4/project/docs/architecture",
 "description": "Create the architecture docs directory"
}
```

### tool_result

```
(Bash completed with no output)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-qt4e1wl4/project/docs/architecture/arc42.md",
 "content": "# birdlog: architecture\n\nStructured after the arc42 template (https://arc42.org). Empty sections are filled when needed.\n\n## 1. Introduction and goals\n\n### Requirements overview\n\n| ID | requirement | rank | status | reason |\n|---|---|---|---|---|\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n\n### Stakeholders\n\n## 2. Constraints\n\n## 3. Context and scope\n\n## 4. Solution strategy\n\n## 5. Building block view\n\n| block | responsibility | may use |\n|---|---|---|\n\n## 6. Runtime view\n\n## 7. Deployment view\n\n## 8. Crosscutting concepts\n\n## 9. Architecture decisions\n\nDecisions are recorded as ADRs in `docs/adr/` ([`../adr/`](../adr/)). The ADR that draws the line between central and local decisions is [Record architecture decisions](../adr/0001-record-architecture-decisions.md); it is written once the architect confirms the setup.\n\n## 10. Quality requirements\n\n| ID | goal | stimulus | environment | response | measure |\n|---|---|---|---|---|---|\n\n## 11. Risks and technical debt\n\n## 12. Glossary\n\n`GLOSSARY.md` is created with the first resolved term.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-qt4e1wl4/project/docs/architecture/arc42.md (file state is current in your context — no need to Read it back)
```

### assistant

The skeleton is written at `docs/architecture/arc42.md`. Nothing else is written yet: no R-list rows, goals, or ADR until you confirm them.

## Proposal for birdlog

The project is fresh (only a README), so this is the first turn. The triage is against an empty R-list, so each requirement gets only a proposed outcome.

### 1. Triage

| # | requirement (your wording) | findings | proposed outcome | reason |
|---|---|---|---|---|
| 1 | Log a sighting (species, place, time, count) from the CLI | no duplicate; no conflict | system-level | It is the core function and fixes the input interface and the record shape. |
| 2 | No sighting is lost, even if the laptop dies mid-write | conflicts in tension with 5 (see Rank) | system-level | It decides how writes are made durable, which is hard to change later. |
| 3 | Runs offline on Linux, macOS, Windows with only Python | none | system-level | It sets the dependency rule: standard library only, no third-party packages. |
| 4 | Export to eBird CSV | none | system-level | It is an import/export data format, which is a central decision. |
| 5 | Must be fast | too vague to measure | system-level, reworded as a proposal | See the question below. |
| 6 | `birdlog list` shows the latest sighting first | none | feature-level under R-1 | Ordering is a detail of listing, which needs a parent. |

**Proposed wording, for you to accept or change:**
- R-1: "Birders log and review sightings (species, place, time, count) from the command line."
- R-5: "Logging a sighting and listing sightings each complete within a measured limit (limit to be set)."

### 2. Rank (proposed; you set the order)

1. **R-2** durability: the core promise, and it constrains the storage design.
2. **R-1** log and review: the core function.
3. **R-3** offline, Python only: sets the dependency rule for everything else.
4. **R-4** eBird export: a format decision, deferrable behind the core.
5. **R-5** speed: a goal with no measure yet.

**Conflict:** R-2 and R-5 pull against each other, because flushing each write to disk costs time.
**Tie-breaker question:** if only one of R-2 and R-5 can be fully met, which one?

### 3. Quality goals (candidates, not yet written)

| candidate | 25010 characteristic | from | measure |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | 0 confirmed sightings lost, 0 unreadable stores, in 100 kill-during-write trials. *Proposed number, please confirm.* |
| QG-2 | Flexibility: installability | R-3 | 0 third-party packages; the test suite passes on Linux, macOS and Windows. |
| QG-3 | Functional correctness | R-1, R-6 | 0 mismatched fields in a round-trip test; list order correct for all test cases. |
| QG-4 | Interoperability | R-4 | *Open question:* what check shows the exported file is accepted by eBird? |
| QG-5 | Performance efficiency: time behaviour | R-5 | *Open question:* what time for logging one sighting, and for listing N sightings (what N)? |

Only QG-1 to QG-3 have a measure I can state. QG-4 and QG-5 stay open until you give the numbers or observations.

### 4. Gap questions

Each asked once, as a question:
- Did you leave out **security: confidentiality**? For example, keeping the locations of sensitive birds private from anyone who sees the file.
- Did you leave out **usability: user error protection**? For example, catching typos in species names.
- Did you leave out **capacity**? How many sightings should one store hold over its lifetime?
- Did you leave out **maintainability: testability**? For example, a required test coverage level.

### 5. Decisions made centrally (draft list for ADR-0001)

Adjusted from the default list for this product:
- **Storage engine and on-disk format:** the core choice; the options (for example the standard library's SQLite or an append-only file) need a decision of their own, which I have not made.
- **Export format:** eBird CSV column mapping.
- **Interfaces and dependency rule:** standard library only, to be confirmed.
- **Versioning:** the CLI commands and the stored file format.
- **Crosscutting conventions:** how time and time zones are stored, and error handling.
- **Third-party dependencies:** none, if you confirm item 3.

### Your answers

1. Confirm or change each outcome in the triage table, and the reworded R-1 and R-5.
2. Set the rank order, and say which of R-2 or R-5 wins if they conflict.
3. Confirm QG-1 to QG-3 and their numbers, and give numbers or observations for QG-4 and QG-5.
4. Answer the four gap questions.
5. Confirm or change the decision list for ADR-0001.

### result (success)

### user

Your triage and your ranking are confirmed as proposed. The quality goals you proposed are
confirmed in your order, except any you could not give a measure: keep those as open
questions. To your "did you leave out" questions: no, nothing is missing. Write everything
down now. I'm offline after this, so finish without asking me again.

### assistant

Everything confirmed is now written. Here is what I'm applying, then the files.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-qt4e1wl4/project/docs/architecture/arc42.md",
 "old_string": "|---|---|---|---|---|\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n",
 "new_string": "|---|---|---|---|---|\n| R-1 | Birders log and review sightings (species, place, time, count) from the command line. | 2 | active | Core function; fixes the input interface and the record shape. |\n| R-2 | No sighting is lost, even if the laptop dies mid-write. | 1 | active | Core promise; decides how writes are made durable. |\n| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Sets the dependency rule: standard library only, no third-party packages. |\n| R-4 | Sightings export to the eBird CSV format. | 4 | active | Import/export data format; a central decision. |\n| R-5 | Logging a sighting and listing sightings each complete within a measured limit (limit to be set). | 5 | active | Goal with no measure yet; see the open questions for QG-4 and QG-5. |\n\nR-6 (`birdlog list` shows the latest sighting first) is feature-level under R-1 and has no row here; it is filed as an issue.\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n| QG-1 | Reliability: recoverability | R-2 | QS-1 |\n| QG-2 | Flexibility: installability | R-3 | QS-2 |\n| QG-3 | Functional correctness | R-1 | QS-3 |\n"
}
```

### tool_result

```
The file /tmp/sa-eval-qt4e1wl4/project/docs/architecture/arc42.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-qt4e1wl4/project/docs/architecture/arc42.md",
 "old_string": "|---|---|---|\n\n## 6. Runtime view",
 "new_string": "|---|---|---|\n\n## 6. Runtime view"
}
```

### tool_result

```
<tool_use_error>No changes to make: old_string and new_string are exactly the same.</tool_use_error>
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-qt4e1wl4/project/docs/architecture/arc42.md",
 "old_string": "|---|---|---|---|---|---|\n",
 "new_string": "|---|---|---|---|---|---|\n| QS-1 | QG-1 | the process is killed (SIGKILL, or power is lost) during `birdlog add` | normal operation | the sighting is either fully stored or absent; sightings stored before are intact and the store opens | 0 confirmed sightings lost and 0 unreadable stores in 100 kill-during-write trials |\n| QS-2 | QG-2 | a person installs birdlog on a machine with only Python 3 | fresh Linux, macOS or Windows machine, offline | birdlog runs without any package beyond the standard library | 0 third-party packages; the test suite passes on all three OSes |\n| QS-3 | QG-3 | a sighting is logged, then listed | normal operation | every field is stored as entered; `list` shows the latest sighting first | 0 mismatched fields and 0 wrong orderings in the round-trip test suite |\n"
}
```

### tool_result

```
The file /tmp/sa-eval-qt4e1wl4/project/docs/architecture/arc42.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/sa-eval-qt4e1wl4/project/docs/adr /tmp/sa-eval-qt4e1wl4/project/.scratch/requirements/issues",
 "description": "Create ADR and issue directories"
}
```

### tool_result

```
(Bash completed with no output)
```

### assistant

The R-list, goals and scenarios are in place. Next: ADR-0001 (status `proposed`) and the issue for R-6.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-qt4e1wl4/project/docs/adr/0001-record-architecture-decisions.md",
 "content": "# 1. Record architecture decisions\n\n## Status\n\nproposed\n\n## Context\n\nThe architect decides the architecture; contributors and agents build it. Sightings must survive a crash mid-write (R-2, QG-1, QS-1) and the product must work offline with only Python installed (R-3, QG-2, QS-2), so the storage and the dependency rule are decided centrally.\n\n## Decision\n\nWe record architecture decisions as ADRs in `docs/adr/`, in Nygard form.\n\nDecided centrally (needs an ADR the architect accepts):\n\n- Storage engine and on-disk data format (serves R-2, QG-1). The choice itself is not yet made and gets its own ADR.\n- Export format: the mapping from sightings to eBird CSV columns (serves R-4).\n- Interfaces between building blocks and the dependency rule: standard library only (serves R-3, QG-2).\n- Versioning of the CLI commands and the stored file format.\n- Crosscutting conventions: how time and time zones are stored, and error handling.\n- Third-party dependencies: none.\n\nLeft to the building blocks (no ADR):\n\n- Internal helpers, structure inside one block, test layout.\n\n## Consequences\n\nWork that depends on a decision on the list waits until its ADR is accepted. The storage engine choice waits for its own ADR; the export mapping waits for the export format decision. No code for storage or export is written before then.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-qt4e1wl4/project/docs/adr/0001-record-architecture-decisions.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-qt4e1wl4/project/.scratch/requirements/issues/01-list-latest-first.md",
 "content": "# `birdlog list` shows the latest sighting first\n\nParent: R-1 (feature-level).\n\n`birdlog list` shows sightings in order, latest first.\n\nAssumption made at setup: \"latest\" means the time of the sighting (the `time` field), not the time it was logged. If the architect means the logging time, change this before implementation.\n\nMeasured by QG-3 (QS-3): 0 wrong orderings in the round-trip test suite.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-qt4e1wl4/project/.scratch/requirements/issues/01-list-latest-first.md (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "sed -n 1,40p docs/architecture/arc42.md && git status --short",
 "description": "Verify arc42 tables and list changed files"
}
```

### tool_result

```
# birdlog: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log and review sightings (species, place, time, count) from the command line. | 2 | active | Core function; fixes the input interface and the record shape. |
| R-2 | No sighting is lost, even if the laptop dies mid-write. | 1 | active | Core promise; decides how writes are made durable. |
| R-3 | Runs offline on Linux, macOS and Windows with nothing but Python installed. | 3 | active | Sets the dependency rule: standard library only, no third-party packages. |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | Import/export data format; a central decision. |
| R-5 | Logging a sighting and listing sightings each complete within a measured limit (limit to be set). | 5 | active | Goal with no measure yet; see the open questions for QG-4 and QG-5. |

R-6 (`birdlog list` shows the latest sighting first) is feature-level under R-1 and has no row here; it is filed as an issue.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: recoverability | R-2 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Functional correctness | R-1 | QS-3 |

### Stakeholders

## 2. Constraints

## 3. Context and scope

## 4. Solution strategy

## 5. Building block view

| block | responsibility | may use |
|---|---|---|

## 6. Runtime view
?? .scratch/
?? docs/
```

### assistant

Everything you confirmed is written down. The architecture is set up, and ADR-0001 is waiting for your approval.

**Written**
- **`docs/architecture/arc42.md`**
  - R-list: R-1 to R-5, all `active`, ranked 2, 1, 3, 4, 5 as you confirmed. Each has its reason.
  - Quality goals: QG-1 (Reliability: recoverability, from R-2), QG-2 (Flexibility: installability, from R-3), QG-3 (Functional correctness, from R-1).
  - Scenarios: QS-1 to QS-3 in section 10, one per goal, each with the measure you confirmed.
  - Section 9 links to ADR-0001.
- **`docs/adr/0001-record-architecture-decisions.md`**: status `proposed`. It lists the central decisions from the draft: storage engine and data format, export mapping, dependency rule (standard library only), CLI and file-format versioning, crosscutting conventions, and no third-party dependencies. The storage choice itself is not made; it gets its own ADR later.
- **`.scratch/requirements/issues/01-list-latest-first.md`**: R-6 as a feature-level issue under R-1. The project has no `docs/agents/issue-tracker.md`, so the issue went to the fallback path.

**Open questions (no goal rows written, as you asked)**
- QG-4, Interoperability (R-4): what check shows eBird accepts the exported file?
- QG-5, Performance time behaviour (R-5): what time limit for logging one sighting, and for listing how many sightings?

**Choices I made that you can redirect**
- **Tie-breaker:** R-2 ranks above R-5, so if the two conflict, durability wins over speed.
- **"Latest" in R-6:** I read it as the sighting's own time, not the time it was logged. The issue states this assumption.
- **R-5 stays `active`** with "limit to be set" in its wording, until QG-5 gets a number.

**Waiting for you**
- **ADR-0001:** accept or reject its text. Nothing else waits on it yet, because no storage or export work has started.
- **Storage engine and export mapping:** both wait for their own ADRs after ADR-0001 is accepted.

I did not write section 5 (building blocks) or the glossary; both follow later.

### result (success)
