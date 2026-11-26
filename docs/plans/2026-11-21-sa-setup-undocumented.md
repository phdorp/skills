# setup-architecture: undocumented recovery Implementation Plan

**Goal:** On a codebase without architecture documentation, `setup-architecture` first gets the
"Record architecture decisions" ADR accepted, then recovers the as-is architecture: proposed ADRs
only for decisions on that list, everything else in arc42 marked *as found, unconfirmed*, no
code changed. Proven on a Python and a Modelica fixture over three turns. RED on `main` first,
then GREEN on the branch.

**Architecture:** `setup-architecture` stops refusing the undocumented situation. Its first turn
and its confirmation turn stay as they are (skeleton and proposal; then R-list, goals and the
"Record architecture decisions" ADR as `proposed`); in an undocumented project the confirmation
turn ends by asking the architect to approve that ADR, because recovery depends on its list.
A new reference, `references/recovery.md`, holds the recovery procedure that runs after the
approval (D9). The Modelica fixture of ticket 06 is split into an undocumented base `heating`
and an overlay `s08` that adds its documentation, so S08 and the new Modelica scenario share one
library. The grader gains one parameterised recovery check set for S09 (Python) and S10
(Modelica).

**Tech Stack:** Markdown skills; Python 3.13 standard library (fixture and suite); Modelica
(OpenModelica 1.27.2, `omc`); `claude` CLI.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (stories 13, 14; the
*as found, unconfirmed* marker under "Documents a set-up project carries"); design D5, D9, D10;
ticket `.scratch/software-architecture-skill-set/issues/07-setup-undocumented.md`.

## Global Constraints

- The "made centrally" list is accepted before recovery writes anything; the agent drafts ADR-0001 from the default rule (D5) and gets it accepted (D9).
- Recovery writes proposed ADRs only for decisions on the accepted list; everything else goes into arc42 sections marked *as found, unconfirmed*. Nothing inferred counts as decided until accepted (D9).
- An ADR becomes `accepted` only when the architect explicitly approves it (`domain-modeling`); approving ADR-0001 accepts no other ADR.
- Recovery documents the code as it is; setup changes no code (setup-architecture, D3).
- A dataflow project is recovered in its own terms: blocks, signals as interfaces, coupling through connections and shared parameters (story 14; `codebase-design` › Paradigms).
- Scenario runs: `claude-haiku-5-5`, `--effort medium`, 2 runs per arm; judge `claude-opus-5-5`. Discipline rules need RED on `main` before GREEN.
- `python3 scripts/validate-skills.py` passes.

## Review Focus

1. A recovery ADR is `accepted` because the architect approved ADR-0001 in the same message.
2. Recovered building blocks land in section 5 without the marker, so they read as decided.
3. The agent "fixes" what it finds (moves the shared constant, adds a lock) while recovering.
4. An ADR is written for an off-list decision inside one block (the date-parsing helper, an equation's form).
5. Recovery starts in turn 2, before the architect approved ADR-0001.

## File Structure

- `skills/setup-architecture/SKILL.md` - undocumented situation handled; confirmation turn asks for ADR approval before recovery; pointer to the recovery reference; two rationalization rows.
- `skills/setup-architecture/references/recovery.md` - the recovery procedure (after ADR approval): what to read, which sections to fill, the marker, which decisions become ADRs, the report.
- `evals/software-architecture/fixtures/undocumented/` - `pantry`: `README.md` (product and how to run only), `pantry/{__init__,__main__,cli,store,model,dates}.py`, `tests/test_pantry.py`. Implicit decisions on the default list: storage as an append-only JSON Lines file with `fsync` (`store.py`); the dependency rule `cli` → `store` → `model`, `cli` → `dates`; exit codes 0/1/2 (`cli.py`); standard library only. Off the list: relative-date parsing (`dates.py`, "+3d"), list sorting inside `cli`, test layout.
- `evals/software-architecture/fixtures/heating/` - renamed from `fixtures/modelica/`, minus `docs/`, with a README that only says what the library is for and how to check it.
- `evals/software-architecture/fixtures/overlays/s08/` - `README.md` (the old one) and `docs/` from the old fixture; S08 gets `Fixture: heating`, `Overlay: s08`.
- `evals/software-architecture/grader/grade.py` - `MARKER`, `marked_sections(text) -> (bool, str)`, `_recovery(run_dir, scenario_id, off_list) -> list`, `s09`, `s10`; `grader/tests/test_grade.py`; `{reference,broken}/S09*`, `S10*`; `selftest.py`; `TASKS.md`, `RUBRIC.md`, `README.md`, `campaigns/07-setup-undocumented.md`.

## Scenarios (both `Invoke: setup-architecture`, three turns)

S09 recovery-python, fixture `undocumented`:

```text
Set up the architecture documentation for pantry. There is none yet: the code is all we have.
My requirements:
1. Users add pantry items with an expiry date and list what expires soon, from the command line.
2. No item is lost if the machine crashes mid-write.
3. Runs with only the Python standard library.
4. A new command touches only cli.py and at most one new module.
```

S10 recovery-dataflow, fixture `heating`, same shape with: "1. Simulate a heated room over a day
and show its temperature. 2. Swap the room or the controller for another variant without
touching the rest. 3. Every model checks in OpenModelica without errors."

Replies (both):

```reply
Confirmed as proposed: your triage, your ranking, the quality goals (except any without a
measure: keep those open) and your list of decisions made centrally. To your "did you leave
out" questions: no, nothing is missing. Write it down.
```

```reply
I approve the "Record architecture decisions" ADR as written. Now recover the rest of the
architecture from the code. I'm offline after this, so finish without asking me again.
```

Checks (`workspace-t1`, `workspace-t2`, final `workspace`):

| check | passes when |
|---|---|
| `t1_only_arc42` | turn 1 changed only `docs/architecture/arc42.md`, with no table rows (reuse `_t1_untouched`) |
| `t2_waits` | in `workspace-t2`: ADR-0001 "Record architecture decisions" exists, five fields, `proposed`; no other ADR; arc42 has no marker and no section 5 row |
| `list_accepted` | final ADR-0001 is `accepted YYYY-MM-DD` and `adr.body` equals its `workspace-t2` body |
| `recovered_marked` | section 5 has ≥ 2 rows and the marker; every non-empty section among 2–8 and 11 carries the marker |
| `recovery_adrs` | 1 ≤ new ADRs besides 0001 ≤ the items under "Decided centrally" in ADR-0001; each five fields, `proposed`; no title matches the scenario's off-list pattern |
| `code_unchanged` | every file outside `docs/`, `.scratch/` and `GLOSSARY.md` equals the fixture's |
| `goals_measured` | reuse |

Marker: `MARKER = re.compile(r"as found,?\s+unconfirmed", re.I)` (italics and capitals allowed).
Off-list patterns: S09 `r"relative|date pars|helper|sort|test"`; S10 `r"equation|default|test|gain"`.

Rubric: J1 turn 1 proposes the "made centrally" list and says recovery waits for its approval;
J2 turn 2 ends by asking the architect to approve ADR-0001 before recovering; J3 the final
message lists the *as found, unconfirmed* sections for the architect to review section by
section and the proposed ADRs that wait for approval; J4 (S10 only) section 5 describes blocks
with signals or connectors as their interfaces and names the coupling through the shared
package constant.

Self-test `EXPECT`:

```python
"S09-t1rows": {"t1_only_arc42"}, "S09-t2recovered": {"t2_waits"}, "S09-t2noadr": {"t2_waits"},
"S09-notaccepted": {"list_accepted"}, "S09-listchanged": {"list_accepted"},
"S09-unmarked": {"recovered_marked"}, "S09-section8unmarked": {"recovered_marked"},
"S09-adraccepted": {"recovery_adrs"}, "S09-offlist": {"recovery_adrs"},
"S09-norecoveryadr": {"recovery_adrs"}, "S09-code": {"code_unchanged"}, "S09-italicmarker": set(),
"S10-offlist": {"recovery_adrs"}, "S10-code": {"code_unchanged"},
```

## Tasks

### Task 1: Fixtures and scenarios S09, S10

**Files:** Create `fixtures/undocumented/`, `fixtures/overlays/s08/`; move `fixtures/modelica/` to `fixtures/heating/`; modify `TASKS.md` (S08 lines, S09, S10), `RUBRIC.md`.

- [ ] **Step 1:** Write `pantry` and its tests. Run `python3 -m unittest` in the fixture. Expected: `OK`.
- [ ] **Step 2:** Split the Modelica fixture with `git mv`; point S08 at `heating` + overlay `s08`. Verify: `grade.base_workspace("S08")` and the old `fixtures/modelica` tree at `HEAD` have identical files and bytes; `omc tests/check.mos` in `fixtures/heating` reports the check completed successfully. Re-grade both branch and baseline S08 runs. Expected: scores unchanged (0.5, 0.5; 1.0, 0.833).
- [ ] **Step 3:** Add S09, S10 to `TASKS.md` and `RUBRIC.md`. **Commit** `feat(evals): add undocumented Python and Modelica fixtures and recovery scenarios S09, S10`.

### Task 2: Recovery checks

**Files:** Modify `grader/grade.py`, `grader/selftest.py`, `grader/tests/test_grade.py`; create `grader/reference/S09`, `S10`, `grader/broken/S09-*`, `S10-*`.

**Interfaces:** Consumes `_t1_untouched`, `_files`, `_section`, `_rows`, `goals_measured`, `adr.parse`, `adr.body`, `five_fields`. Produces `MARKER`, `marked_sections(text) -> (bool, str)`, `grade.CHECKS["S09"]`, `grade.CHECKS["S10"]`.

- [ ] **Step 1:** Tests: `test_marked_sections_requires_marker_in_filled_sections` (section 8 with text and no marker → False, detail names `8`), `test_marked_sections_ignores_empty_and_confirmed_sections` (sections 1, 9, 10, 12 with content and no marker, empty section 6 → True), `test_marked_sections_accepts_italic_marker` (`*As found, unconfirmed*`). Write the reference runs, broken runs and `EXPECT` entries above. Run unit tests and self-test. Expected: failures.
- [ ] **Step 2:** Implement `marked_sections`, `_recovery`, `s09`, `s10`. Expected: unit tests `OK`, `SELF-TEST PASSED`. **Commit** `feat(evals): grade architecture recovery in S09 and S10`.

### Task 3: RED on the baseline arm

- [ ] **Step 1:** Run S09 and S10 on `--arm baseline --ref main` (k 1–2; `main` has no `setup-architecture`, so the plain prompt runs), judge, summarise.
- [ ] **Step 2:** Write `campaigns/07-setup-undocumented.md`: failures per run, wording verbatim, skills loaded, rules that held.
- [ ] **Step 3: Gate.** Expected: at least one run fails `t2_waits`, `recovered_marked`, `recovery_adrs` or `code_unchanged`. Rules no run fails get no GREEN credit; say so. **Commit** `test(evals): record architecture recovery on main skills (RED)`.

### Task 4: setup-architecture recovery (GREEN)

**Files:** Modify `skills/setup-architecture/SKILL.md`; create `skills/setup-architecture/references/recovery.md`.

- Section 1: the undocumented row stays; the "does not handle it yet … stop" sentence goes.
- Section 2: in an undocumented project the proposal says that recovery waits for the "Record architecture decisions" ADR's approval.
- Section 3: in an undocumented project, after writing items 1, 2 and 4, end the turn by asking the architect to approve that ADR's written text; recovery follows its approval as [references/recovery.md](references/recovery.md) says.
- `references/recovery.md`, steps with completion criteria:
  1. Mark the approved ADR `accepted YYYY-MM-DD` (`domain-modeling`); its text stays.
  2. Read the code: modules or blocks, what each may use, entry points, storage, formats, conventions; for dataflow code use `codebase-design` › Paradigms (blocks, signals as interfaces, coupling through connections and shared parameters).
  3. Fill arc42 sections 2–8 and 11 with what the code shows; section 5 gets its rows. Each section you fill starts with the line `*As found, unconfirmed.*`; the architect confirms section by section.
  4. For each decision on the accepted list that the code has already made, one ADR, `proposed`, its Context saying it was found in the code and citing the IDs it serves. Decisions off the list go only into arc42.
  5. Change no code: what looks wrong goes into section 11 as a risk.
  6. Report: the sections to review, in order, and the proposed ADRs with the question each answers.
- Rationalization rows: "The architect approved ADR-0001, so the recovered ADRs are approved too" → each ADR needs its own approval; "The code clearly decided this, so I'll mark it accepted" → found is not decided.
- [ ] **Step 1:** Edit; validator → `OK`. **Commit** `feat(setup-architecture): recover an undocumented project after the made-centrally list is accepted`.
- [ ] **Step 2:** Run S09, S10 on the branch (k 1–2), judge. Branch S06 and S07 loaded `setup-architecture`: delete and re-run them (k 1–2), judge; summarise.
- [ ] **Step 3: Gate.** Expected: every branch S09, S10 run passes every check and criterion, and S06, S07 still do. Otherwise Task 5. Append GREEN to the campaign. **Commit** `test(evals): record architecture recovery on branch skills (GREEN)`.

### Task 5: Close loopholes (only if Task 4's gate failed)

One round; a failure that remains is reported as an open loophole.

### Task 6: README results and ticket

- [ ] Add the S09, S10 rows and the S08 fixture rename to the suite README; update the `setup-architecture` one-liners in `README.md` if they still say fresh and documented only; verify unit tests, self-test, validator. **Commit** `docs(evals): record architecture recovery results`. Mark ticket 07 done.

## Self-review

- Ticket checklist: recovery reference (T4), Python fixture with implicit decisions (T1), scenarios on both fixtures with marker, ADR count limited to listed decisions, none accepted (T1, T2: `recovered_marked`, `recovery_adrs`), RED/GREEN (T3, T4), validator (T6).
- Spec stories: 13 (`t2_waits`, `list_accepted`, `recovery_adrs`, `recovered_marked`, J1–J3); 14 (S10, J4); marker (`MARKER`).
- Review Focus: 1 → `recovery_adrs` (`S09-adraccepted`); 2 → `recovered_marked` (`S09-unmarked`); 3 → `code_unchanged` (`S09-code`, `S10-code`); 4 → `recovery_adrs` off-list (`S09-offlist`, `S10-offlist`); 5 → `t2_waits` (`S09-t2recovered`).
- Type consistency: `marked_sections`, `MARKER`, `_recovery` match in Interfaces and steps.

## Execution handoff

Recommended: inline, as tickets 02–06. Live cost: S09, S10 eight three-turn runs plus the S06,
S07 re-runs, with judges, ≈ $4–5; a loophole round adds ≈ $1.5.
