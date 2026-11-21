# Software architecture scenario suite

Measures whether the software-architecture skill set (spec:
`docs/specs/2026-11-21-software-architecture-skill-set-spec.md`) changes what an agent does,
against the skills at `main`. Re-run it when the model or the skills change.

## Contents

- `TASKS.md`: scenarios (S01…), each a prompt given verbatim to a fresh agent on a copy of one
  fixture.
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
  that saw a foreign plugin or a user skill is saved with `isolation_ok: false` and left out of
  the scores.
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
| S02 record-decision | 0.785 | 0.834 | 0.928 | 0.666 | 1 of 2 |
| S03 lifecycle | 0.400 | 0.000 | 1.000 | 1.000 | 2 of 2 |

Cost so far: about $0.80 per arm (runs ≈ $0.10, judge ≈ $0.70). Each run takes 20–60 s.

- S01: no run loaded a skill on either arm. It shows an ordinary change stays ordinary, not
  that the skills stay quiet once loaded.
- S02, S03 (ticket 02, [campaign](campaigns/02-adr-rules.md)): on `main`, agents accepted their
  own ADRs, marked the replaced ADR superseded early, and added requirements on their own. Every
  branch run that loaded `domain-modeling` followed every rule; the branch S02 run that did not
  load it accepted its own ADR again. Open loophole: the skill does not load reliably for
  "record the decision as an ADR".
- Reviewed runs (flagged by `summarize.py`): `baseline/S02-r2`, where the grader's `cites_ids`
  failure stands because R-6 does not exist.

## Known gaps

- The unattended "PR containing only the ADR" path (design D17) is not exercised: fixtures have
  no pull-request remote.
- The CLI ships a built-in `code-review` skill, visible beside `sa:code-review` on both arms.
- Scenario prompts must carry the architect's answers up front: a `-p` run cannot answer
  questions, so a run that stops to ask ends there.
- Two runs per scenario cannot detect small effects.
- Haiku 5.5 often works without loading a skill (S01: 0 of 4 runs; S02: 1 of 4 on the branch). A scenario
  whose point is a skill's behaviour must make that skill likely to load, or it measures the
  model alone.
