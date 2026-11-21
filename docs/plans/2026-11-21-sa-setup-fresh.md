# setup-architecture (fresh project) Implementation Plan

**Goal:** The architect runs `setup-architecture` on an empty project with their requirements.
In the first turn the agent writes only the arc42 skeleton and proposes triage, ranking,
quality goals with scenarios, gap questions and the "made centrally" list. After the architect
confirms, it writes the R-list, the confirmed goals and scenarios, and ADR-0001 "Record
architecture decisions" as `proposed`. RED on `main` first, then GREEN on the branch.

**Architecture:** One new user-invoked skill, `setup-architecture`, with two references: an
arc42 skeleton in our own words and a "made centrally" ADR template with the default list. It
detects the situation (fresh, documented, undocumented); only fresh is handled in this ticket.
It reuses `add-requirements` step 1 for triage and `quality-requirements` for Rank, Derive
goals and Gap question. The suite gains **multi-turn scenarios**: further architect replies are
sent with `claude -p --resume <session>`, the workspace is snapshotted after each turn but the
last, and the grader checks each snapshot.

**Tech Stack:** Markdown skills; Python 3.13 standard library for the suite; `claude` CLI.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (stories 1–10, 15, 47;
Implementation Decisions › New skills); design D1, D3, D4, D5, D10; ticket
`.scratch/software-architecture-skill-set/issues/04-setup-fresh.md`.

## Global Constraints

- `setup-architecture` is user-invoked (`metadata: opencode/autoinvoke: false`); the scenario calls it with `Invoke: setup-architecture`.
- Turn 1 writes only `docs/architecture/arc42.md` with all 12 section headings (`## 1. …` to `## 12. …`) and the section 9 link to `docs/adr/`. R-list rows, QG/QS rows, issues and ADRs are written only after the architect confirms (user, 2026-11-21).
- The arc42 skeleton is in our own words and links arc42.org and docs.arc42.org; no arc42 template text is copied (licence).
- Section 12 links an existing `GLOSSARY.md`; a fresh project has none, so it says the glossary is created with the first term (`domain-modeling`).
- The "made centrally" ADR is titled "Record architecture decisions", takes ADR-0001 in a fresh project, is `proposed`, and its Context cites the confirmed R- and QG-IDs. It is found by title, never by number.
- Requirements and goals follow `quality-requirements` (R-list format, Rank, Derive goals, Gap question; top 3–5 goals; no measure → open question); triage follows `add-requirements` step 1. Link to them, do not restate them.
- Skill text works without any AGENTS.md pointer (user, 2026-11-21).
- Scenario runs: `claude-haiku-5-5`, `--effort medium`, 2 runs per scenario and arm; judge `claude-opus-5-5`. Discipline rules need RED on `main` before GREEN.
- `python3 scripts/validate-skills.py` passes; README updated (user-invoked count 12).

## Probe findings (2026-11-21)

- `claude -p "<turn 1>" --output-format stream-json …` then `claude -p "<turn 2>" --resume <session_id> …` with the same isolated flags and cwd continues the session: the init event of turn 2 carries the same `session_id`, and the agent recalled a word from turn 1.

## Review Focus

1. The agent writes R-list rows or goals in turn 1 because the architect "gave" the requirements, and the skeleton looks harmless. `t1_only_skeleton` must fail it.
2. "It must be fast" becomes a goal with an invented measure ("< 100 ms") instead of an open question.
3. A characteristic no requirement supports (Security, Safety) appears as a goal because the gap question was answered with "no".
4. ADR-0001 is marked `accepted` because the architect said "confirmed" in turn 2 (that confirmed the proposals, not the ADR text).
5. A turn-2 run that never resumed the session (new session, no memory of turn 1) still passes because the prompt alone suffices.

## File Structure

- `skills/setup-architecture/SKILL.md` - situation detection, the fresh-project steps, what turn 1 writes, what confirmation writes, report.
- `skills/setup-architecture/references/arc42-skeleton.md` - the 12 headings with one line each in our own words, links to arc42.org and docs.arc42.org, and the section 1/10 tables from `quality-requirements`.
- `skills/setup-architecture/references/made-centrally-adr.md` - Nygard template for "Record architecture decisions" with the default list (D5).
- `evals/software-architecture/grader/run.py` - `Scenario.replies`, multi-turn `run_scenario`, `_claude(..., resume=)`.
- `evals/software-architecture/grader/judge.py` - task text includes the replies.
- `evals/software-architecture/grader/grade.py` - `s06`.
- `evals/software-architecture/fixtures/fresh/README.md` - one paragraph: product idea, nothing built.
- `evals/software-architecture/grader/{reference,broken}/S06*`; `TASKS.md`, `RUBRIC.md`, `README.md`, `.gitignore`, `campaigns/04-setup-fresh.md`.
- `README.md` - skill entry and user-invoked table row.

## Scenario S06 setup-fresh (fixture `fresh`, `Invoke: setup-architecture`)

Turn 1 (` ```text `):

```text
Set up the architecture for birdlog, a command-line tool for logging bird sightings.
My requirements:
1. Birders log a sighting (species, place, time, count) from the command line.
2. No sighting is ever lost, even if the laptop dies mid-write.
3. Runs offline on Linux, macOS and Windows with nothing but Python installed.
4. Sightings export to the eBird CSV format.
5. It must be fast.
6. `birdlog list` shows the latest sighting first.
```

Turn 2 (` ```reply `):

```text
Your triage and your ranking are confirmed as proposed. The quality goals you proposed are
confirmed in your order, except any you could not give a measure: keep those as open
questions. To your "did you leave out" questions: no, nothing is missing. Write everything
down now. I'm offline after this, so finish without asking me again.
```

Checks (`workspace-t1/` is the snapshot after turn 1):

| check | passes when |
|---|---|
| `t1_only_skeleton` | `workspace-t1` holds `docs/architecture/arc42.md` and no other new file; its R-list, QG and QS tables have no rows |
| `headings` | final arc42 has `## 1.` … `## 12.` headings, each once, in order |
| `rlist` | R-list rows `R-1`…`R-n` contiguous, n ≥ 4, status `active`/`deferred`/`rejected`; no row mentions "latest" |
| `goals_measured` | 3–5 QG rows; each `from` names only existing R-IDs; each `scenario` names a QS row whose `measure` contains a digit |
| `adr_0001` | exactly one ADR, `docs/adr/0001-*.md`, title contains "record architecture decisions", five fields, status `proposed`, Context cites an R- or QG-ID from arc42 |
| `section9_links_adr` | section 9's text contains `../adr/` or `docs/adr/` |
| `feature_routed` | a new file under `.scratch/**/issues/` or `docs/` (ADRs excluded) mentions "latest" and an R-ID from the R-list |

Rubric: J1 turn 1 ends with a triage outcome for each of the six, a ranking with a reason each,
and candidate goals each citing R-IDs with a scenario, and asks the architect to confirm;
J2 "It must be fast" is handled as an open question (a measure is asked for, or the goal is
left out as unmeasured), not filed with an invented measure; J3 turn 1 asks at least one
"did you leave out something like X?" question about a characteristic no requirement supports,
and no goal for such a characteristic is filed; J4 the final message says ADR-0001 waits for
the architect's approval.

Self-test `EXPECT`:

```python
"S06-t1rows": {"t1_only_skeleton"}, "S06-t1adr": {"t1_only_skeleton"},
"S06-heading": {"headings"}, "S06-gapid": {"rlist"}, "S06-latestrow": {"rlist", "feature_routed"},
"S06-sixgoals": {"goals_measured"}, "S06-nomeasure": {"goals_measured"},
"S06-accepted": {"adr_0001"}, "S06-noids": {"adr_0001"}, "S06-nolink": {"section9_links_adr"},
"S06-not1": {"t1_only_skeleton"},   # single-turn run: no workspace-t1
```

## Tasks

### Task 1: Multi-turn runs and S06 checks

**Files:** Modify `grader/run.py`, `grader/judge.py`, `grader/grade.py`, `grader/selftest.py`, `grader/tests/test_run.py`, `grader/tests/test_judge.py`, `TASKS.md`, `RUBRIC.md`, `.gitignore`; create `fixtures/fresh/README.md`, reference and broken runs.

**Interfaces:**
- Produces:
  - `Scenario.replies: list[str]` (default `[]`) from ` ```reply ` blocks after the ` ```text ` block; a second ` ```text ` block still raises `ValueError`.
  - `_claude(prompt, cwd, plugin_dir, out_jsonl, resume: str | None = None)` adds `--resume <id>`.
  - `run_scenario`: turn 1 as today; for each reply k ≥ 2, copy the workspace to `run_dir/workspace-t{k-1}` (without `.git`), then resume the turn-1 `session_id` writing `transcript-t{k}.jsonl`. `transcript.md` renders every turn in order (each reply as `### user`). `meta.json` gains `"turns": int`, `"session_ids": list[str]`, and sums `cost_usd`; `isolation_ok` requires every turn's init to pass and every turn's `session_id` to equal turn 1's.
  - `judge.task_text(scenario) -> str`: the prompt, then each reply under a line `--- architect's reply ---`; `build_prompt` uses it for `{{TASK}}`.
  - `grade.CHECKS["S06"]`.
- [ ] **Step 1:** Write the tests: `test_load_scenarios_reads_replies`, `test_load_scenarios_still_rejects_two_text_blocks` (existing), `test_claude_cmd_adds_resume` (factor `claude_cmd(prompt, plugin_dir, resume=None) -> list[str]` out of `_claude`), `test_render_turns_in_order`, `test_session_mismatch_fails_isolation` (factor `turn_errors(inits: list[dict], plugin_dir, user_skills) -> list[str]`), `test_task_text_includes_replies`, and the self-test entries above. Run them. Expected: failures.
- [ ] **Step 2:** Implement the code, the `fresh` fixture, TASKS/RUBRIC entries, `.gitignore` (`runs/*/*/transcript*.jsonl`), the reference run (`workspace-t1` with skeleton only; `workspace` with arc42, `docs/adr/0001-record-architecture-decisions.md`, `.scratch/requirements/issues/01-list-latest-first.md`) and the broken runs.
- [ ] **Step 3:** Run them again. Expected: `OK`, `SELF-TEST PASSED`.
- [ ] **Step 4: Commit** `feat(evals): add multi-turn scenarios and setup scenario S06`.

### Task 2: RED on the baseline arm

- [ ] **Step 1:** Run S06 on `--arm baseline --ref main` (k 1–2; plain prompt, `main` has no `setup-architecture`), judge, summarise. Confirm `meta.json` shows 2 turns and one session id.
- [ ] **Step 2:** Write `campaigns/04-setup-fresh.md`: failed checks and criteria per run, wording verbatim, skills loaded.
- [ ] **Step 3: Gate.** Expected: at least one run fails `t1_only_skeleton`, `goals_measured` or `adr_0001`. If none fails, stop and report which rules get no GREEN credit.
- [ ] **Step 4: Commit** `test(evals): record setup scenario on main skills (RED)`.

### Task 3: setup-architecture (GREEN)

**Files:** Create `skills/setup-architecture/SKILL.md` and its two references; modify `README.md`.

- Frontmatter: `metadata: opencode/autoinvoke: false`; description "Use when the architect sets up architecture documentation for a project: a fresh project, existing documentation, or code without documentation."
- Body:
  - **Situation:** no source files and no architecture docs → fresh; architecture docs (an arc42 file, `docs/architecture/`, an ADR directory) → documented; source without them → undocumented. Documented and undocumented: say which you found and that this version handles fresh projects only (tickets 05, 07 fill these in).
  - **Turn 1 (fresh):** write `docs/architecture/arc42.md` from the skeleton, then propose in one message: triage of each requirement (`add-requirements` step 1, linked), Rank, Derive goals (candidates with scenarios; unmeasured ones as open questions), Gap question, and the draft "made centrally" list for ADR-0001. End with the question. Nothing else is written.
  - **On confirmation:** R-list rows with R-IDs, feature-level issues per `add-requirements` step 3, confirmed QG/QS rows, then ADR-0001 from the template (`proposed`, Context citing R-/QG-IDs) through `domain-modeling`, linked from section 9.
  - **Report:** what was written, open questions (unmeasured goals), and ADR-0001 waiting for approval with what waits for it.
- References: `arc42-skeleton.md` (12 headings, one line each, our words; links; where sections 1, 9, 10, 12 point), `made-centrally-adr.md` (template; default list: storage and data formats, interfaces between building blocks, dependency rules, versioning, crosscutting conventions such as naming, units and error handling, third-party dependencies; "left to building blocks" examples).
- README: entry under Design and planning; user-invoked table row; counts "twelve".
- [ ] **Step 1:** Write the files; validator → `OK`. **Commit** `feat(setup-architecture): add fresh-project setup with arc42 skeleton and ADR-0001 draft`.
- [ ] **Step 2:** Run S06 on the branch (k 1–2), judge, summarise. Re-run S01–S05 on the branch (k 1–2): the skill set they saw gained `quality-requirements`, `add-requirements` and `setup-architecture` (campaign 03 promised this).
- [ ] **Step 3: Gate.** Expected: every branch S06 run passes every check and criterion, and S01–S05 stay at 1.000/1.000. Otherwise Task 4.
- [ ] **Step 4:** Append GREEN to the campaign. **Commit** `test(evals): record setup scenario on branch skills (GREEN)`.

### Task 4: Close loopholes (only if Task 3's gate failed)

One round, as in tickets 02 and 03: quote the failure, add the specific counter (or tighten a
description and micro-test it, 5 reps per variant plus the no-change control), re-run the
failing scenarios, record the result. A failure that remains is reported as an open loophole.

### Task 5: README results

- [ ] Add the S06 row and the multi-turn note (`reply` blocks, `workspace-t<k>`) to the suite README; refresh S01–S05 branch rows; verify self-test, unit tests, validator. **Commit** `docs(evals): record setup scenario results`.

## Self-review

- Ticket checklist: user-invoked skill with skeleton and links (T3), "made centrally" template (T3), scenario on a fresh fixture checking headings, R-IDs, QG/QS with measures, ADR `proposed` (T1 `headings`, `rlist`, `goals_measured`, `adr_0001`), RED/GREEN (T2, T3), validator (T5).
- Spec stories: 1 (`headings`, `section9_links_adr`), 2–3 (`rlist`, `feature_routed`), 4 (J1), 5–6 (`goals_measured`, J1), 7 (J2), 8 (J3), 9 (`goals_measured`), 10 (`adr_0001`), 15 (fresh takes 0001; the next-free-number case is ticket 05), 47 (S01 re-run).
- Review Focus pins: 1 → `t1_only_skeleton`; 2 → J2 and `goals_measured` (digit); 3 → J3; 4 → `adr_0001`; 5 → session-id check in `isolation_ok` (`test_session_mismatch_fails_isolation`).
- Type consistency: `Scenario.replies`, `claude_cmd`, `turn_errors`, `task_text` named the same in Interfaces and Step 1.
- Deferred minors from ticket 03 stay deferred; none is in this ticket's files except `grade.py`, and none blocks S06.

## Execution handoff

Recommended: inline in this session, as tickets 02 and 03. Live cost: S06 4 two-turn runs plus
S01–S05 10 re-runs, with judges ≈ $3.
