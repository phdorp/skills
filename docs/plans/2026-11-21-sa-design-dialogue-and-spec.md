# design-dialogue and spec-and-plan in a set-up project Implementation Plan

**Goal:** In a project with `docs/architecture/arc42.md`, `design-dialogue` reads arc42 and the
ADRs first, asks which quality goals a change touches, offers structural choices as 2–3 options
tied to quality goals, and suggests `add-requirements` for a new system-level requirement;
`spec-and-plan`'s spec carries a Quality Requirements section and never relies on a proposed
ADR. Projects without arc42 see no change. RED on `main` first, then GREEN on the branch.

**Architecture:** Each skill gets one gated pointer: "If `docs/architecture/arc42.md` exists,
read `references/architecture.md`". The set-up behaviour lives in that reference, so a project
without setup loads none of it (D15). `design-dialogue/references/architecture.md` covers
reading, the quality-goal question, D7 options and the `add-requirements` suggestion;
`spec-and-plan/references/spec-template.md` gains a Quality Requirements section marked
"set-up projects only". Four scenarios: two in the set-up fixture, two controls in `plain`.

**Tech Stack:** Markdown skills; Python 3.13 standard library (grader); `claude` CLI.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (stories 31, 32, 41;
"Changed skills" › `design-dialogue`, `spec-and-plan`); design D7, D8, D15, D18; ticket
`.scratch/software-architecture-skill-set/issues/08-design-dialogue-and-spec-and-plan.md`.

## Global Constraints

- Architecture behaviour runs only when `docs/architecture/arc42.md` exists; other projects behave as today, apart from a single suggestion to run `setup-architecture` (D15).
- Structural choices: 2–3 options, each tied to the quality goals it serves or hurts, one recommended; an option that cannot be tied to a quality goal is not offered (D7, stories 31, 32).
- A new system-level requirement noticed in `design-dialogue` is suggested for `add-requirements`; the agent does not run it (D18).
- The spec's Quality Requirements section cites scenario IDs, ADRs and parent R-IDs, not copies; a spec never relies on a proposed ADR (story 41).
- `design-dialogue`'s approval gate stands: nothing is built or written before the design is approved.
- Scenario runs: `claude-haiku-5-5`, `--effort medium`, 2 runs per arm; judge `claude-opus-5-5`. RED on `main` before GREEN; a rule no baseline run fails gets no GREEN credit.
- `python3 scripts/validate-skills.py` passes.

## Review Focus

1. The agent runs `add-requirements` itself (or edits the R-list) instead of suggesting it.
2. An option is tied to a quality goal that does not exist (`QG-7`) or to none.
3. The spec presents proposed ADR-0004 as a settled rule ("writes are atomic per ADR-0004").
4. The spec copies scenario text (the QS-1 measure) instead of citing `QS-1`.
5. A project without arc42 gets quality-goal questions or a Quality Requirements section.

## File Structure

- `skills/design-dialogue/SKILL.md` - one gated pointer in "Look before you ask"; one rationalization row.
- `skills/design-dialogue/references/architecture.md` - set-up behaviour: what to read, the quality-goal question, structural options (D7), the `add-requirements` suggestion, proposed ADRs as open.
- `skills/spec-and-plan/SKILL.md` - gated pointer in "Explore first"; one red-flag row.
- `skills/spec-and-plan/references/spec-template.md` - "Quality Requirements" section (set-up projects only).
- `evals/software-architecture/` - `TASKS.md` S11–S14, `RUBRIC.md`, `grader/grade.py` (`s11`–`s14`, `turn_texts`, `skill_called`), `grader/tests/test_grade.py`, `grader/{reference,broken}/S11*`–`S14*`, `selftest.py`, `README.md`, `campaigns/08-dialogue-and-spec.md`.

## Scenarios

S11 dialogue-setup: fixture `setup`, overlay `s03` (proposed ADR-0004 atomic writes, ADR-0005), `Invoke: design-dialogue`, two turns.

```text
I want a `notes export DIR` command that writes every note as a Markdown file, so people can
open their notes in other editors. The exported files should be encrypted with a passphrase,
so a lost USB stick exposes nothing. Help me think this through before anything gets built.
```

```reply
One Markdown file per note, the title as the heading, the date in a small header. The user
names the folder. I'm offline after this: lay out the ways to build it and recommend one. I'll
pick tomorrow.
```

S12 spec-setup: fixture `setup`, overlay `s03`, `Invoke: spec-and-plan`, one turn. The prompt is
an approved design for `notes backup PATH` (copy the SQLite store to PATH), whose last line
reads "The backup file is written atomically, as ADR-0004 says." and ends "Write the spec. I'm
not available: where you would ask me, state the assumption in the spec."

S13 spec-plain: fixture `plain`, `Invoke: spec-and-plan`, one turn: an approved design for
`tally --ignore-case`, same closing line.

S14 dialogue-plain: fixture `plain`, `Invoke: design-dialogue`, one turn: "I want tally to also
count word pairs. Help me think this through before anything gets built."

Checks:

| scenario | check | passes when |
|---|---|---|
| S11 | `nothing_built` | `workspace-t1` and `workspace` equal the base (every file) |
| S11 | `arc42_read` | a turn-1 tool call names `arc42.md` |
| S11 | `goals_cited` | turn 2's assistant text cites ≥ 1 `QG-n`, all in arc42 |
| S11 | `add_requirements_suggested` | assistant text names `add-requirements` and no Skill call loads it |
| S12 | `one_spec` | exactly one new `docs/specs/*.md` |
| S12 | `qr_section` | the spec has a heading containing "Quality Requirements" |
| S12 | `qr_cites` | that section cites ≥ 1 `QS-n` and ≥ 1 `R-n`, all in arc42 |
| S12 | `not_copied` | the spec does not contain "0 unreadable stores in 100 trials" |
| S12 | `code_unchanged` | no file outside `docs/` and `.scratch/` changed |
| S13 | `one_spec`, `no_qr_section`, `no_architecture_docs`, `setup_suggested_at_most_once` | |
| S14 | `nothing_built`, `no_quality_goals` (no `QG-`, "quality goal", "25010" in assistant text), `setup_suggested_at_most_once` | |

Rubric: S11 J1 before laying out approaches the agent asks or states which quality goals the
change touches, by ID; J2 turn 2 offers 2–3 ways to build the export, each tied to the quality
goals it serves or hurts, and recommends one; J3 encryption is named as a new system-level
requirement and the agent suggests the architect run `add-requirements`; J4 the agent treats
ADR-0004 as proposed, not as a settled rule. S12 J1 the spec does not rely on proposed ADR-0004:
it marks the atomic-write dependency as waiting for its acceptance or drops it, and the final
message says so; J2 the Quality Requirements section names the parent R-ID and the scenarios
the work must keep. S13, S14 J1 no quality goals, arc42 or ADRs are raised.

Self-test `EXPECT`:

```python
"S11-built": {"nothing_built"}, "S11-noread": {"arc42_read"}, "S11-inventedgoal": {"goals_cited"},
"S11-ranaddreq": {"add_requirements_suggested"}, "S11-nosuggest": {"add_requirements_suggested"},
"S12-noqr": {"qr_section", "qr_cites"}, "S12-inventedqs": {"qr_cites"},
"S12-copied": {"not_copied"}, "S12-code": {"code_unchanged"}, "S12-twospecs": {"one_spec"},
"S13-qr": {"no_qr_section"}, "S13-arc42": {"no_architecture_docs"},
"S14-goals": {"no_quality_goals"}, "S14-built": {"nothing_built"},
```

## Tasks

### Task 1: Scenarios S11–S14 and their checks

**Files:** Modify `TASKS.md`, `RUBRIC.md`, `grader/grade.py`, `grader/selftest.py`, `grader/tests/test_grade.py`; create `grader/reference/S11`–`S14`, `grader/broken/S11-*`–`S14-*`.

**Interfaces:** Consumes `_files`, `base_workspace`, `_section`-style heading search, `adr.ids`, `_rows`, `assistant_text`, `HEADING`. Produces `turn_texts(run_dir) -> list[str]` (assistant text per turn, split at `### user`), `skill_called(run_dir, name) -> bool` (a `tool_use Skill` whose `skill` is `name` or `sa:name`), `CHECKS["S11"]`–`["S14"]`.

- [ ] **Step 1:** Tests `test_turn_texts_splits_at_user_headings` (two turns → two strings, tool calls excluded), `test_skill_called_matches_prefixed_and_plain` (`"skill": "sa:add-requirements"` → True; a Read of `add-requirements/SKILL.md` → False). Reference and broken runs, `EXPECT` above. Run unit tests and self-test. Expected: failures.
- [ ] **Step 2:** Implement. Expected: unit `OK`, `SELF-TEST PASSED`. **Commit** `feat(evals): add design-dialogue and spec scenarios S11-S14`.

### Task 2: RED on the baseline arm

- [ ] **Step 1:** Run S11–S14 on `--arm baseline --ref main` (k 1–2), judge, summarise.
- [ ] **Step 2:** Write `campaigns/08-dialogue-and-spec.md`: failures per run, wording verbatim, skills loaded, rules that held.
- [ ] **Step 3: Gate.** Expected: at least one S11 run fails `goals_cited` or J1–J3, and at least one S12 run fails `qr_section` or J1. S13, S14 are controls: they should pass on both arms and get no GREEN credit. **Commit** `test(evals): record dialogue and spec on main skills (RED)`.

### Task 3: Skill changes (GREEN)

**Files:** Modify `skills/design-dialogue/SKILL.md`, `skills/spec-and-plan/SKILL.md`, `skills/spec-and-plan/references/spec-template.md`; create `skills/design-dialogue/references/architecture.md`.

- `design-dialogue` › Look before you ask, new paragraph: "In a set-up project (`docs/architecture/arc42.md` exists), read [references/architecture.md](references/architecture.md) before your first message."
- `references/architecture.md`, sections with completion criteria:
  1. **Read:** arc42 sections 1 (R-list, quality goals), 5, 8, 10 and every ADR in the ADR directory, with its status.
  2. **Quality goals:** before laying out approaches, name the `QG-n` the change touches and ask the architect to confirm; a goal the change would hurt is named too.
  3. **Structural choices** (D7): when an approach turns on a paradigm, architectural pattern or design pattern, or a decision on the "Record architecture decisions" list, lay out 2–3 options, each with the `QG-n` it serves or hurts, and recommend one. Drop an option you cannot tie to a goal. The architect's choice becomes a proposed ADR through `domain-modeling`, after they choose.
  4. **New requirements:** a requirement the R-list does not cover, at system level, is named as such, with the suggestion "run `/add-requirements`". You suggest; the architect runs it.
  5. **Proposed ADRs** are open decisions: name them as such; the design does not build on them.
- `design-dialogue` red-flags row: "The change needs encryption, I'll add it to the requirements" → "Suggest `add-requirements`. The R-list changes only through it."
- `spec-and-plan` › Explore first: "In a set-up project (`docs/architecture/arc42.md` exists), also read the R-list, quality goals, section 10 and the ADRs, and fill the template's Quality Requirements section."
- `spec-template.md`, new section after Testing Decisions: "### Quality Requirements (set-up projects only)": the parent R-IDs; the `QS-n` the work must keep, cited by ID, not copied; the accepted ADRs it builds on. A decision the work needs that only a proposed ADR settles is listed as blocking, with the ADR number: the spec does not build on it until it is accepted.
- `spec-and-plan` red-flags row: "The design says ADR-0004, so the spec follows it" → "A proposed ADR is open. List it as blocking until the architect accepts it."
- [ ] **Step 1:** Edit; validator → `OK`. **Commit** `feat(design-dialogue,spec-and-plan): use quality goals and ADRs in a set-up project`.
- [ ] **Step 2:** Run S11–S14 on the branch (k 1–2), judge, summarise.
- [ ] **Step 3: Gate.** Expected: every branch S11, S12 run passes every check and criterion; S13, S14 pass. Otherwise Task 4. Append GREEN to the campaign. **Commit** `test(evals): record dialogue and spec on branch skills (GREEN)`.

### Task 4: Close loopholes (only if Task 3's gate failed)

One round; a failure that remains is reported as an open loophole.

### Task 5: README results and ticket

- [ ] Add S11–S14 rows and a campaign line to the suite README; verify unit tests, self-test, validator. **Commit** `docs(evals): record dialogue and spec results`. Mark ticket 08 done.

## Self-review

- Ticket checklist: gated on arc42 (T3 pointers; S13, S14 controls), set-up scenario with judge on goal question, options tied to goals, suggestion not invocation (S11 J1–J3, `add_requirements_suggested`), RED/GREEN (T2, T3), validator (T5).
- Spec: story 31 (S11 J2, `goals_cited`), 32 (J2; Focus 2), 41 (S12 `qr_section`, `qr_cites`, `not_copied`, J1), D15 (S13, S14), D18 suggestion (J3, `add_requirements_suggested`).
- Review Focus: 1 → `add_requirements_suggested` (`S11-ranaddreq`) and `nothing_built`; 2 → `goals_cited` (`S11-inventedgoal`), J2; 3 → S12 J1; 4 → `not_copied` (`S12-copied`); 5 → `no_quality_goals`, `no_qr_section` (`S14-goals`, `S13-qr`).
- Type consistency: `turn_texts`, `skill_called` match Interfaces and checks.

## Execution handoff

Recommended: inline, as tickets 02–07. Live cost: 16 runs (S11 two turns) with judges, ≈ $3–4;
a loophole round ≈ $1.5.
