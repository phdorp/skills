# Campaign: design dialogue and spec in a set-up project (ticket 08)

Method: `writing-for-agents` › testing-skills (RED on the `main` skills, smallest change, GREEN
on the branch, one loophole round). Plan: `docs/plans/2026-11-21-sa-design-dialogue-and-spec.md`.

## RED: skills at `main` (2026-11-22, Haiku 5.5 medium, 2 runs each, clean isolation)

`main` has both `design-dialogue` and `spec-and-plan`, so every run started with the
`/sa:<skill>` prefix. No run loaded another skill through the Skill tool. S11 kept one session
over both turns.

| run | failed checks | failed criteria |
|---|---|---|
| S11-r1 | goals_cited, add_requirements_suggested | J1, J2, J3 |
| S11-r2 | goals_cited, add_requirements_suggested | J1, J2, J3 |
| S12-r1 | qr_section, qr_cites, (code_unchanged, see below) | J2 |
| S12-r2 | qr_section, qr_cites | J2 |
| S13-r1, S13-r2 | - | - |
| S14-r1, S14-r2 | - | - |

Observed failures, in the agents' words (`runs/baseline/S1[12]-r*`):

1. **Trade-offs tied to requirements and ADRs, not quality goals** (S11, both, J1, J2,
   `goals_cited`): both runs read arc42 and the ADRs and argued from R-3, ADR-0002 and QS-2, but
   neither named a `QG-n` in turn 2: "Trade-off: it needs a third-party dependency, so R-3 and
   ADR-0002 both need accepted changes." (S11-r1).
2. **Encryption handled as an ADR, not as a new requirement** (S11, both, J3,
   `add_requirements_suggested`): "1. ADR for the `cryptography` dependency (R-3 change)."
   (S11-r1); "Needs an accepted ADR, since it changes R-3 (standard library only) and adds a
   dependency." (S11-r2). Neither names `add-requirements`.
3. **No Quality Requirements section** (S12, both, J2, `qr_section`): S12-r1 put the links in a
   header line, "Related: … arc42 QG-1 / QS-1 (no note lost)."; S12-r2 went from Implementation
   Decisions straight to Testing Decisions and cited no `QS-n`.

What held on `main`:

- Both S11 runs read arc42 in turn 1 (`arc42_read`), built nothing (`nothing_built`) and treated
  ADR-0004 as proposed (J4): "ADR-0004 (atomic writes, still proposed) would apply to each
  exported file." (S11-r1). These get no GREEN credit.
- Both S12 runs marked the spec blocked on ADR-0004 (J1): "Status: ready-for-agent (blocked on
  ADR-0004 acceptance; see Further Notes)" (S12-r1). Neither copied QS-1's measure
  (`not_copied`). No GREEN credit for J1 or `not_copied`.
- Controls: S13 and S14 raised no quality goals, arc42 or ADRs; neither suggested
  `setup-architecture`.

Grader correction: S12-r1 added a glossary term ("**Backup**: a copy of the store, …") and so
failed `code_unchanged`. A glossary entry is documentation, as S09/S10's `DOC_FILES` already
say; the check now allows `GLOSSARY.md` (self-test case `S12-glossary`), and S12-r1 passes it.

Gate: met (both S11 runs fail `goals_cited` and J1–J3; both S12 runs fail `qr_section` and J2).

## GREEN, first attempt: skills at `890c456` (2026-11-22, 2 runs each, clean isolation)

Every run started with `/sa:<skill>`. Both S11 runs read `references/architecture.md` in turn
1; both S12 runs read the template. S12 was re-run after a session restart cut its first two
runs off; S11, S13 and S14 completed before it. No earlier scenario loads or names
`design-dialogue` or `spec-and-plan` (grep of `runs/branch/S0*`, `S10*`), so S01–S10 keep
their branch runs.

| run | failed checks | failed criteria |
|---|---|---|
| S11-r1 | goals_cited | J1, J2 |
| S11-r2 | - | J2 |
| S12-r1, S12-r2 | - | - |
| S13-r1 | - | - |
| S13-r2 | no_qr_section | J1 |
| S14-r1 | - | J1 |
| S14-r2 | - | - |

What the change fixed: both S12 specs carry the section, cite IDs and list ADR-0004 under
"Blocked by"; both S11 runs suggest the skill instead of running it ("Whether encrypted exports
should become a requirement. If so, run `/add-requirements`." S11-r1).

Loopholes:

1. **Requirement and scenario IDs stand in for goals** (S11-r1 J1, J2, `goals_cited`): the run
   read the reference and argued from "R-3 and QS-2 require a stdlib-only program that works
   with no install steps." but named no `QG-n`.
2. **An option tied to no goal is still offered** (S11-r1, S11-r2 J2): "3. Write plain Markdown
   into `DIR` and encrypt the drive" cites no quality goal in either run.
3. **The plain-project spec grows the section** (S13-r2, regression): the template's section
   is visible in every project, and the run filled it: "Not applicable. The project has no
   `docs/architecture/arc42.md`, so there are no R-, QS-, or ADR IDs to cite."
4. **The pointer primes ADR talk in a plain project** (S14-r1, regression): "There are no
   architecture docs, so the design doesn't have to fit an existing ADR set." The pointer
   names "quality goals, requirements and ADRs" in every project.

Gate: not met. Task 4 (one loophole round) follows.

## Loophole round: skills at `b7e6c09` (2026-11-22, 2 runs each, clean isolation)

Changes: both pointers now name only the condition and the reference ("If
`docs/architecture/arc42.md` exists, read …"); the spec's Quality Requirements section and its
red flag moved from the template into `spec-and-plan/references/quality-requirements.md`;
`design-dialogue/references/architecture.md` gained a slot line for the touched goals, a slot
form for each option, the rule that `R-n` and `QS-n` do not stand in for a goal, and its red
flags (worded generally, not for this scenario). All eight runs were replaced.

| run | failed checks | failed criteria | read the reference |
|---|---|---|---|
| S11-r1 | - | - | yes |
| S11-r2 | goals_cited, add_requirements_suggested | J1, J3 | no |
| S12-r1, S12-r2 | - | - | yes |
| S13-r1, S13-r2 | - | - | - |
| S14-r1, S14-r2 | - | - | - |

Closed: the controls no longer raise quality goals, arc42 or ADRs (S13, S14, 4 of 4); S11-r1
opened with "**Quality goals this touches:**" and tied every option to a `QG-n`; S12 still
passes with the section in a reference of its own.

Open loophole: **the bare pointer did not fire** (S11-r2). The run read arc42, the ADRs and
the code with `cat`, but never `references/architecture.md`, and fell back to the `main`
behaviour: "Encryption is not in the Python standard library. Requirement R-3 and the section 2
constraint allow only the standard library." In the first attempt, whose pointer said what the
reference covers, both S11 runs read it. The pointer lost its "what the material is" half
(`writing-for-agents` › Context pointers). Candidate fix for a later round: state what the
reference changes without naming the concepts that primed the controls, for example "…: it
changes how the dialogue runs in a set-up project", and re-run S11 and S14.

Gate: not met for S11 (1 of 2 runs); one round spent, so S11-r2 stands as an open loophole.
GREEN credit: S11 `goals_cited`, `add_requirements_suggested`, J1–J3 (1 of 2 runs after the
round, 2 of 2 in the first attempt for `add_requirements_suggested`); S12 `qr_section`,
`qr_cites`, J2 (2 of 2 in both rounds).

## Review fix pass: skills at `dcac0c7` (2026-11-22, 2 runs each, clean isolation)

The whole-ticket review (fresh Opus reviewer) found two Important issues and two Minors that
were re-graded Important because they inflate this campaign's results:

- A spec blocked on a proposed ADR could still be published as `ready-for-agent`. New check
  `status_blocked` (self-test `S12-ready`): both `main` runs fail it ("Status: ready-for-agent
  (blocked on ADR-0004 acceptance; …)", S12-r1); `quality-requirements.md` now requires
  `Status: blocked (ADR-nnnn)` and no `ready-for-agent` label while **Blocked by** is non-empty.
- The bare pointer did not fire (S11-r2 above): it now adds "it changes how this dialogue
  runs", with a red-flag row for reading arc42 alone.
- Red flags and examples quoted the scenario ("ADR-0004", "encryption at rest"); now general.

All eight runs were replaced.

| run | failed checks | failed criteria | read the reference |
|---|---|---|---|
| S11-r1, S11-r2 | - | J4 | yes |
| S12-r1, S12-r2 | - | - | yes |
| S13-r1 | - | - | - |
| S13-r2 | - | J1 | - |
| S14-r1, S14-r2 | - | - | - |

Closed: the pointer fired in both S11 runs, which now name the touched goals, tie every option
to a `QG-n` and suggest `/add-requirements`; both S12 specs read "Status: blocked …".

Open after the one fix pass (no second pass):

1. **Options build on proposed ADR-0004** (S11-r1, S11-r2 J4, regression: both `main` runs
   passed J4). The goals slot asks how the change bears on each goal, and both runs answered
   with ADR-0004's mechanism: "QG-1 Reliability (each export file is written atomically per
   ADR-0004, …)" (S11-r1); "Serves … QG-1, since … each write goes through ADR-0004's
   temp-file-and-rename." (S11-r2). Candidate fix: in the goals line and the options, cite only
   accepted ADRs; a proposed ADR appears only as an open decision with what changes if it is
   rejected.
2. **The plain-project spec run mentions arc42** (S13-r2 J1): "The repo has no tracker config,
   glossary, or arc42 docs, so this was the local-file path." The gated pointer names the file in
   every project; S13-r1 said the same in mid-run text and passed. A judge-strict borderline,
   recorded as a cost of the gated pointer.
