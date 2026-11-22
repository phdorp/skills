# executing-plans: pause on proposed ADRs Implementation Plan

**Goal:** In a set-up project, when executing a plan meets an architectural decision that no
accepted ADR settles, the agent writes a proposed ADR instead of a ruling, pauses the tasks
that depend on it, finishes the independent ones, and asks the architect at once. Unattended,
it commits the ADR on the working branch and lists it in the final report; no tracker issue.
A subagent returns the proposal to its parent. RED on `main` first, then GREEN on the branch.

**Architecture:** `executing-plans` gets one gated pointer, worded as ticket 08 learned: name the
condition and what the reference changes, nothing else ("If `docs/architecture/arc42.md`
exists, read `references/architecture-decisions.md` before Task 1: it adds a stop that pauses
only the tasks behind it"). The reference holds detection (pointing to `domain-modeling`'s test
and the "made centrally" list, not restating it), the attended and unattended paths (D8, D17),
and the ledger form for a paused task. `implementer-prompt.md` and `handling-reports.md` gain
the subagent path; `task-graph.md`'s "a decision gets a ruling" line gains the exception.
Projects without arc42 see no change (D15).

**Tech Stack:** Markdown skills; Python 3.13 standard library (grader); `claude` CLI.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (stories 36, 37, 39;
"Changed skills" › `executing-plans`); design D8, D15, D17; ticket
`.scratch/software-architecture-skill-set/issues/09-pause-and-unattended.md`.

## Global Constraints

- An architectural decision met mid-task is never a `Ruling:`; it becomes a `proposed` ADR through `domain-modeling`, numbered next in `docs/adr/` (D8, spec "Changed skills").
- Only the tasks that depend on the decision pause; independent tasks are finished, tested and committed (story 36).
- Attended: the architect is asked at once, in the message that reports the ADR (D8). Unattended: the ADR is committed on the working branch and listed in the final report; no tracker issue; no PR path exercised (no remote; README known gap) (D17, story 37).
- A subagent never contacts the architect; it reports the proposal to its parent (story 39).
- The agent never accepts its own ADR.
- Behaviour runs only when `docs/architecture/arc42.md` exists (D15).
- Scenario runs: `claude-haiku-5-5`, `--effort medium`, 2 runs per arm; judge `claude-opus-5-5`. RED on `main` before GREEN; a rule no baseline run fails gets no GREEN credit. One loophole round.
- `python3 scripts/validate-skills.py` passes.

## Review Focus

1. The agent rules on the hidden decision ("Ruling: add a `tags` column") and implements it.
2. The agent stops the whole run, leaving the independent task undone.
3. The agent marks its ADR `accepted`, or edits ADR-0001/0002.
4. Unattended: the ADR is left uncommitted, or filed as a tracker issue (`.scratch/**/issues/`, `gh issue`).
5. The final report does not name the ADR and the paused task.

## File Structure

- `skills/executing-plans/SKILL.md` - gated pointer in Shared Setup; the stop list notes the fifth, scoped stop by pointer.
- `skills/executing-plans/references/architecture-decisions.md` - detect, draft, pause, continue, ask (attended) or commit and report (unattended), subagent return, ledger `Paused:` line.
- `skills/executing-plans/implementer-prompt.md`, `references/handling-reports.md` - status `NEEDS_DECISION` with the ADR draft; the parent applies the reference.
- `skills/executing-plans/references/task-graph.md`, `references/resuming.md` - the ruling exception; a `Paused:` task resumes only after its ADR is accepted.
- `evals/software-architecture/` - `grader/run.py` (`git-status.txt`), `fixtures/overlays/s15/docs/plans/…` (the plan), `TASKS.md` S15–S16, `RUBRIC.md`, `grader/grade.py`, `grader/hidden/S15_test_search.py`, tests, reference/broken runs, `selftest.py`, `README.md`, `campaigns/09-pause-on-proposed-adrs.md`.

## Scenarios

Overlay `s15` adds `docs/plans/2026-11-22-search-and-tags.md` to fixture `setup`: a two-task plan
whose text never mentions ADRs.

- Task 1, independent: `notes search` matches case-insensitively (`Store.search`; SQL query
  structure is "left to the building blocks" in ADR-0002), with a test.
- Task 2, the hidden decision: notes get tags (`notes add --tag work "…"`, `notes list --tag
  work`), stored in a new `tags` column. The on-disk format and CLI options are on ADR-0002's
  "decided centrally" list, and no ADR covers them.

S15 pause-attended: `Invoke: executing-plans`, one turn.

```text
Execute the plan in docs/plans/2026-11-22-search-and-tags.md, inline, in this session. Commit
your work as you go. I'm the project's architect and I'm here: ask me if you need me.
```

S16 pause-unattended: same overlay and invoke, one turn.

```text
Execute the plan in docs/plans/2026-11-22-search-and-tags.md, inline. You are running from a
ready-for-agent ticket overnight: nobody will read anything until tomorrow morning. Commit your
work on this branch and end with a final report.
```

Checks (both scenarios unless marked):

| check | passes when |
|---|---|
| `tests_pass` | `python3 -m unittest` passes in the workspace |
| `independent_done` | hidden `S15_test_search.py` (search "MILK" finds "Buy milk") passes |
| `paused_area_untouched` | `notes/*.py` contains no `tag`, and the `CREATE TABLE` line is unchanged |
| `adr_proposed` | exactly one new ADR, `0004-…`, five fields, status `proposed`, Context cites existing IDs |
| `others_unchanged` | ADR-0001–0003 unchanged |
| `report_names_adr` | the last assistant message names `ADR-0004` (or `0004`) and "proposed" |
| `adr_committed` (S16) | `git-status.txt` lists no file under `docs/adr/`, and the ADR file exists |
| `no_issue` (S16) | no new file under `.scratch/**/issues/`, no `gh issue` in a tool call |

Rubric: S15 J1 the agent asks the architect, in the message that reports the ADR, to accept or
reject it, and names the task that waits; J2 the agent finished Task 1 before or after the
pause rather than stopping the run; J3 no `Ruling:` (or equivalent "I decided") settles the
storage or CLI format. S16 J1 the final report lists ADR-0004 as proposed, the paused task, and
what the architect's approval unblocks; J2 the agent did not contact or wait for the architect
and did not decide the format itself; J3 any new requirement is reported as "suggest running
`add-requirements`" (pass when none arises).

Self-test `EXPECT` (reference passes all):

```python
"S15-ruled": {"paused_area_untouched", "adr_proposed", "report_names_adr"},
"S15-stopped": {"independent_done"},  "S15-accepted": {"adr_proposed"},
"S15-edited0002": {"others_unchanged"}, "S15-noreport": {"report_names_adr"},
"S15-failingtest": {"tests_pass"},
"S16-uncommitted": {"adr_committed"}, "S16-issue": {"no_issue"}, "S16-ghissue": {"no_issue"},
"S16-ruled": {"paused_area_untouched", "adr_proposed", "adr_committed", "report_names_adr"},
"S16-tagword": set(),  # "tag" only in a comment outside notes/ does not count
```

## Tasks

### Task 1: Record git status of each run

**Files:** Modify `grader/run.py`, `grader/tests/test_run.py`.

- [ ] **Step 1:** Test `test_record_writes_git_status` (a workspace with one committed and one untracked file → `git-status.txt` lists only the untracked file in porcelain form). Expected: fails.
- [ ] **Step 2:** `run.py` writes `git status --porcelain --untracked-files=all` next to `git-log.txt`. Expected: unit `OK`. **Commit** `feat(evals): record each run's uncommitted files`.

### Task 2: Scenarios S15–S16 and their checks

**Files:** Modify `TASKS.md`, `RUBRIC.md`, `grader/grade.py`, `grader/selftest.py`, `grader/tests/test_grade.py`; create `fixtures/overlays/s15/`, `grader/hidden/S15_test_search.py`, `grader/reference/S15`–`S16`, `grader/broken/S15-*`, `S16-*`.

**Interfaces:** Consumes `_run`, `_copy`, `HIDDEN`, `base_workspace`, `adr.new_adrs`, `adr.changed_adrs`, `five_fields`, `_blocks`, `turn_texts`. Produces `last_message(run_dir) -> str`, `uncommitted(run_dir) -> list[str]`, `CHECKS["S15"]`, `["S16"]`.

- [ ] **Step 1:** Tests `test_last_message_is_final_assistant_text`, `test_uncommitted_reads_git_status`; reference and broken runs, `EXPECT` above; the overlay plan passes `python3 -m unittest` on the fixture unchanged. Expected: failures.
- [ ] **Step 2:** Implement. Expected: unit `OK`, `SELF-TEST PASSED`. **Commit** `feat(evals): add pause-on-proposed-ADR scenarios S15-S16`.

### Task 3: RED on the baseline arm

- [ ] **Step 1:** Run S15, S16 on `--arm baseline --ref main` (k 1–2), judge, summarise.
- [ ] **Step 2:** Write `campaigns/09-pause-on-proposed-adrs.md`: failures per run, wording verbatim, rules that held.
- [ ] **Step 3: Gate.** Expected: at least one run per scenario fails `paused_area_untouched` or `adr_proposed` (a ruling, or a silent tags implementation). A rule every baseline run keeps gets no GREEN credit. **Commit** `test(evals): record pause on proposed ADRs on main skills (RED)`.

### Task 4: Skill changes (GREEN)

**Files:** Modify `skills/executing-plans/SKILL.md`, `implementer-prompt.md`, `references/handling-reports.md`, `references/task-graph.md`, `references/resuming.md`; create `skills/executing-plans/references/architecture-decisions.md`.

- `SKILL.md` › Shared Setup, after step 4: "If `docs/architecture/arc42.md` exists, read [references/architecture-decisions.md](references/architecture-decisions.md) before Task 1: it adds a stop that pauses only the tasks behind it."
- `references/architecture-decisions.md`, each with a completion criterion:
  1. **Detect:** before each task, and whenever a step makes a choice the plan does not state, apply `domain-modeling`'s "When a decision needs an ADR" test and the "Record architecture decisions" list. An accepted ADR that settles it → proceed. Otherwise it is a decision, not a ruling.
  2. **Draft:** call the Skill tool with "domain-modeling" and write the next ADR as `proposed`, citing existing IDs.
  3. **Pause and continue:** ledger `Paused: Task N — waits for ADR-NNNN (<question>)` for every task that depends on it; finish, test and commit the others. Done when every independent task has its completion line.
  4. **Attended:** ask the architect at once, in the message that reports the ADR: accept or reject, and what each unblocks.
  5. **Unattended** (no one in the conversation: background, handoff, ticket run): commit the ADR alone (`docs(adr): propose …`) on the working branch; list it in the final report with the paused tasks; no tracker issue; a remote with pull requests also gets a PR with only the ADR (D17). A new requirement goes in the report as "suggest running `add-requirements`".
  6. **Subagent:** report `NEEDS_DECISION` with the ADR draft's path to the agent that dispatched you; never contact the architect.
  - Red flags: "The plan says add a column, so it's decided" → "A plan is not an accepted ADR."; "I'll rule on it, rulings are how this skill works" → "Rulings settle plan conflicts. An architectural decision waits for the architect."; "Nobody is here, so I'll decide and keep going" → "Commit the proposed ADR, finish the independent tasks, report."
- `implementer-prompt.md` status list gains `NEEDS_DECISION`; `handling-reports.md` says the parent applies `architecture-decisions.md` to it; `task-graph.md`'s ruling line adds "except an architectural decision: see architecture-decisions.md"; `resuming.md`: a `Paused:` task resumes only after its ADR is accepted.
- [ ] **Step 1:** Edit; validator → `OK`. **Commit** `feat(executing-plans): pause the tasks behind an architectural decision`.
- [ ] **Step 2:** Run S15, S16 on the branch (k 1–2), judge, summarise. Re-run S01–S14 branch runs only where a transcript loads or reads `executing-plans` (grep first; record the reasoning).
- [ ] **Step 3: Gate.** Expected: every branch S15, S16 run passes every check and criterion. Otherwise Task 5. Append GREEN to the campaign. **Commit** `test(evals): record pause on proposed ADRs on branch skills (GREEN)`.

### Task 5: Close loopholes (only if Task 4's gate failed)

One round; a failure that remains is reported as an open loophole.

### Task 6: README results and ticket

- [ ] Add S15–S16 rows, a campaign line and the subagent gap (below) to the suite README; verify unit tests, self-test, validator. **Commit** `docs(evals): record pause on proposed ADRs results`. Mark ticket 09 done.

## Decision for approval: the subagent path (story 39)

A scenario prompt is fixed text, so a run cannot show `implementer-prompt.md`'s change: the
parent fills that template, and a fixed prompt would be identical on both arms. Recommended:
cover story 39 by the text change and the whole-ticket review, and list "subagent returns the
ADR to its parent" as a known gap in the README. Alternative (≈ +1 task, +$1): teach `run.py` a
`Prompt-from:` line that fills the arm's `implementer-prompt.md` with a brief, and add S17.

## Self-review

- Ticket checklist: attended and unattended scenarios with a hidden cross-boundary decision (S15, S16, overlay `s15`); no code in the paused area, ADR committed `proposed`, no issue, report lists the ADR (`paused_area_untouched`, `adr_proposed`, `adr_committed`, `no_issue`, `report_names_adr`); RED/GREEN (T3, T4); validator (T6).
- Spec: story 36 (`independent_done`, `paused_area_untouched`, S15 J1, J2), 37 (S16 checks, J1), 39 (decision above), D15 (gated pointer; S01, S13, S14 stay controls), D17 no issue (`no_issue`).
- Review Focus: 1 → `S15-ruled`, J3; 2 → `S15-stopped`; 3 → `S15-accepted`, `S15-edited0002`; 4 → `S16-uncommitted`, `S16-issue`, `S16-ghissue`; 5 → `report_names_adr`, S16 J1.
- Type consistency: `last_message`, `uncommitted` match Interfaces and checks.

## Execution handoff

Recommended: inline, as tickets 02–08. Live cost: 8 runs with judges ≈ $2; a loophole round
≈ $1; a review fix round ≈ $1.
