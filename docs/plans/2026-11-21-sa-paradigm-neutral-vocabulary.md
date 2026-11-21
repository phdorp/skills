# Paradigm-neutral vocabulary and goal-driven architecture review Implementation Plan

**Goal:** `codebase-design` speaks for object-oriented, imperative and dataflow code alike and
carries the seminar's principles, GoF patterns and anti-patterns as short reference tables.
`improve-codebase-architecture`, run on a set-up project, ties every candidate to a quality
goal by ID and, once the architect accepts a change, records it as a `proposed` ADR instead of
changing code. Proven on a Modelica fixture that compiles with `omc`. RED on `main` first, then
GREEN on the branch.

**Architecture:** `codebase-design` gains a "Paradigms" section mapping module, interface,
seam, adapter, depth to object-oriented, imperative and dataflow code (signals and connectors
are the interface; coupling comes from connections and shared parameters), and three reference
files reached by pointer. Code smells stay in `code-review`'s smell baseline (ticket 10 marks
them "(OO)"); `codebase-design` points there. `improve-codebase-architecture` reads arc42 and
the project's ADR directory when set up (D15), adds a "Quality goal" field to every candidate,
drops candidates it cannot tie to a goal, and routes an accepted change through
`domain-modeling` as a `proposed` ADR. The suite gains fixture `modelica` (set up: arc42 with
goals, an accepted "Record architecture decisions" ADR) and two-turn scenario S08; the grader
reads the HTML report from the transcript's `Write` call, since the skill writes it outside the
workspace.

**Tech Stack:** Markdown skills; Modelica (OpenModelica 1.27.2, `omc`); Python 3.13 standard
library for the suite; `claude` CLI.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (stories 14, 31, 32,
44 (marks only), 45, 46); design D7, D13, D15; ticket
`.scratch/software-architecture-skill-set/issues/06-paradigm-neutral-vocabulary.md`.

## Global Constraints

- One vocabulary: `codebase-design` keeps module, interface, implementation, depth, seam, adapter, leverage, locality and maps them; it adds no paradigm-specific synonyms as glossary terms (D13).
- New text is paradigm-neutral. Existing object-oriented-only patterns and examples are marked "(OO)" with the dataflow counterpart where one exists, not rewritten (D13).
- Reference files are short tables that link out to sources; they may adapt the user's seminar summary without attribution (D13).
- `improve-codebase-architecture` changes behaviour only in a project with `docs/architecture/arc42.md`; elsewhere it behaves as today (D15).
- Every candidate names the quality goal(s) it serves by `QG-n`; a candidate tied to no goal is left out (D7, story 46). An accepted change becomes a `proposed` ADR through `domain-modeling`, never code in the same run (story 46, D6).
- The ADR-offer rule at `improve-codebase-architecture/SKILL.md:71` points to `domain-modeling` instead of restating it (deferred minor from ticket 02).
- Scenario runs: `claude-haiku-5-5`, `--effort medium`, 2 runs per arm; judge `claude-opus-5-5`. Discipline rules need RED on `main` before GREEN.
- `python3 scripts/validate-skills.py` passes.

## Review Focus

1. The report calls Modelica models "classes" and connections "method calls", or recommends inheritance and interfaces in the OO sense, so a dataflow project gets advice in the wrong paradigm.
2. A candidate cites a quality goal that does not exist (QG-7) to satisfy the "tie to a goal" rule.
3. After the architect accepts a candidate, the agent edits the `.mo` files in the same run.
4. The new ADR for the accepted change is `accepted` because the architect said "I accept".
5. The report is written into the repository instead of the temp directory, or not written at all.

## File Structure

- `skills/codebase-design/SKILL.md` - "Paradigms" section; pointers to the three references and to `code-review`'s smell baseline.
- `skills/codebase-design/references/principles.md` - SoC, DRY, KISS, YAGNI, SOLID, Law of Demeter, Rule of Three: rule and dataflow reading per row; the two tensions; links.
- `skills/codebase-design/references/patterns.md` - architectural patterns (layered, pipe-and-filter, plug-in, client-server, event-driven) and the 23 GoF patterns by group, OO-only ones marked "(OO)" with a dataflow counterpart where one exists; links.
- `skills/codebase-design/references/anti-patterns.md` - Blob, Lava Flow, Golden Hammer, Spaghetti Code, Analysis Paralysis with an OO and a dataflow sign each; links.
- `skills/improve-codebase-architecture/SKILL.md`, `HTML-REPORT.md` - arc42/ADR reading, "Quality goal" card field, ADR routing, pointer to `domain-modeling`.
- `evals/software-architecture/fixtures/modelica/` - `HeatingLib/package.mo`, `package.order`, `Interfaces.mo` (connectors), `Room.mo` (plant), `Thermostat.mo` (controller that reads the room's internal parameter `Room.C` through a shared global constant instead of its port, the friction), `System.mo` (connects them); `docs/architecture/arc42.md` (R-1…R-3, QG-1 Maintainability: modifiability, QG-2 Flexibility: replaceability, QG-3 Reliability: faultlessness, with QS rows); `docs/adr/0001-record-architecture-decisions.md` (accepted: connector definitions, units and the dependency rule `System` → blocks are decided centrally); `tests/check.mos` (loads the package, `checkModel(HeatingLib.System)`).
- `evals/software-architecture/grader/grade.py` - `written_file(run_dir, suffix) -> str | None` (content of the last `Write` tool call whose path ends with `suffix`), `s08`; `grader/tests/test_grade.py`; `{reference,broken}/S08*`; `TASKS.md`, `RUBRIC.md`, `README.md`, `campaigns/06-paradigm-neutral.md`.

## Scenario S08 architecture-scan-dataflow (fixture `modelica`, `Invoke: improve-codebase-architecture`)

Turn 1:

```text
Look for architecture improvements in HeatingLib. I'm not available for questions until you
have the report ready.
```

Reply:

```text
I accept your top recommendation. Take it forward; I'm offline after this, so finish without
asking me again.
```

Checks (`workspace-t1` after turn 1; the report from the transcript):

| check | passes when |
|---|---|
| `report_outside_repo` | a `Write` call wrote `architecture-review-*.html` outside the workspace; no `.html` file in `workspace-t1` or `workspace` |
| `goals_cited` | the report names at least one `QG-n`, and every `QG-n` it names exists in the fixture's arc42 |
| `t1_unchanged` | `workspace-t1` equals the fixture |
| `code_unchanged` | every `.mo` file of the final workspace equals the fixture's |
| `adr_proposed` | exactly one new ADR, `docs/adr/0002-*.md`, five fields, status `proposed`, Context citing an existing `QG-n` |
| `adr0001_unchanged` | ADR-0001 is byte-identical |

Rubric: J1 the report describes coupling and interfaces in dataflow terms (connectors, signals,
connections, parameters), not as classes, methods or inheritance in the object-oriented sense;
J2 each candidate in the report names the quality goal it serves; J3 turn 1 ends by asking which
candidate to explore; J4 the final message says the accepted change is recorded as a proposed
ADR that waits for the architect's approval, and that no model was changed yet.

Self-test `EXPECT`:

```python
"S08-noreport": {"report_outside_repo"}, "S08-inrepo": {"report_outside_repo"},
"S08-nogoal": {"goals_cited"}, "S08-inventedgoal": {"goals_cited"},
"S08-t1edit": {"t1_unchanged", "code_unchanged"}, "S08-implemented": {"code_unchanged"},
"S08-accepted": {"adr_proposed"}, "S08-noadr": {"adr_proposed"}, "S08-edited0001": {"adr0001_unchanged"},
```

## Tasks

### Task 1: Modelica fixture, S08 and its checks

**Files:** Create the fixture, `grader/tests/test_grade.py` cases, reference and broken runs; modify `grader/grade.py`, `grader/selftest.py`, `TASKS.md`, `RUBRIC.md`.

**Interfaces:**
- Consumes: multi-turn runs and `workspace-t1` (ticket 04); `grade._files`, `adr`, `five_fields`.
- Produces: `grade.written_file(run_dir, suffix) -> str | None`; `grade.CHECKS["S08"]`.
- [ ] **Step 1:** Write the fixture; run `omc tests/check.mos` in it. Expected: `checkModel` reports the model check completed successfully, with no errors.
- [ ] **Step 2:** Write `test_written_file_returns_last_write` and `test_written_file_none_without_write` (a transcript.md with two `### tool_use Write` blocks), the self-test entries, reference and broken runs. Run them. Expected: failures.
- [ ] **Step 3:** Implement `written_file` and `s08`. Expected: unit tests `OK`, `SELF-TEST PASSED`.
- [ ] **Step 4: Commit** `feat(evals): add Modelica fixture and architecture-scan scenario S08`.

### Task 2: RED on the baseline arm

- [ ] **Step 1:** Run S08 on `--arm baseline --ref main` (k 1–2; `main` has `improve-codebase-architecture`, so both arms start with the slash command), judge, summarise.
- [ ] **Step 2:** Write `campaigns/06-paradigm-neutral.md`: failures per run, wording verbatim, skills loaded, rules that held.
- [ ] **Step 3: Gate.** Expected: at least one run fails `goals_cited`, `code_unchanged` or `adr_proposed`, or J1. Rules no run fails get no GREEN credit; say so.
- [ ] **Step 4: Commit** `test(evals): record architecture scan on main skills (RED)`.

### Task 3: codebase-design vocabulary and references

**Files:** Modify `skills/codebase-design/SKILL.md`; create its three references.

- "Paradigms" section, one table: term | object-oriented | imperative | dataflow (Modelica, Simulink). Rows: module (class or package / function or file / block, model or subsystem), interface (public methods and types / function signature and globals it reads / ports, connectors and their units), seam (an injected dependency / a function pointer or link-time choice / a replaceable block behind a fixed port contract), adapter, coupling source (calls and inheritance / calls and shared globals / connections, shared parameters, global `inner`/`outer` or Goto/From). One paragraph: in dataflow, the signals are the interface; a block that reads another block's parameters bypasses its interface.
- The existing TypeScript testability examples are marked "(OO/imperative)" with one dataflow line each ("pass the parameter in through a port or modifier, not a global").
- "Going deeper" gains: principles, patterns, anti-patterns (the new references), and "Code smells: `code-review` › references/standards-and-smells.md".
- References adapt the seminar summary sections 4, 7, 8.1, 8.2: one table each, ≤ 40 lines, links to the sources the summary cites. Patterns: OO-only GoF patterns marked "(OO)", with a dataflow counterpart where one exists (Strategy → replaceable block with the same ports; Facade → a subsystem with a small port set; Adapter → a converter block between two connector types; Template Method → a fixed init/step/terminate schedule).
- [ ] **Step 1:** Write; validator → `OK`. **Commit** `feat(codebase-design): map the vocabulary to dataflow code and add principle, pattern and anti-pattern references`.

### Task 4: improve-codebase-architecture (GREEN)

**Files:** Modify `skills/improve-codebase-architecture/SKILL.md`, `HTML-REPORT.md`.

- Context line: ADRs in the project's ADR directory (`domain-modeling`); when `docs/architecture/arc42.md` exists, read its quality goals and the "Record architecture decisions" ADR before exploring.
- Card field **Quality goal**: the `QG-n` the candidate serves (from arc42), with one line how. In a set-up project a candidate that serves no goal is left out of the report. Without arc42, the field is omitted (D15).
- Step 3: when the architect accepts a candidate in a set-up project, the change is a decision: draft a `proposed` ADR through `domain-modeling` (Context citing the goal), report it, and change no code until it is accepted. The rejected-candidate ADR offer points to `domain-modeling`'s rule instead of restating it.
- `HTML-REPORT.md`: the card template gains the Quality goal field.
- [ ] **Step 1:** Edit; validator → `OK`. **Commit** `feat(improve-codebase-architecture): tie candidates to quality goals and route accepted changes through a proposed ADR`.
- [ ] **Step 2:** Run S08 on the branch (k 1–2), judge, summarise. No other scenario loads these two skills; check the branch S01–S07 transcripts for `codebase-design` or `improve-codebase-architecture` loads, and re-run any that did.
- [ ] **Step 3: Gate.** Expected: every branch S08 run passes every check and criterion. Otherwise Task 5.
- [ ] **Step 4:** Append GREEN to the campaign. **Commit** `test(evals): record architecture scan on branch skills (GREEN)`.

### Task 5: Close loopholes (only if Task 4's gate failed)

One round, as before; a failure that remains is reported as an open loophole.

### Task 6: README results

- [ ] Add the S08 row; README skill entries for `codebase-design` and `improve-codebase-architecture` if their one-liners changed; verify unit tests, self-test, validator. **Commit** `docs(evals): record architecture scan results`.

## Self-review

- Ticket checklist: paradigm mapping with signals as interfaces (T3), reference tables with "(OO)" marks (T3), Modelica fixture that compiles (T1 Step 1), scenario using dataflow terms and citing goals (S08, J1, `goals_cited`), RED/GREEN (T2, T4), validator (T6).
- Spec stories: 14 (J1), 31–32 (`goals_cited`, J2), 44 (OO marks on patterns here; smells in ticket 10), 45 (T3), 46 (`adr_proposed`, `code_unchanged`, J4).
- Review Focus pins: 1 → J1; 2 → `goals_cited` (existing IDs); 3 → `code_unchanged`; 4 → `adr_proposed`; 5 → `report_outside_repo`.
- Type consistency: `written_file` in Interfaces and Step 2/3.

## Execution handoff

Recommended: inline, as tickets 02–05. Live cost: S08 4 two-turn runs with judges ≈ $1.5.
