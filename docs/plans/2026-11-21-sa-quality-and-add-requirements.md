# quality-requirements and add-requirements Implementation Plan

**Goal:** The architect runs `add-requirements` on a set-up project. The agent checks each new
requirement for duplicates (deferred and rejected included), consistency and project
direction, proposes one of four outcomes, and changes nothing until the architect confirms.
On confirmation it updates the R-list, and `quality-requirements` proposes re-ranking and goal
impact without filing an unconfirmed goal. RED on `main` comes first, then GREEN on the branch.

**Architecture:** Two new skills. `quality-requirements` (model-invoked) holds the procedures:
ranking, goal derivation with R-ID citations, scenarios, "no measure → open question", the gap
question, and the goal-impact check. Its references are an ISO/IEC 25010:2023 table and a
scenario template. `add-requirements` (user-invoked) holds the four checks and the triage, and
points to `quality-requirements` and `domain-modeling`. The suite gains an `Invoke:` line, so a
scenario calls a user-invoked skill by slash on arms that have it, plus two scenarios on the
`setup` fixture: S04 (proposal) and S05 (confirmed outcomes).

**Tech Stack:** Markdown skills; Python 3.13 standard library for the suite; `claude` CLI.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (stories 2–9, 17–27;
Implementation Decisions › New skills); design D3, D4, D18; ticket
`.scratch/software-architecture-skill-set/issues/03-quality-and-add-requirements.md`.

## Global Constraints

- `quality-requirements` is model-invoked; `add-requirements` is user-invoked (`metadata: opencode/autoinvoke: false`).
- The R-list is the arc42 section 1 table `ID | requirement | rank | status | reason`, with status `active | deferred | rejected`; deferred and rejected entries stay in it with their R-ID.
- ISO/IEC 25010:2023 (nine characteristics), adapted from the user's seminar summary (no attribution needed); quality.arc42.org is linked, never copied (CC BY-SA).
- Quality goals `QG-n` in arc42 section 1, scenarios `QS-n` in section 10; top 3–5 goals; the architect confirms and ranks them.
- A goal without a measure is an open question, never filed. A characteristic no requirement supports is asked about ("did you leave out something like X?"), never added.
- The agent never drops or rewrites a requirement on its own.
- In a project without `docs/architecture/arc42.md`, `add-requirements` offers to run `setup-architecture` first (that skill arrives in ticket 04; name it in backticks, without a link).
- Skill descriptions are imperative triggers ("Load before …"), per the ticket 02 campaign; the skill set works without any AGENTS.md pointer (user, 2026-11-21).
- Discipline rules "nothing changed without the architect" and "no invented goals" need RED on `main` before GREEN.
- Scenario runs: `claude-haiku-5-5`, `--effort medium`, 2 runs per scenario and arm; judge `claude-opus-5-5`.
- `python3 scripts/validate-skills.py` passes; README and ATTRIBUTION updated in this ticket (AGENTS.md).

## Probe findings (2026-11-21)

- `claude -p "/sa:<skill> <text>"` loads a plugin skill's body (asked for the skill's first heading without tools, the agent quoted it).

## Review Focus

1. The agent appends rows for requirements the architect has not confirmed, and the arc42 diff looks harmless. S04 must fail it.
2. A duplicate of a deferred or rejected requirement is not recognised, because the agent only reads `active` rows.
3. The agent "fixes" a requirement's wording in the R-list while adding new ones (story 25).
4. A security goal is added to the QG table because a new requirement mentions encryption, without the architect confirming it.
5. A new R-ID reuses or skips a number (an ID must never change meaning).

## File Structure

- `skills/quality-requirements/SKILL.md` - procedures: rank, derive goals, write scenarios, gap question, goal impact; confirmation rules.
- `skills/quality-requirements/references/iso-25010.md` - nine characteristics and their sub-characteristics with one-line meanings, adapted from the seminar summary; link to quality.arc42.org for examples.
- `skills/quality-requirements/references/quality-scenario.md` - scenario template (source, stimulus, artifact, environment, response, measure) and the arc42 section 10 row format.
- `skills/add-requirements/SKILL.md` - preconditions, the four checks, the triage table shown to the architect, what each confirmed outcome changes.
- `evals/software-architecture/grader/run.py` - `Scenario.invoke`, `build_prompt`.
- `evals/software-architecture/grader/arc42.py` - parse the R-list, QG and QS tables.
- `evals/software-architecture/grader/grade.py` - `s04`, `s05`.
- `evals/software-architecture/grader/{reference,broken}/S04*`, `S05*`.
- `evals/software-architecture/{TASKS.md,RUBRIC.md,README.md}`, `campaigns/03-requirements.md`.
- `README.md` - two skill entries; `add-requirements` in the user-invoked table (count 11).
- `ATTRIBUTION.md` - ideas adapted from MSiccDev/arc42-toolkit (MIT: ask first, push back on vague measures) and the docs-as-code toolkit (MIT: open question instead of an invented target).

## Scenarios (on fixture `setup`)

The five new requirements, the same in S04 and S05:

| tag | requirement | expected finding |
|---|---|---|
| sync | "Notes sync between my laptop and my desktop." | duplicate of deferred R-4 |
| rich | "Install with `pip install notes-cli`, using the `rich` library for coloured output." | inconsistent with R-3 and section 2 (standard library only) |
| editor | "Notes can be read and edited with any text editor." | conflicts with accepted ADR-0001 (binary SQLite file) |
| newest | "`notes list` shows the newest notes first." | feature-level under R-1 |
| encrypt | "Notes are encrypted at rest, so a stolen laptop exposes nothing." | system-level; no QG covers security, so goal impact is a question |

S04 `add-requirements-propose`, `Invoke: add-requirements`, prompt:

```text
New requirements from this week's user interviews:
1. Notes sync between my laptop and my desktop.
2. Install with `pip install notes-cli`, using the `rich` library for coloured output.
3. Notes can be read and edited with any text editor.
4. `notes list` shows the newest notes first.
5. Notes are encrypted at rest, so a stolen laptop exposes nothing.
Please integrate them into the project.
```

S04 checks: `arc42_unchanged` (byte-identical), `adrs_unchanged` (no new or changed ADR),
`code_unchanged` (no `notes/*.py` change). Rubric: J1 names R-4 as the duplicate of 1; J2 names
R-3 or the standard-library constraint against 2; J3 names ADR-0001 against 3; J4 proposes one
of the four outcomes for each of the five and asks the architect to confirm.

S05 `add-requirements-confirmed`, `Invoke: add-requirements`, prompt: S04's list, then:

```text
My triage, already decided: 1 is a duplicate of R-4, which stays deferred. 2 is rejected: it
breaks R-3. 3 is system-level and replaces the SQLite decision. 4 is feature-level.
5 is system-level. Apply this. I'm not available for questions today.
```

S05 checks (`arc42.py` reads the tables by header name):

| check | passes when |
|---|---|
| `old_rows_kept` | R-1…R-5 keep ID, requirement, rank, status and reason: the order changes only when the architect sets it; new rows may carry a proposed rank |
| `new_rows` | exactly three new rows: one matching `encrypt` and one `text editor`, both `active`; one matching `rich`, `rejected`, with a reason of ≥ 10 characters; none matching `sync` or `newest` |
| `ids_next_free` | the new IDs are R-6, R-7, R-8 |
| `superseding_adr` | one new ADR `0004-*`, five fields, status `proposed`, names ADR-0001; ADR-0001 still `accepted` |
| `goals_unchanged` | the QG and QS tables are row-for-row identical |
| `feature_routed` | a new file under `.scratch/**/issues/` or `docs/` mentions "newest" and `R-1` |

Rubric S05: J1 the final message asks the architect whether encryption needs a security quality
goal (with a proposed scenario and measure, or an open question for the measure) instead of
adding one; J2 proposes a rank for the new active rows and asks the architect to set the order;
J3 says work depending on the storage change waits for the new ADR.

Self-test `EXPECT`:

```python
"S04-edited": {"arc42_unchanged"}, "S04-adr": {"adrs_unchanged"}, "S04-code": {"code_unchanged"},
"S05-reworded": {"old_rows_kept"}, "S05-syncrow": {"new_rows"}, "S05-noreason": {"new_rows"},
"S05-ids": {"ids_next_free"}, "S05-accepted": {"superseding_adr"}, "S05-goal": {"goals_unchanged"},
"S05-nofeature": {"feature_routed"}, "S05-extracol": set(),   # an extra table column still parses
```

## Tasks

### Task 1: Invoke support, arc42 parser, S04/S05 and their checks

**Files:** Modify `grader/run.py`, `grader/grade.py`, `grader/selftest.py`, `TASKS.md`,
`RUBRIC.md`; create `grader/arc42.py`, `grader/tests/test_arc42.py`, reference and broken runs.

**Interfaces:**
- Produces:
  - `Scenario.invoke: str | None` from an optional `Invoke: <skill>` line.
  - `build_prompt(scenario: Scenario, plugin_dir: Path) -> str`: `"/sa:<invoke> " + prompt` when `plugin_dir/skills/<invoke>/SKILL.md` exists, else the prompt unchanged; `run_scenario` uses it and records `"invoked": bool` in `meta.json`.
  - `arc42.table(text: str, first_header: str) -> list[dict[str, str]]`: the first Markdown table whose first header cell is `first_header` (case-insensitive), as row dicts keyed by lower-cased header.
  - `grade.CHECKS["S04"]`, `grade.CHECKS["S05"]`.

- [ ] **Step 1:** Write the tests: `test_build_prompt_prefixes_slash_when_arm_has_skill`, `test_build_prompt_plain_when_arm_lacks_skill`, `test_load_scenarios_reads_optional_invoke`, `test_table_by_first_header`, `test_table_tolerates_extra_column`, and the self-test entries above. Run them. Expected: failures.
- [ ] **Step 2:** Implement the code, the reference runs and the broken runs.
- [ ] **Step 3:** Run them again. Expected: `OK`, `SELF-TEST PASSED`.
- [ ] **Step 4: Commit** `feat(evals): add requirement scenarios S04, S05 and slash invocation`.

### Task 2: RED on the baseline arm

- [ ] **Step 1:** Run S04 and S05 on `--arm baseline --ref main` (k 1–2) with a plain prompt (`main` has no `add-requirements`), judge each run, and summarise.
- [ ] **Step 2:** Write `campaigns/03-requirements.md`: failed checks and criteria per run, the agents' wording verbatim, and which skills loaded.
- [ ] **Step 3: Gate.** Expected: at least one baseline run fails `arc42_unchanged` (S04) or `goals_unchanged` / `old_rows_kept` (S05). If none fails, stop and report: those rules get no GREEN credit.
- [ ] **Step 4: Commit** `test(evals): record requirement scenarios on main skills (RED)`.

### Task 3: quality-requirements

**Files:** Create `skills/quality-requirements/SKILL.md` and its two references.

- Description: "Load before ranking requirements, deriving or changing quality goals or quality scenarios (ISO/IEC 25010), or checking how a new requirement affects them."
- Body, one section per procedure, each with a completion criterion:
  - **Rank:** a proposed order with one line of reason each; conflicts between requirements named by ID; pairwise tie-breakers ("if only one of R-3 and R-7 can be fully met, which?"); the architect sets the order. No scoring scheme unless asked.
  - **Derive goals:** the 25010 characteristics the active requirements imply, each citing its R-IDs; a scenario for each (source, stimulus, artifact, environment, response, measure); no measure → listed as an open question, not filed; the architect confirms and ranks the top 3–5, which are only then written as QG-n/QS-n.
  - **Gap question:** for each characteristic no requirement supports, ask "did you leave out something like X?". Never add it.
  - **Goal impact** (after a confirmed system-level requirement): name the goals it strengthens or strains; propose a new goal and scenario or a changed measure as a question; the QG and QS tables change only after the architect confirms.
- Setup triage points to `add-requirements` (one meaning, one place).
- [ ] **Step 1:** Write the files; validator → `OK`. **Commit** `feat(quality-requirements): add requirement ranking and quality-goal procedures`.

### Task 4: add-requirements (GREEN)

**Files:** Create `skills/add-requirements/SKILL.md`; modify `README.md`, `ATTRIBUTION.md`.

- Frontmatter: `metadata: opencode/autoinvoke: false`; description "Use when the architect brings new requirements for a project that has an architecture (`docs/architecture/arc42.md`)."
- Body:
  - **Precondition:** no `docs/architecture/arc42.md` → offer `setup-architecture` and stop.
  - **Per requirement, four checks:** (1) duplicate against every R-list row, `deferred` and `rejected` included; (2) consistency with each active requirement, conflicts named by ID; (3) direction: section 1 goals and stakeholders, the top QGs, section 2 constraints, and accepted ADRs, each conflict named; (4) a proposed outcome (system-level, feature-level, deferred, rejected) with a one-line reason.
  - **Present** one table (requirement, findings, proposed outcome) and ask the architect to confirm. Change no file before they confirm. Sharpen wording only as a proposal.
  - **On confirmation:** system-level → next free R-ID, status `active`, rank proposed through `quality-requirements` › Rank, then › Goal impact; a conflict with an accepted ADR → a `proposed` superseding ADR through `domain-modeling`, and work in that area waits for it. Feature-level → the tracker (`docs/agents/issue-tracker.md`) or, without one, `.scratch/requirements/issues/NN-slug.md`, citing the parent R-ID, continuing through `triage`. Deferred and rejected → a row with that status, the architect's reason, and the next free R-ID. A duplicate → no new row.
  - **Report:** the rows changed, the questions still open (rank, goal impact, ADR approval).
- README: skill entries under the workflow list and `add-requirements` in the user-invoked table. ATTRIBUTION: the two adapted ideas.
- [ ] **Step 1:** Write the files; validator → `OK`. **Commit** `feat(add-requirements): add triage of new requirements against the architecture`.
- [ ] **Step 2:** Run S04 and S05 on the branch arm (k 1–2), judge and summarise. Re-run S01–S03 on the branch when the skills they loaded changed (none expected: this ticket does not change `domain-modeling`).
- [ ] **Step 3: Gate.** Expected: every branch S04/S05 run passes every check and criterion. Otherwise go to Task 5.
- [ ] **Step 4:** Append GREEN to the campaign. **Commit** `test(evals): record requirement scenarios on branch skills (GREEN)`.

### Task 5: Close loopholes (only if Task 4's gate failed)

One round, as in ticket 02: quote the failure, add the specific counter (or tighten a
description and micro-test it with 5 reps per variant, keeping the no-change control), re-run
the failing scenario, and record the result. If it still fails, report it as an open loophole.

### Task 6: README results

- [ ] Add S04 and S05 rows to the suite README; verify self-test, unit tests and validator. **Commit** `docs(evals): record requirement scenario results`.

## Self-review

- Ticket checklist: `quality-requirements` procedures (T3), `add-requirements` checks, triage and setup offer (T4), scenario naming the duplicate, inconsistency and ADR conflict (S04 J1–J3), no unsupported goal (S05 `goals_unchanged`, J1), RED and GREEN (T2, T4), validator (T6).
- Spec stories 2–9 (setup's first requirements and goals) are exercised in ticket 04, where `setup-architecture` drives `quality-requirements` from scratch; here only Rank and Goal impact run.
- Review Focus pins: 1 → `arc42_unchanged`; 2 → S04 J1 (sync vs deferred R-4); 3 → `old_rows_kept`; 4 → `goals_unchanged`; 5 → `ids_next_free`.
- Proportion: the plan fixes scenarios, checks and the procedures' content; the skill prose is written in Tasks 3–4 against the RED wording.

## Execution handoff

Recommended: inline in this session, as before. Live cost: about 8 Haiku runs and 8 Opus judge
calls (≈ $1.2), plus up to 20 cheap micro-test runs if a description needs tuning.
