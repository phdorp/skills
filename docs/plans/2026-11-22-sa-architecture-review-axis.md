# code-review: Architecture axis Implementation Plan

**Goal:** In a set-up project, code review reports a third axis, Architecture, from its own
sources: accepted ADRs, arc42 section 8 rules, the quality scenarios the change touches, and
traceability (an accepted ADR naming no requirement or quality goal is a finding, except
legacy ADRs). The smell baseline gains Long Method and Large Class, and marks OO-only smells
"(OO)" with a dataflow counterpart where one exists. RED on `main` first, then GREEN.

**Architecture:** `code-review/SKILL.md` gets one gated pointer, in the form ticket 08 learned:
the condition plus what the reference changes ("If `docs/architecture/arc42.md` exists, read
[references/architecture-axis.md](references/architecture-axis.md) before step 4: it adds a
third axis with its own reviewer"). The reference holds the sources, the four checks, the
`## Architecture` report section and how aggregation changes. `reviewer-prompt.md` gains an
Architecture block, which the reference tells the reviewer to fill. Projects without arc42 keep
two axes (D15). The smell edits live in `standards-and-smells.md` and `reviewer-prompt.md`'s
baseline slot, which is still their one owner (`codebase-design` points there).

**Tech Stack:** Markdown skills; Python 3.13 standard library (grader); `claude` CLI.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (stories 42, 43, 44;
"Changed skills" › `code-review`); design D12, D15, D16; ticket
`.scratch/software-architecture-skill-set/issues/10-architecture-review-axis.md`.

## Global Constraints

- The Architecture axis runs only when `docs/architecture/arc42.md` exists (D15); otherwise the
  review has two axes and says nothing about architecture setup.
- Its sources are accepted ADRs (`accepted …`, `accepted (legacy)`, or no Status: legacy, D16),
  arc42 section 8, the section 10 scenarios the change touches, and section 1's IDs. A
  `proposed` or `rejected` ADR is not a rule; a change that relies on one is reported as
  depending on an open decision.
- Traceability: an accepted ADR in the change, or one it relies on, whose Context names no
  `R-n`, `QG-n` or `QS-n` is a finding; a legacy ADR (`accepted (legacy)` or no Status) is not.
- Each axis keeps its own reviewer and its own report section; the closing line names the worst
  issue per axis.
- The review stays read-only: no file in the workspace changes.
- Scenario runs: `claude-haiku-5-5`, `--effort medium`, 2 runs per arm; judge `claude-opus-5-5`.
  RED on `main` before GREEN; a rule no baseline run fails gets no GREEN credit. One loophole
  round.
- `python3 scripts/validate-skills.py` passes.

## Review Focus

1. The ADR-0003 breach is reported under Standards or Spec, or not at all.
2. The review cites a proposed ADR as a rule, or skips an accepted one.
3. The new accepted ADR that names no requirement or goal passes unremarked.
4. A plain project's review gains an Architecture section or setup advice (D15).
5. The reviewer edits code.

## File Structure

- `skills/code-review/SKILL.md` - "The two axes" names the gated third axis by pointer; step 4 and step 5 say "each axis".
- `skills/code-review/references/architecture-axis.md` - sources, checks, report form, aggregation.
- `skills/code-review/references/reviewer-prompt.md` - Architecture block (sources, checks); Long Method, Large Class and the (OO) marks reach it through `{SMELL_BASELINE}`.
- `skills/code-review/references/standards-and-smells.md` - Long Method, Large Class; "(OO)" marks with dataflow counterparts.
- `evals/software-architecture/` - `grader/run.py` (`Change:` line: an overlay committed as a second commit), `fixtures/overlays/s19/`, `s20/`, `TASKS.md` S19–S20, `RUBRIC.md`, `grader/grade.py`, tests, reference and broken runs, `selftest.py`, `README.md`, `campaigns/10-architecture-review-axis.md`.

## Scenarios

A review needs a commit range, and `prepare_workspace` makes one commit. `run.py` learns
`Change: <overlay> <subject>`: after the fixture commit, that overlay is copied in and
committed with that subject, so `HEAD~1..HEAD` is the change under review.
`grade.base_workspace` applies it too (the agent first saw it).

S19 review-setup: `Fixture: setup`, `Change: s19 feat: export notes as JSON`,
`Invoke: code-review`. The change:
- adds `notes export`, which opens the SQLite file in `notes/cli.py` with `sqlite3` (breaks
  accepted ADR-0003; touches QS-3: a storage swap now changes `cli.py`) and prints a failure as
  a Python traceback (breaks arc42 section 8's error rule);
- adds `docs/adr/0004-export-as-json-lines.md`, `accepted 2026-11-20`, whose Context names no
  `R-n`, `QG-n` or `QS-n` (traceability);
- adds `docs/specs/export.md` (the spec: "`notes export` prints every note as one JSON line"),
  which the change implements, so the Spec axis has a source and little to say.

```text
Review the last commit (HEAD~1..HEAD) against main's state before it. The spec is
docs/specs/export.md. Report your findings; don't change any files.
```

S20 review-plain (control, D15): `Fixture: plain`, `Change: s20 feat: …` (a `tally` command
that adds a flag, with one Long Method of ~40 lines), `Invoke: code-review`, the same prompt
with its own spec. No arc42.

Checks:

| check | scenario | passes when |
|---|---|---|
| `read_only` | S19, S20 | the workspace equals the base (fixture plus change) |
| `architecture_section` | S19 | the last message has a heading whose text is `Architecture` |
| `adr_under_architecture` | S19 | that section cites ADR-0003 (`ADR-0003`, `ADR-3`, `0003`) |
| `section8_under_architecture` | S19 | that section names the error rule (`stderr` or `section 8` or `§8`) |
| `qs_under_architecture` | S19 | that section cites `QS-3` |
| `trace_under_architecture` | S19 | that section cites ADR-0004 |
| `no_architecture_section` | S20 | no heading whose text is `Architecture`, and no `arc42` in the last message |

Rubric: S19 J1 the ADR-0003 breach is a finding under Architecture, citing the ADR as its
source, not under Standards or Spec; J2 ADR-0004's missing requirement or goal is reported as a
traceability finding; J3 the review names QS-3 as the scenario the change touches and says
how; J4 the axes are reported apart, and the closing line names the worst issue per axis.
S20 J1 the review has Standards and Spec only and does not suggest setting up an
architecture; J2 the Standards findings name the long function (Long Method or an equivalent
description) as a judgement call. S20 J2 tests the smell baseline; S20 J1 is the D15 control.

Self-test `EXPECT` (reference passes all):

```python
"S19-standards": {"architecture_section", "adr_under_architecture", "section8_under_architecture",
                  "qs_under_architecture", "trace_under_architecture"},  # all under ## Standards
"S19-noqs": {"qs_under_architecture"}, "S19-notrace": {"trace_under_architecture"},
"S19-edited": {"read_only"},
"S20-archsection": {"no_architecture_section"}, "S20-arc42": {"no_architecture_section"},
"S20-edited": {"read_only"},
```

## Tasks

### Task 1: `Change:` line in run.py

**Files:** Modify `grader/run.py`, `grader/grade.py` (`base_workspace`), `grader/tests/test_run.py`, `README.md` (Contents).

**Interfaces:** Produces `Scenario.change: tuple[str, str] | None` (overlay, subject); `prepare_workspace(fixture_dir, overlay_dir=None, change=None)` where `change=(dir, subject)`.

- [ ] **Step 1:** Tests `test_load_scenarios_reads_change`, `test_prepare_workspace_commits_change` (two commits; `HEAD~1..HEAD` touches only the change's files; subject as given). Expected: fail.
- [ ] **Step 2:** Implement; `base_workspace` applies the change dir. Expected: unit `OK`, `SELF-TEST PASSED`. **Commit** `feat(evals): commit a scenario's change on top of its fixture`.

### Task 2: Scenarios S19–S20 and their checks

**Files:** Modify `TASKS.md`, `RUBRIC.md`, `grader/grade.py`, `grader/selftest.py`, `grader/tests/test_grade.py`; create `fixtures/overlays/s19/`, `s20/`, `grader/reference/S19`–`S20`, `grader/broken/S19-*`, `S20-*`.

**Interfaces:** Produces `section(text, heading) -> str | None` (the body under a Markdown heading whose text is `heading`, up to the next heading of the same or higher level), `CHECKS["S19"]`, `["S20"]`.

- [ ] **Step 1:** Test `test_section_*` (`## Architecture`, `### Architecture`, `**Architecture**` is not a heading, stops at the next same-level heading); reference and broken runs, `EXPECT`; the fixture tests still pass with each change applied. Expected: failures.
- [ ] **Step 2:** Implement. Expected: unit `OK`, `SELF-TEST PASSED`. **Commit** `feat(evals): add architecture review scenarios S19-S20`.

### Task 3: RED on the baseline arm

- [ ] **Step 1:** Run S19, S20 on `--arm baseline --ref main` (k 1–2), judge, summarise.
- [ ] **Step 2:** Write `campaigns/10-architecture-review-axis.md`: failures per run, wording verbatim, rules that held.
- [ ] **Step 3: Gate.** Expected: every S19 run fails `architecture_section` (`main` has two axes). The checks and criteria that `main` passes get no GREEN credit. **Commit** `test(evals): record architecture review on main skills (RED)`.

### Task 4: Skill changes (GREEN)

**Files:** Modify `skills/code-review/SKILL.md`, `references/reviewer-prompt.md`, `references/standards-and-smells.md`; create `skills/code-review/references/architecture-axis.md`.

- `SKILL.md` › "The two axes", after the Spec bullet: "If `docs/architecture/arc42.md` exists, read [references/architecture-axis.md](references/architecture-axis.md) before step 4: it adds a third axis with its own reviewer." Steps 4–5 say "each axis" instead of "both"; the aggregate step names the sections the review has.
- `references/architecture-axis.md`, each section with a completion criterion:
  1. **Sources:** arc42 sections 1 (IDs), 8 and 10; every ADR in the directory section 9 links, with its status. Accepted means `accepted …`, `accepted (legacy)` or no Status (legacy, per `domain-modeling`). Proposed and rejected ADRs are not rules.
  2. **Checks:**
     - conformance with each accepted ADR the change's area falls under;
     - every section 8 rule;
     - quality scenarios: each `QS-n` whose stimulus or response the change bears on, and whether the change keeps its measure;
     - traceability: an accepted, non-legacy ADR in the change, or one it relies on, whose Context names no `R-n`, `QG-n` or `QS-n`.

     A change that relies on a proposed ADR is a finding: it depends on an open decision.
  3. **Report:** each finding cites its source (ADR number, "arc42 §8: <rule>", `QS-n`), quotes the hunk and gives the fix; severity as in the other axes.
  4. **Dispatch and aggregate:** a third reviewer with the Architecture block of `reviewer-prompt.md`; `## Architecture` beside `## Standards` and `## Spec`; a breach of an accepted ADR or a §8 rule is reported here, not under Standards.
  - Red flags:
    - "The ADR breach is a coding-standard breach" → "ADRs and §8 rules are Architecture's sources. Report it there."
    - "The ADR is proposed, but the change follows it, so it conforms" → "A proposed ADR is not a rule. Report that the change depends on an open decision."
- `reviewer-prompt.md`: `{AXIS}` gains "Architecture"; a `## Architecture  <!-- Architecture axis only -->` block with `{ARCHITECTURE_SOURCES}` and the four checks; "What to check" gains an Architecture list.
- `standards-and-smells.md`:
  - Long Method: "a function so long that its parts need comments or names of their own" → extract the parts into named functions.
  - Large Class: "a class or module holding many unrelated fields or responsibilities" → split it along its responsibilities.
  - "(OO)" marks with dataflow counterparts where one exists:
    - Feature Envy (OO) → dataflow: a block reading another block's internal variables instead of its outputs;
    - Refused Bequest (OO) → none;
    - Message Chains (OO) → dataflow: a connection reaching through nested sub-blocks;
    - Middle Man (OO) → dataflow: a pass-through block;
    - Repeated Switches: also imperative, no mark.

  The counterparts use `codebase-design`'s terms.
- [ ] **Step 1:** Edit; validator → `OK`. **Commit** `feat(code-review): add the Architecture axis in set-up projects`.
- [ ] **Step 2:** Run S19, S20 on the branch (k 1–2), judge, summarise. Re-run S01–S18 branch runs only where a transcript loads or reads `code-review` (grep first; record the reasoning).
- [ ] **Step 3: Gate.** Expected: every branch S19, S20 run passes every check and criterion that `main` failed. Otherwise Task 5. Append GREEN to the campaign. **Commit** `test(evals): record architecture review on branch skills (GREEN)`.

### Task 5: Close loopholes (only if Task 4's gate failed)

One round; a failure that remains is reported as an open loophole.

### Task 6: README results and ticket

- [ ] Add S19–S20 rows and a campaign line to the suite README; add known gaps:
  - a legacy ADR's traceability exemption has no scenario;
  - the "(OO)" marks and Large Class are not exercised.

  Verify unit tests, self-test and validator. **Commit** `docs(evals): record architecture review results`. Mark ticket 10 done.

## Self-review

- Ticket checklist:
  - its own sources and report section, skipped when not set up (Task 4, S20 control);
  - an accepted-ADR breach found under Architecture (S19 `adr_under_architecture`, J1);
  - RED/GREEN (Tasks 3, 4);
  - validator (Task 6).
- Spec:
  - story 42: `adr_under_architecture`, `section8_under_architecture`, `qs_under_architecture`, J1, J3, J4;
  - story 43: `trace_under_architecture`, J2 (the legacy exemption is text only, a known gap);
  - story 44: S20 J2 for Long Method; the (OO) marks are text only, a known gap;
  - D15: S20 `no_architecture_section`, J1.
- Review Focus:
  - 1 → `S19-standards`, J1;
  - 2 → text and the final review (no proposed ADR in S19's area; a known gap);
  - 3 → `S19-notrace`, J2;
  - 4 → `S20-archsection`, `S20-arc42`;
  - 5 → `S19-edited`, `S20-edited`.
- Type consistency: `section`, `Scenario.change` match Interfaces and checks.

## Execution handoff

Recommended: inline, as tickets 02–09. Live cost: 8 runs with judges ≈ $2.5 (the review
dispatches reviewer subagents, so runs cost more than earlier scenarios); a loophole round ≈ $1;
a review fix round ≈ $1.
