# Software Architecture Skill Set: Design

Status: draft, awaiting approval (builder check done)
Source: design conversation of 2026-11-21; method in
`/root/repos/software-architectrue/software-architecture-fundamentals.md` (seminar summary, kept
outside this repo); prior art in
[docs/research/software-architecture-skill-sets.md](../research/software-architecture-skill-sets.md).

## Intent and why

The user wants to run projects with a systematic software architecture method: make quality
requirements explicit, choose solutions because they serve those requirements, record decisions
as ADRs, and document the architecture with arc42. In this skill set **the human is the
architect**. They provide requirements and make every architectural decision. The agent is a
coworker: it sharpens and prioritises requirements, derives quality goals, prepares options,
drafts ADRs and documentation, implements, and reviews against what was decided.

Today this collection's workflow (`design-dialogue` → `spec-and-plan` → `executing-plans` →
`code-review`) never asks for quality goals, its ADR format is a one-paragraph note with optional
status, and its design vocabulary is phrased for code with classes and calls. Agents in the
popular external packs decide architecture themselves ("make confident architectural
decisions"). The research found no existing set that covers the method end to end, and none
that covers the architecture/development boundary or ties pattern choices to quality goals.

## Goals

1. A project using this collection has, after setup, an arc42 document, a ranked requirement
   list with IDs, 3–5 confirmed quality goals with measurable scenarios, and an ADR-0001 that
   lists which decisions are made centrally.
2. Every architectural decision the agent meets is written as a `proposed` ADR and waits for
   the architect; no code that depends on it is written before acceptance.
3. Every accepted ADR traces back to requirement and quality-goal IDs.
4. Code review reports on architecture conformance separately from coding standards and spec.
5. The skills work unchanged for object-oriented, imperative, and model-based (dataflow, e.g.
   Simulink or Modelica) projects in any language.
6. All three starting situations are handled, and new requirements can be added to an existing
   architecture at any time (see D1 and D18).

## Non-goals

- MADR or any richer ADR template (may come later).
- C4, ATAM, threat modelling, or diagram generation.
- Migrating existing documentation into arc42 form.
- Tooling that enforces ADRs automatically on its own; checks are proposed per ADR.
- Teaching the method. The seminar summary stays the user's reference.

## Anti-goals

- The agent accepts its own proposals, or treats a `proposed` ADR as settled.
- The agent invents quality goals or targets that no requirement supports.
- A second, parallel design vocabulary next to `codebase-design`.
- Process that slows small changes: a change inside one building block gets no ADR and no
  ceremony.
- Copying CC BY-SA text (arc42 template, quality.arc42.org) into this MIT repo.

## Constraints

- Repo rules in `AGENTS.md`: lowercase kebab-case IDs equal to `name:`, descriptions say *when*,
  one meaning in one place, heavy reference in skill directories, `python3
  scripts/validate-skills.py` passes, README updated, borrowed material recorded in
  `ATTRIBUTION.md`, cross-references rewritten so no stale IDs survive.
- Skills are tested with `writing-for-agents` (RED without the change, GREEN with it).
- ISO/IEC 25010 **2023** model: nine characteristics (Functional suitability, Performance
  efficiency, Compatibility, Interaction capability, Reliability, Security, Maintainability,
  Flexibility, Safety), as tabled in the seminar summary §3.
- Licences: arc42, quality.arc42.org and arc42agentic are CC BY-SA 4.0 — link and paraphrase
  only. Semantic-Anchors (Apache-2.0) and MSiccDev/arc42-toolkit, docs-as-code
  architecture-knowledge-toolkit (MIT) may be adapted with notice. skillrecordings/adr-skill has
  no licence — ideas only.
- Language and paradigm agnostic: no skill text may assume classes, objects, or a specific
  language.

## Approaches

1. **One hub skill** `software-architecture` with the whole method. One home, but one
   description must trigger for very different moments and every run loads everything.
2. **Two focused new skills plus adaptations** — chosen. `quality-requirements` and
   `setup-architecture`; ADRs stay in `domain-modeling`, the rest are changes to existing
   skills. Each skill fires at one clear moment; matches the existing split between
   `setup-project-workflow` and `design-dialogue`.
3. **No new skills**, folding everything into `design-dialogue` and `setup-project-workflow`.
   Rejected: it bloats a deliberately open-ended dialogue skill, and architecture recovery is
   analysis, not configuration.

The user chose option 2, and asked explicitly that the existing skills be adapted to the new
workflow rather than left alongside it.

## Decisions

Decisions marked *(agent's call)* were proposed by the agent during design and not objected
to, or settled by the agent afterwards; all others were the user's.

### D1. Project situations

| Situation | Entry point | What happens |
|---|---|---|
| Fresh project | `setup-architecture` | Create arc42 skeleton, run `quality-requirements` from scratch, draft ADR-0001. |
| Existing, documented | `setup-architecture` | Map existing documentation onto arc42 sections where it already lives (no migration); fill gaps. Migrating is a separate decision, recorded as an ADR. |
| Existing, undocumented | `setup-architecture` | Recover the as-is architecture from code (see D9). |
| New requirements for an existing architecture | `add-requirements` (D18) | Recurring, not a setup case. A skill of its own, invoked by the architect. |

### D2. Roles

The architect provides requirements and decides. The agent prepares, drafts, implements, and
never accepts its own proposals.

### D3. Requirements

- Live in arc42 section 1 ("Requirements overview"), each with an ID `R-1`, `R-2`, …; bulky
  requirements move to a linked `docs/requirements.md`.
- Section 1 holds only **system-level** requirements: the ones the architect provides that shape
  the architecture. The triage from D18 applies to the first requirements at setup too, so
  feature-level detail goes to the issue tracker from the start.
- Specs cite the parent R-ID; they never copy the requirement.
- The architect writes or dictates them; the agent sharpens the wording.
- Prioritisation: the agent proposes a ranking with a one-line reason each, points out conflicts
  between requirements, and breaks ties with pairwise questions ("if only one of R-3 and R-7 can
  be fully met, which?"). The architect sets the final order. No scoring scheme (MoSCoW etc.)
  unless the user asks.

### D4. Quality goals

- The agent derives the implied ISO/IEC 25010:2023 characteristics from the prioritised
  requirements, each citing its requirement IDs.
- For each, it proposes a quality scenario: stimulus, environment, response, measure (plus
  source and artifact where useful). A goal without a measure is not filed; it becomes an open
  question to the architect.
- The architect confirms and ranks the top 3–5. Goals go in arc42 section 1 (list), scenarios in
  section 10, with IDs `QG-1`… and `QS-1`… *(ID prefixes: agent's call)*.
- The 25010 checklist is used only to ask "did you leave out something like X?"; a
  characteristic no requirement supports is flagged, never added.

### D5. What counts as architectural

- Replaces `domain-modeling`'s current three-condition test (hard to reverse **and** surprising
  **and** a real trade-off).
- Rule: a decision is architectural when it is **expensive to change later** or **crosses a
  module boundary** (interfaces, data formats, dependency rules, versioning, crosscutting
  conventions such as naming, units, error handling), **or** it is on the project's own list.
- The list lives in an ADR titled "Record architecture decisions", drafted at setup, accepted by
  the architect. It takes ADR-0001 in a fresh project, otherwise the next free number; skills find
  it by its title and the link from arc42 section 9, never by number *(agent's call)*.
  Decisions inside a single building block are left to implementation and get no ADR.

### D6. ADR format and lifecycle

- Nygard format, all five fields required: Title, Status, Context, Decision, Consequences.
  Replaces the one-paragraph template in `domain-modeling/ADR-FORMAT.md`. Files stay
  `docs/adr/NNNN-slug.md`.
- Context names the requirement and quality-goal IDs the decision serves.
- Status values: `proposed`, `accepted`, `rejected`, `superseded by ADR-NNNN`.
- Only the architect accepts. The agent may change `proposed` to `accepted` only after explicit
  approval in the conversation, and records the date.
- Rejected proposals stay, with status `rejected` and one line saying why. ADRs are never deleted.
- A changed decision is a new ADR that supersedes the old one.

### D7. Choosing paradigms and patterns

When a design needs a structural choice (paradigm, architectural pattern, design pattern), the
agent presents 2–3 options, each tied to the quality goals it serves or hurts, recommends one, and
writes the architect's choice as a proposed ADR. An option that cannot be tied to a quality goal
is not offered.

### D8. Implementation while an ADR is proposed

The agent continues independent tasks and pauses all implementation that depends on a proposed
ADR, and asks the architect at once. When nobody is in the conversation, D17 applies.

### D9. Recovering an undocumented project

The agent drafts the as-is architecture from the code. It writes proposed ADRs only for
decisions on the project's "made centrally" list; everything else goes into the arc42 sections
marked *as found, unconfirmed*, which the architect reviews section by section. Nothing inferred
counts as decided until accepted. Because the "made centrally" list does not exist yet in this situation,
the agent first drafts ADR-0001 from the default rule in D5 and gets it accepted *(ordering:
agent's call)*.

### D10. Documents and locations

- arc42 in `docs/architecture/arc42.md`, one file; split per section only when it grows too big.
- Start with sections 1, 10, 9 and 5; others are filled when needed.
- Section 9 links to `docs/adr/`; section 12 links to the existing `GLOSSARY.md` instead of
  repeating it.
- A repo with several contexts (`GLOSSARY-MAP.md`) has one system-wide arc42 and one "made
  centrally" ADR at the root; context-specific ADRs stay in that context's `docs/adr/`, as
  `domain-modeling` already allows *(agent's call)*.
- The arc42 skeleton in the skill is written in our own words with links to arc42.org and
  docs.arc42.org (licence constraint).

### D11. Mechanical rules

When an accepted ADR states a rule a tool can check (dependency rule, naming convention), the
agent proposes an automated check (linter, test, CI step). The architect decides whether to add
it.

### D12. Code review

`code-review` gains a third axis, **Architecture**, next to Standards and Spec. It checks
conformance to accepted ADRs, the crosscutting rules in arc42 section 8, the quality scenarios
the change touches, and traceability (an accepted ADR naming no requirement or quality goal is a
finding). The Standards smell baseline gains Long Method and Large Class.

### D13. One vocabulary

`codebase-design` becomes the single paradigm-neutral vocabulary. It keeps module, interface,
seam, depth, adapter, leverage, locality, and adds:

- how the terms map to object-oriented, imperative, and dataflow code (in dataflow, signals are
  the interface and coupling comes from signal routing and shared data);
- the programming principles (SoC, DRY, KISS, YAGNI, SOLID, Law of Demeter, Rule of Three) with
  their tensions, each with a dataflow reading;
- the GoF patterns, the anti-patterns (Blob, Lava Flow, Golden Hammer, Spaghetti Code, Analysis
  Paralysis), and code smells, as reference files reached by pointer.

New text is paradigm-neutral. Existing smells and GoF patterns that assume object-oriented code
are marked "(OO)", with the dataflow counterpart where one exists, rather than rewritten. The
reference files are short tables that link out to the sources, not teaching material *(agent's
calls)*. They may adapt the user's seminar summary directly: it is the user's own text, so no
`ATTRIBUTION.md` entry is needed for it.

Paradigm choice is per project or building block, and is itself a D7 decision.

### D14. Skill set

**New skills**

- `quality-requirements` (model-invoked): the first requirement list and IDs, prioritisation,
  deriving 25010 characteristics, scenarios with measures. Its re-ranking and goal-impact
  procedures are reused by `add-requirements`. Reference files: 25010:2023 characteristic table
  in our own words, scenario template.
- `add-requirements` (user-invoked, `opencode/autoinvoke: false`): integrates requirements the
  architect adds later (D18). Owns the triage procedure, which `quality-requirements` points to
  at setup.
- `setup-architecture` (user-invoked, `opencode/autoinvoke: false`): detects the situation
  (D1 cases 1–3), lays out `arc42.md`, drafts ADR-0001 with the "made centrally" list, runs
  recovery (D9) or mapping. Reference files: arc42 skeleton, recovery procedure.

**Changed skills**

| Skill | Change |
|---|---|
| `domain-modeling` | ADR format (D6), trigger rule (D5), approval protocol, traceability field, supersede and reject. Remains the one owner of ADRs. |
| `design-dialogue` | Asks which quality goals a change touches; when a request brings a new system-level requirement, suggests the architect run `add-requirements`; structural choices follow D7; reads arc42 and ADRs in "look before you ask". |
| `spec-and-plan` | Spec template gains a "Quality Requirements" section linking the scenarios and ADRs; specs may not rely on proposed ADRs. |
| `executing-plans` | Detects architectural decisions mid-task, drafts a proposed ADR via `domain-modeling`, pauses dependent tasks, continues independent ones (D8); unattended runs follow D17. |
| `code-review` | Architecture axis and smell baseline (D12). |
| `codebase-design` | Paradigm-neutral vocabulary, principles, patterns (D13). |
| `improve-codebase-architecture` | Ties each deepening opportunity to a quality goal; any accepted change goes through a proposed ADR. |
| `setup-project-workflow` | Points to `setup-architecture` for the architecture docs; its domain-doc section stays for the glossary and ADR locations. *(agent's call: no merge of the two setup skills.)* |

Every changed skill applies its architecture behaviour only when the project is set up (D15).

Also: `README.md` (workflow table, skill list, user-invoked table), `ATTRIBUTION.md` (adapted ideas from
Semantic-Anchors and MSiccDev/arc42-toolkit; inspiration from docs-as-code toolkit and
skillrecordings, credited without copied text).

### D15. When the architecture behaviour switches on

The new steps (quality-goal questions, pausing on proposed ADRs, the Architecture review axis,
the spec's Quality Requirements section) run only in projects that have
`docs/architecture/arc42.md`. Other projects behave as today, apart from a single suggestion to
run `setup-architecture`. `add-requirements` in a project without it offers to run setup first.
The changes to `domain-modeling` (D5, D6) apply everywhere.

### D16. ADRs a project already has

Existing ADRs without a Status count as *accepted (legacy)*: they are not reopened and raise no
traceability findings. During setup the agent offers to bring them into the D6 format with
traceability, and the architect confirms them in one batch.

### D17. Approval when nobody is in the conversation

Applies to subagents, background agents, handoffs, and runs from `ready-for-agent` tickets.

- **Always:** the agent commits the ADR as `docs/adr/NNNN-….md` with status `proposed` on the
  working branch and lists it in its final report. The architect approves later in the
  conversation.
- **When the repo has a remote with pull requests, also:** the agent opens a PR containing only
  the ADR against the default branch. Merging it means `accepted`; closing it means `rejected`.
- No issue on the tracker; that would store the decision in a second place.
- Dependent work stays paused and independent work continues (D8).
- A subagent never contacts the architect. It returns the proposal to the agent that started it,
  which applies the two rules above.
- A new requirement noticed during such a run goes in the final report as "suggest running
  `add-requirements`", nowhere else.

### D18. Adding requirements: `add-requirements`

A dedicated skill, invoked only by the architect. When the agent notices a new requirement in
`design-dialogue` or during implementation, it suggests running the skill but does not run it.
For each new requirement the agent:

1. **Checks for duplicates** against the existing R-list.
2. **Checks consistency** with the existing requirements, naming any conflict.
3. **Checks the project direction**: the goals and stakeholders in arc42 section 1, the top
   quality goals, the constraints in section 2, and the accepted ADRs. Conflicts are reported
   with the conflicting item named. The agent never drops or rewrites a requirement on its own.
4. **Triages** it into one of four outcomes, which the agent proposes and the architect
   confirms:
   - *System-level*: gets the next R-ID, is re-ranked, and is checked against quality goals and
     accepted ADRs using the `quality-requirements` procedures. A conflict with an accepted ADR
     yields a proposed superseding ADR, and work in that area pauses (D8).
   - *Feature-level*: fits within existing requirements; goes to the issue tracker or a spec,
     citing its parent R-ID, and from there through the existing `triage` skill.
   - *Deferred*: recorded with a reason.
   - *Rejected*: recorded with a reason.

Where deferred and rejected requirements are recorded is left to the builder, as long as it is
one place that `add-requirements` checks for duplicates.

## What is left to the builder

- The exact wording, file split and reference layout inside each skill, within `AGENTS.md`'s
  rules.
- Which Semantic-Anchors traceability rules and MSiccDev interview prompts to adapt, as long as
  `ATTRIBUTION.md` records them.
- How `executing-plans` recognises an architectural decision mid-task, as long as it applies D5
  and ADR-0001's list.
- The RED/GREEN scenarios for testing each skill change.
- The order of work, though `domain-modeling` (D5, D6) should land first since every other
  change points to it.

Come back to the architect for: anything that changes the roles (D2), adds a template or
process step beyond this design, changes document locations, or makes a change inside one
building block require an ADR.
