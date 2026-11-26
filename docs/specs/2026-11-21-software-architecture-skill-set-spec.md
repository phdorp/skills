# Software Architecture Skill Set Spec

Status: ready-for-agent
Source: [2026-11-21-software-architecture-skill-set-design.md](2026-11-21-software-architecture-skill-set-design.md)
(approved 2026-11-21). Decision numbers D1–D18 below refer to that design.

## Problem Statement

The user wants to run projects with a systematic software architecture method (their seminar
summary at `/root/repos/software-architectrue/software-architecture-fundamentals.md`): make quality
requirements explicit, choose solutions because they serve them, record decisions as ADRs,
document the architecture with arc42. They are the architect; the agent should be a coworker.

With this collection today, the agent never asks for quality goals, records decisions as an
optional one-paragraph note that nobody approves, and settles architectural questions itself:
`executing-plans` tells it to rule on conflicts and keep going. Its design vocabulary assumes code
with classes and calls, so a Modelica or Simulink project gets object-oriented advice. Nothing in
the collection sets up architecture documentation for a fresh project, recovers it for an
undocumented one, or checks new requirements against an existing architecture. Unspecified
quality requirements are therefore decided by accident during implementation, which the method
says is the most expensive place to decide them.

## Solution

Three new skills and changes to eight existing ones turn the collection's workflow into the
method, with the human as the only one who decides architecture:

- `setup-architecture` (user-invoked) brings a fresh, documented, or undocumented project into the
  method: arc42 document, ranked system-level requirements, 3–5 measurable quality goals, and an
  accepted "Record architecture decisions" ADR listing what is decided centrally.
- `quality-requirements` (model-invoked) holds the procedures for ranking requirements and deriving
  ISO/IEC 25010:2023 quality goals and scenarios from them.
- `add-requirements` (user-invoked) integrates later requirements: duplicates, consistency,
  project direction, triage.
- The existing workflow learns to ask about quality goals, to write architectural decisions as
  `proposed` ADRs and wait for the architect, to review against accepted ADRs, and to speak in
  paradigm-neutral terms.
- A kept scenario suite in `evals/software-architecture/` proves the behaviour against the current
  skills and can be re-run when the model or the skills change.

## User Stories

Setup

1. As an architect starting a fresh project, I want the agent to create `docs/architecture/arc42.md` with sections 1, 5, 9 and 10 started and the rest present but empty, so that documentation grows with the project.
2. As an architect, I want to give my requirements in my own words and have the agent sharpen the wording and assign `R-n` IDs, so that each requirement can be referenced.
3. As an architect, I want the agent to triage my first requirements so that only system-level ones enter arc42 section 1 and feature-level detail goes to the issue tracker, so that section 1 stays architectural.
4. As an architect, I want the agent to propose a ranking with a one-line reason each, point out conflicts, and ask pairwise tie-breakers, so that I can set the final order quickly.
5. As an architect, I want the agent to derive the ISO/IEC 25010 characteristics my requirements imply, each citing its requirement IDs, so that quality goals come from my requirements and not from a checklist.
6. As an architect, I want every proposed quality goal to come with a scenario (stimulus, environment, response, measure), so that it can be tested.
7. As an architect, I want a goal without a measure to come back to me as an open question rather than be filed, so that nothing unverifiable enters the document.
8. As an architect, I want the agent to ask "did you leave out something like X?" for characteristics no requirement supports, and never add them itself, so that I keep control of the goals.
9. As an architect, I want to confirm and rank the top 3–5 quality goals (`QG-n`) with their scenarios (`QS-n`) in arc42 sections 1 and 10, so that every later decision has something to trace to.
10. As an architect, I want the agent to draft the "Record architecture decisions" ADR with a list of decisions made centrally and decisions left to building blocks, so that I can edit and accept the line between architecture and development.
11. As an architect of an existing project with documentation in another form, I want the agent to map it onto arc42 sections where it already lives, without migrating it, so that nothing is duplicated.
12. As an architect of an existing project with status-less ADRs, I want them treated as accepted (legacy) and offered for upgrade in one batch, so that work is not paused all over the project.
13. As an architect of an undocumented project, I want the agent first to get the "made centrally" list accepted, then recover the as-is architecture, writing proposed ADRs only for listed decisions and marking everything else *as found, unconfirmed*, so that I review a manageable set.
14. As an architect of a Modelica or Simulink project, I want recovery to describe building blocks, signals as interfaces, and coupling through signal routing, so that the documentation fits the paradigm.
15. As an architect of a project whose ADR-0001 is already taken, I want the "made centrally" ADR to take the next free number and be found by its title, so that nothing is renumbered.
16. As an architect of a multi-context repo, I want one system-wide arc42 and "made centrally" ADR at the root, with context ADRs where they already live.

Adding requirements

17. As an architect, I want to run `add-requirements` with new requirements and have each checked for duplicates against the R-list and against deferred and rejected requirements.
18. As an architect, I want each new requirement checked for consistency with existing ones, with the conflicting requirement named.
19. As an architect, I want each checked against the project direction (arc42 section 1 goals and stakeholders, top quality goals, section 2 constraints, accepted ADRs), with the conflicting item named.
20. As an architect, I want the agent to propose one of four outcomes per requirement (system-level, feature-level, deferred, rejected) for me to confirm, so that triage is fast but mine.
21. As an architect, I want a confirmed system-level requirement to get the next R-ID, be re-ranked, and be checked against the quality goals, so that the goals stay current.
22. As an architect, I want a conflict with an accepted ADR to produce a proposed superseding ADR and pause work in that area.
23. As an architect, I want feature-level requirements to go to the tracker or a spec citing their parent R-ID, and continue through the existing `triage` skill.
24. As an architect, I want deferred and rejected requirements to stay in the R-list with status `deferred` or `rejected`, a one-line reason, and their R-ID, so that the duplicate check reads one table and an ID never changes meaning.
25. As an architect, I want the agent never to drop or rewrite a requirement on its own.
26. As an architect, when the agent notices a new requirement in a design conversation or during implementation, I want it to suggest `add-requirements` rather than run it.
27. As an architect, I want `add-requirements` in a project without arc42 to offer setup first.

Decisions

28. As an architect, I want the agent to treat a decision as architectural when it is expensive to change, crosses a module boundary, or is on the "made centrally" list, so that the trigger is concrete.
29. As an architect, I want decisions inside one building block left to implementation with no ADR, so that small changes carry no ceremony.
30. As an architect, I want every ADR in Nygard form with all five fields, Status required, and Context citing R-, QG- or QS-IDs.
31. As an architect, I want structural choices offered as 2–3 options, each tied to the quality goals it serves or hurts, with a recommendation, so that I decide on the grounds that matter.
32. As an architect, I want an option that cannot be tied to a quality goal left out.
33. As an architect, I want the agent to mark an ADR `accepted` only after my explicit approval, with the date.
34. As an architect, I want rejected ADRs kept with status `rejected` and one line why, and changed decisions recorded as new ADRs that supersede, so that nothing is deleted.
35. As an architect, I want the agent to propose an automated check when an accepted ADR states a mechanical rule, and add it only if I agree.

Implementation

36. As an architect, I want the agent to stop work that depends on a proposed ADR, ask me at once, and continue independent tasks.
37. As an architect, I want unattended runs (subagents, background agents, handoffs, ticket runs) to commit the proposed ADR on the working branch and list it in the final report.
38. As an architect, I want an unattended run in a repo with a pull-request remote to also open a PR containing only the ADR, where merging means accepted and closing means rejected.
39. As an architect, I want a subagent to return a proposed ADR to the agent that started it rather than contact me.
40. As an architect, I want no tracker issue for a proposed ADR, so that each decision lives in one place.
41. As an architect, I want specs to carry a Quality Requirements section linking the scenarios and ADRs they rely on, and never rely on a proposed ADR.

Review and vocabulary

42. As an architect, I want code review to report an Architecture axis separately from Standards and Spec, covering accepted-ADR conformance, arc42 section 8 rules, touched quality scenarios, and traceability.
43. As an architect, I want an accepted ADR that names no requirement or quality goal reported as a finding, except legacy ADRs.
44. As an architect, I want Long Method and Large Class in the smell baseline, and object-oriented-only smells marked "(OO)" with a dataflow counterpart where one exists.
45. As an architect, I want one vocabulary (`codebase-design`) that maps module, interface and seam to object-oriented, imperative and dataflow code and carries the principles, patterns and anti-patterns from my seminar.
46. As an architect, I want `improve-codebase-architecture` to tie each opportunity to a quality goal and route any accepted change through a proposed ADR.

Scope and safety

47. As a user of a project that has not run setup, I want the workflow to behave as today apart from one suggestion to run `setup-architecture`, so that unrelated projects gain no steps.
48. As the maintainer of this collection, I want a scenario suite I can re-run when the model or skills change, so that I notice when the discipline rules stop holding.

## Implementation Decisions

### New skills

- **`setup-architecture`** — user-invoked (`opencode/autoinvoke: false`). Detects the situation
  from observable state: no source code and no docs → fresh; architecture documentation present →
  documented; source code without architecture documentation → undocumented. Lays out the arc42
  skeleton, runs the requirement and quality-goal procedures, drafts the "made centrally" ADR,
  maps existing documentation (D1), upgrades legacy ADRs in one batch (D16), or recovers (D9).
  References: arc42 skeleton in our own words with links to arc42.org and docs.arc42.org;
  recovery procedure; "made centrally" ADR template with the default list.
- **`quality-requirements`** — model-invoked. Owns ranking (proposal, conflicts, pairwise
  tie-breakers), deriving 25010:2023 characteristics with requirement-ID citations, scenario
  writing with the "no measure → open question" rule, the gap question, and the goal-impact check
  used after a new requirement. References: 25010:2023 table adapted from the seminar summary;
  scenario template.
- **`add-requirements`** — user-invoked. Owns the four checks and the four-way triage (D18),
  calls `quality-requirements` for re-ranking and goal impact, hands feature-level items to the
  tracker and `triage`. `quality-requirements` points to its triage procedure for setup.

### Changed skills

- **`domain-modeling`** — owns ADRs everywhere. New ADR format (D6) replaces the one-paragraph
  template, new trigger rule (D5) replaces the three-condition test, approval protocol (D6, D17),
  supersede and reject, legacy ADRs (D16). Applies in every project; trigger uses the "made
  centrally" list when the project has one, the default rule otherwise.
- **`design-dialogue`** — after setup only: reads arc42 and ADRs while looking before asking, asks
  which quality goals a change touches, offers structural choices per D7, suggests
  `add-requirements` for new system-level requirements.
- **`spec-and-plan`** — spec template gains "Quality Requirements" (scenario IDs and ADRs the work
  relies on, cited, not copied; parent R-IDs). A spec may not rely on a proposed ADR.
- **`executing-plans`** — an architectural decision met mid-task is **not a Ruling**: it becomes a
  proposed ADR through `domain-modeling`, its dependent tasks pause, independent tasks continue,
  and the architect is asked at once; unattended runs follow D17. This is a fifth stop condition
  scoped to the dependent tasks, not a halt of the run.
- **`code-review`** — Architecture axis with its own sources (accepted ADRs, arc42 section 8, the
  quality scenarios) and its own report section; the smell baseline gains Long Method and Large
  Class and marks OO-only smells.
- **`codebase-design`** — paradigm mappings in the body; principles, GoF patterns, anti-patterns
  as reference files adapted from the seminar summary.
- **`improve-codebase-architecture`** — ties opportunities to quality goals; accepted change goes
  through a proposed ADR.
- **`setup-project-workflow`** — points to `setup-architecture`; its domain-doc section stays.

Every changed skill except `domain-modeling` gates its architecture behaviour on the presence of
`docs/architecture/arc42.md` (D15).

### Documents a set-up project carries

- `docs/architecture/arc42.md` with all 12 section headings; section 1 holds the R-list as a
  table (ID, requirement, rank, status `active | deferred | rejected`, reason), stakeholders and
  top goals; section 10 holds QS scenarios; section 9 links to `docs/adr/`; section 12 links to
  `GLOSSARY.md`.
- `docs/adr/NNNN-slug.md` in Nygard form; one titled "Record architecture decisions".
- Unconfirmed recovered content carries the marker *as found, unconfirmed*.

### Repository

- `README.md`: workflow table, skill list, user-invoked table (now 12 skills).
- `ATTRIBUTION.md`: adapted ideas from LLM-Coding/Semantic-Anchors (Apache-2.0) and
  MSiccDev/arc42-toolkit (MIT); no copied text from CC BY-SA sources or unlicensed repos.

## Testing Decisions

- **The seam is the scenario suite** in `evals/software-architecture/`, kept for re-runs and laid
  out like `evals/openmodelica/`: `README.md`, `TASKS.md`, `fixtures/`, `grader/`, `runs/`,
  `results/`.
- **Fixtures** (five small projects): fresh empty; documented in another form (README with a
  homegrown architecture section, plus status-less ADRs); undocumented Python with implicit
  decisions; undocumented Modelica dataflow project that compiles with `omc`; set-up project with
  `arc42.md`, ranked requirements, goals, the "made centrally" ADR and a few accepted ADRs.
- **Scenarios** give a fresh agent one task on a copy of one fixture, with the architect's input
  written into the task. They cover: setup in each of the three starting situations; adding
  requirements with a duplicate, an inconsistency and an ADR conflict; implementing a ticket that
  hides a cross-boundary decision, attended and unattended; reviewing a diff that breaks an
  accepted ADR; a project without setup to prove no new steps appear.
- **Grading**: `grade.py` (Python standard library) checks file outcomes; a rubric covers
  judged behaviour. A fresh judge agent scores each run against the rubric and quotes the
  transcript or file passage behind every verdict; the user reviews runs where judge and grader
  disagree, plus a sample. Grader self-test with reference and broken outputs, as in openmodelica.
- **Arms**: baseline (skills at `main`) and new skills; 2 runs per scenario, about 10 scenarios.
- **Models**: scenario runs on Claude Haiku 5.5 (`claude-haiku-5-5`) at medium effort; the judge
  on Claude Opus 5.5 (`claude-opus-5-5`).
- **Discipline rules get RED before GREEN**: for "never self-accept", "pause dependent work", and
  "no invented goals", the baseline run must show the failure before the change counts as fixing
  it (`writing-for-agents`).
- `python3 scripts/validate-skills.py` passes after every ticket.
- Prior art: `evals/openmodelica/` (layout, grader self-test, results table).

## Out of Scope

- The unattended "PR containing only the ADR" path (D17) is not exercised: fixtures have no
  pull-request remote. It is listed as a known gap in the suite's README.

- MADR or other richer ADR templates.
- C4, ATAM, threat modelling and diagrams.
- Migrating existing documentation into arc42.
- Enforcing ADRs without the architect agreeing to a check.
- Teaching the method.

## Further Notes

- `domain-modeling` lands first; every other change points to it.
- The seminar summary is the user's own text and may be adapted without attribution.
- Research: [../research/software-architecture-skill-sets.md](../research/software-architecture-skill-sets.md).
