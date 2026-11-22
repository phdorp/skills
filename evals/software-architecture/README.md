# Software architecture scenario suite

Measures whether the software-architecture skill set (spec:
`docs/specs/2026-11-21-software-architecture-skill-set-spec.md`) changes what an agent does,
against the skills at `main`. Re-run it when the model or the skills change.

## Contents

- `TASKS.md`: scenarios (S01…), each a prompt given verbatim to a fresh agent on a copy of one
  fixture. An `Invoke: <skill>` line prefixes the prompt with `/sa:<skill>` on arms that have
  that user-invoked skill; `meta.json` records `invoked`. A `Prompt-from: <path>` line makes the
  prompt the arm's own copy of that dispatch template (its `prompt: |` text), filled from the
  ` ```text ` block's `key: value` lines, so each arm gets its own template; `meta.json` records
  `prompt_from`. Each ` ```reply ` block after the
  prompt is a scripted architect reply, sent with `claude -p --resume` in the same session;
  the workspace before reply k is saved as `workspace-t<k-1>/`, and a run whose turns do not
  share one session fails isolation.
- `RUBRIC.md`: judged criteria per scenario.
- `fixtures/<name>/`: small projects the scenarios start from.
- `grader/run.py`: runs one scenario on one arm and saves the run; `probe` proves isolation.
- `grader/grade.py`: deterministic checks per scenario; `summarize.py` grades every run, merges
  the judge's verdicts and writes `results/<arm>.json`; `selftest.py` checks the grader against
  `reference/` (every check passes) and `broken/` variants (each fails exactly its checks).
- `grader/judge.py`: scores one run against `RUBRIC.md` and checks every quote.
- `runs/<arm>/<scenario>-r<k>/`: `workspace/` (files the agent left, without `.git`),
  `git-log.txt`, `transcript.md`, `meta.json`, `judge.json`. The raw `transcript.jsonl` is not
  committed.
- `results/`: summaries of the runs below.

## Arms, models, isolation

- Arms: `baseline` runs the skills at `main`; `branch` runs the skills at the branch under test.
  Each arm's skills come from `git archive <ref>` into a directory named `sa`, loaded with
  `--plugin-dir`, so they appear as `sa:<skill>` on both arms. Never the working tree.
- Scenario runs: Claude Haiku 5.5 (`claude-haiku-5-5`) at `--effort medium`, `claude -p` with
  `--setting-sources project` (keeps `~/.claude/skills` out), in a fresh temp workspace outside
  this repository (keeps its `AGENTS.md` out), with a clean environment.
- Judge: Claude Opus 5.5 (`claude-opus-5-5`), no tools, everything in the prompt.
- The stream-json `init` event lists the plugins and skills a run saw. `run.py` checks it; a run
  that saw a foreign plugin, a user skill or any MCP server is saved with `isolation_ok: false`
  and left out of the scores. Runs set `ENABLE_CLAUDEAI_MCP_SERVERS=false` and
  `--strict-mcp-config`, because the account's claude.ai connectors otherwise load into
  scenario runs (they reached 20 of 26 runs before 2026-11-21's fix).
- 2 runs per scenario and arm.

## Run it

Needs the `claude` CLI (2.1.326 tested), git and python3 (standard library only).

```sh
cd evals/software-architecture/grader
python3 -I -m unittest discover -s tests       # unit tests of runner and judge
python3 -I selftest.py                         # grader self-test
python3 -I run.py probe --ref main             # isolation proof, per arm ref
python3 -I run.py run S01 --arm baseline --ref main -k 1
python3 -I run.py run S01 --arm branch --ref <branch> -k 1
python3 -I judge.py ../runs/baseline/S01-r1    # writes judge.json
python3 -I summarize.py ../runs                # writes ../results/<arm>.json, prints the table
```

`run.py` refuses to overwrite an existing run directory.

## Review rule

The judge must quote the run for every verdict; `judge.py` checks each quote occurs in the named
file and sets `needs_review` when one does not, or when a criterion has no verdict.
`summarize.py` lists runs that need review: those flagged by the judge, and those where grader
and judge disagree (every check passed but a criterion failed, or the reverse). The user
reviews every listed run, plus a sample of the rest.

## Results

Haiku 5.5 medium runs, Opus 5.5 judge, 2 runs per scenario and arm. `baseline` ran the skills
at `main`; `branch` ran the skills at the commit named in each run's `meta.json`. A branch run
is replaced when the skills it ran change; git history keeps the old runs. Campaign records
with the agents' wording: [campaigns/](campaigns/).

| scenario | baseline grader | baseline judge | branch grader | branch judge | branch runs that loaded the target skill |
|---|---:|---:|---:|---:|---|
| S01 no-setup | 1.000 | 1.000 | 1.000 | 1.000 | - (none expected) |
| S02 record-decision | 0.928 | 1.000 | 1.000 | 1.000 | 2 of 2 |
| S03 lifecycle | 0.400 | 0.250 | 1.000 | 1.000 | 2 of 2 |
| S04 add-requirements-propose | 0.500 | 0.750 | 1.000 | 1.000 | 2 of 2 (slash) |
| S05 add-requirements-confirmed | 0.375 | 0.000 | 1.000 | 1.000 | 2 of 2 (slash) |
| S06 setup-fresh (two turns) | 0.000 | 0.250 | 1.000 | 0.875 | 2 of 2 (slash) |
| S07 setup-documented (two turns) | 0.071 | 0.000 | 1.000 | 1.000 | 2 of 2 (slash) |
| S08 architecture-scan-dataflow (two turns) | 0.500 | 0.375 | 0.916 | 0.875 | 2 of 2 (slash) |
| S09 recovery-python (three turns) | 0.000 | 0.000 | 0.928 | 1.000 | 2 of 2 (slash) |
| S10 recovery-dataflow (three turns) | 0.000 | 0.000 | 1.000 | 0.875 | 2 of 2 (slash) |
| S11 dialogue-setup (two turns) | 0.500 | 0.250 | 1.000 | 0.750 | 2 of 2 (slash) |
| S12 spec-setup | 0.500 | 0.500 | 1.000 | 1.000 | 2 of 2 (slash) |
| S13 spec-plain (control) | 1.000 | 1.000 | 1.000 | 0.500 | 2 of 2 (slash) |
| S14 dialogue-plain (control) | 1.000 | 1.000 | 1.000 | 1.000 | 2 of 2 (slash) |
| S15 pause-attended | 0.584 | 0.500 | 1.000 | 1.000 | 2 of 2 (slash) |
| S16 pause-unattended | 0.625 | 0.667 | 1.000 | 1.000 | 2 of 2 (slash) |
| S17 pause-subagent | 0.375 | 0.000 | 0.938 | 1.000 | - (dispatch template) |
| S18 pause-on-existing | 0.916 | 0.750 | 1.000 | 1.000 | 2 of 2 (slash) |

Cost so far: about $2.10–2.50 per arm (runs ≈ $0.20–0.25, judge ≈ $1.90–2.20). A turn takes 20–60 s.

- S01: no run loaded a skill on either arm. It shows an ordinary change stays ordinary, not
  that the skills stay quiet once loaded.
- S02, S03 (ticket 02, [campaign](campaigns/02-adr-rules.md)): on `main`, agents marked the
  replaced ADR superseded early and cited requirements that did not exist; accepting their own
  ADRs was seen only in runs the claude.ai connector reached (clean re-run: campaign addendum). Every
  branch run that loaded `domain-modeling` followed every rule; the branch S02 run that did not
  load it accepted its own ADR again. The skill loaded unreliably for "record the decision as
  an ADR" until its description became an imperative trigger ("Load before creating or editing
  any ADR …"): 2 of 5 loads before, 5 of 5 after, in a micro-test recorded in the campaign.
- S04, S05 (ticket 03, [campaign](campaigns/03-requirements.md)): on `main`, agents built a
  requirement before the architect confirmed the triage, rewrote deferred R-4, and accepted
  the superseding ADR themselves. On the branch the scenarios start with
  `/sa:add-requirements` (`Invoke:` line in `TASKS.md`), and every run also loaded
  `quality-requirements` and `domain-modeling`. One loophole round: the report now names the
  work each proposed ADR holds back.
- S06 (ticket 04, [campaign](campaigns/04-setup-fresh.md)): on `main`, "set up the
  architecture" became a coded program in turn 1, with nothing proposed to confirm and no
  arc42 or ADR. On the branch, turn 1 wrote only the skeleton and the proposal; the reply
  produced the R-list, measured goals, section 5's building-block table and a proposed
  ADR-0001. All branch runs of S01–S05 were
  re-run then, with the three new skills visible.
- S07 (ticket 05, [campaign](campaigns/05-setup-documented.md)): on `main`, turn 1 rewrote or
  duplicated the README's architecture and wrote new ADRs into the slot the "made centrally"
  ADR needs. On the branch, documents stay in place and legacy ADRs become
  `accepted (legacy)`. An earlier round filed an unmeasured goal (both S07 runs) and dropped
  single proposal items (two runs); the final re-run did not repeat them, which two runs
  cannot rule out. Every branch run was re-run with clean isolation.
- S08 (ticket 06, [campaign](campaigns/06-paradigm-neutral.md)): fixture `heating` with
  overlay `s08` (its README and `docs/`; until ticket 07 one fixture, `modelica`) is a
  Modelica library that checks with `omc`. On `main`, both runs implemented the accepted
  candidate in the `.mo` files, wrote no ADR ("no new ADR is needed") and tied no candidate to a
  quality goal. On the branch, every candidate cites an existing `QG-n`, the accepted change is
  a `proposed` ADR-0002, and no model changes. One loophole round: a run named the Modelica
  seam "partial base classes"; `codebase-design` now names constructs in the language's own
  words. Open loophole: one final run wrote a safety-net test for the accepted change before
  its ADR was accepted, and skipped turn 1's closing question.
- S09, S10 (ticket 07, [campaign](campaigns/07-setup-undocumented.md)): fixtures `undocumented`
  (`pantry`, a Python CLI) and `heating` without its docs. On `main`, every run wrote a whole
  architecture document in turn 1, proposed no "made centrally" list, marked nothing as found
  and wrote no ADR for a found decision; no run changed code. On the branch, turn 2 stops at
  ADR-0001 `proposed`; after its approval, arc42 sections 2–8 and 11 carry *As found,
  unconfirmed.* and only listed decisions become `proposed` ADRs. One loophole round gave
  dataflow blocks `in`/`out` columns in section 5. Open loopholes: S09-r2 filed an unmeasured
  goal; S10-r1's final message did not list the as-found sections for review. S06 and S07 were
  re-run because `setup-architecture` changed; S06-r2 ranked requirements without reasons (J1).
- S11–S14 (ticket 08, [campaign](campaigns/08-dialogue-and-spec.md)): fixtures `setup` with
  overlay `s03` (proposed ADR-0004) and `plain`. On `main`, the dialogue argued from R- and
  QS-IDs and ADRs but named no quality goal and treated encryption as an ADR, and the spec had
  no Quality Requirements section; both already treated ADR-0004 as open (no GREEN credit). On
  the branch, both pointers are gated on `docs/architecture/arc42.md` and name nothing else; the
  set-up guidance lives in `design-dialogue/references/architecture.md` and
  `spec-and-plan/references/quality-requirements.md`. One loophole round moved that guidance out
  of always-read text after the S13 and S14 controls each regressed once; the review fix pass
  made the dialogue pointer say what the reference changes and added `status_blocked` (a spec
  waiting for a proposed ADR is not `ready-for-agent`; both `main` runs failed it). Open: both
  final S11 runs build options on proposed ADR-0004 (J4, which `main` passed); an extra round
  approved by the architect brought that to 1 of 2 and cost one J3 hedge; S13-r2 mentions that
  the repo has no arc42 (J1). No S01–S10 run loads either skill, so none was re-run.
- S15–S17 (ticket 09, [campaign](campaigns/09-pause-on-proposed-adrs.md)): fixture `setup`
  with overlay `s15` (a plan whose Task 2, tags, needs a "decided centrally" format), and `s17`
  (the same plan plus a Task 2 brief). S17's prompt is the arm's own `implementer-prompt.md`
  (`Prompt-from:`). On `main`:
  - No run drafted an ADR.
  - S15-r1 ruled on tags and built them.
  - The other S15 and S16 runs paused from ADR-0002's own text but asked the architect to
    write the ADR, so S16 committed nothing to accept.
  - Both S17 subagents built tags and reported DONE_WITH_CONCERNS.

  On the branch, `executing-plans` points (gated on arc42) to
  `references/architecture-decisions.md`:
  - Every run drafts ADR-0004 `proposed`, leaves tags unwritten and finishes the independent
    task.
  - S16 commits the ADR and files no issue.
  - S17 reports `NEEDS_DECISION`.

  One loophole round moved the implementer's check into "Before You Begin" (S17 had built tags
  with the rule in its prompt). The review fix pass:
  - Subagents now commit the ADR (`adr_committed` added to S17).
  - S17 J1 was reworded: naming the architect as the decider passes, contacting them fails.
  - S18 was added, with a proposed ADR-0004 already in the fixture. Every branch run passed
    it before any fix; on `main` one run built tags.

  Open: S17-r2 split the decision into two ADRs, which `adr_proposed` does not accept. No
  S01–S14 run loads `executing-plans`, so none was re-run.
- Reviewed runs (flagged by `summarize.py`): `baseline/S02-r2`, where the grader's `cites_ids`
  failure stands because R-6 does not exist.

## Known gaps

- The unattended "PR containing only the ADR" path (design D17) is not exercised: fixtures have
  no pull-request remote.
- The CLI ships a built-in `code-review` skill, visible beside `sa:code-review` on both arms.
- Scenario prompts must carry the architect's answers up front: a `-p` run cannot answer
  questions, so a run that stops to ask ends there.
- Two runs per scenario cannot detect small effects.
- Runs share `HOME` with the machine's Claude installation: an agent can search
  `~/.claude` (baseline S07-r2 found "other projects' transcripts" and did not open them), and
  can load the machine's installed skills instead of the arm's `sa:` copies (branch S08-r2
  loaded `codebase-design` and `domain-modeling` that way).
- The account's usage limit can cut a run off mid-turn; the run then fails isolation on its
  exit code and must be re-run.
- S17 imitates a subagent: its prompt is the filled template, but no parent receives its
  `NEEDS_DECISION` report, so the parent's side (`handling-reports.md`) is not exercised. The
  grader also cannot see work done in a git worktree outside the checkout (ticket 09's first S15
  runs).
- Spec story 16 (a multi-context repo with `GLOSSARY-MAP.md`) has no fixture.
- Haiku 5.5 often works without loading a skill (S01: 0 of 4 runs; S02 on the branch: 1 of 4 in early runs, 2 of 2 in the ticket 04 re-run). A scenario
  whose point is a skill's behaviour must make that skill likely to load, or it measures the
  model alone.
