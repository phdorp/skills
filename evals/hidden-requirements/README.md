# Hidden-requirements benchmark

Measures how many of an architect's unstated requirements a design session finds, and whether
code built from the session's documents meets them. It compares `setup-architecture` (with
`quality-requirements`, `add-requirements` and `domain-modeling`) against
[mattpocock/skills](https://github.com/mattpocock/skills) `grill-me`, which hands off to
`grilling`.

The suite in `../software-architecture/` checks *process* (did the agent propose and wait?).
This benchmark checks *outcome*: requirements found, and the code built from them.

## How it works

- `project/README.md`: a three-sentence product idea (a kit tracker for a youth football club).
- `hidden.md`: twelve requirements H1–H12 that only the simulated architect knows.
- `architect-system.md`: the simulated architect (Sonnet 5.5, no tools). It answers only what a
  message asks or touches, corrects contradictions and confirms reasonable proposals.
- `drive.py <arm> <k>`: the design session. The designer is Haiku 5.5 at medium effort, isolated
  as in `../software-architecture/` (`--setting-sources project`, `--strict-mcp-config`, a clean
  environment, a workspace outside the repo). It allows at most 10 architect replies.
- `judge.py <run>`: Opus 5.5 scores each H as 2 (written into the documents accurately), 1
  (surfaced in the dialogue only, or written wrongly) or 0 (never surfaced).
- `implement.py <run>`: the code stage. A fresh Haiku 5.5 agent with **no skills** builds the
  first version from the run's documents alone, with no one to ask.
- `judge_code.py <run>`: Opus 5.5 scores the code against H1–H12 and rates its quality 1–10.
- `runtests.sh <run>`: runs the build's tests in a fresh venv.

Arms go in `arms/<arm>/sa/` (`skills/` plus `plugin.json`, built with `git archive <ref> skills
plugin.json`). For `grill`, put upstream `grill-me` and `grilling` there, with `grill-me`'s body
changed to `Call the Skill tool with "sa:grilling".` `arms/`, `runs/` and `venvs/` are not
committed. `results/` keeps each run's transcript, judgements and written documents.

## Results (2026-11-23/24)

| arm | skills | design score /24 (runs) | hidden reqs written | designer msgs | code score /24 | code quality |
|---|---|---|---|---|---|---|
| `setup` | branch at `ba2f17d` (gap questions) | 16, 7 | 8, 3 | 5, 3 | 19, 15 | 8, 6 |
| `grill` | upstream `grill-me` | 24, 19 | 12, 9 | 11 (cap), 8 | 23, 23 | 8, 8 |
| `setup2` | + Interview in rounds | 24, 24, 22 | 12, 12, 11 | 3, 5, 5 | 23, 20 | 7, 8 |
| `setup3` | + asks scale | 23, 24, 23 | 11, 12, 11 | 3, 3, 6 | – | – |
| `setup4` | + records figures and ruled-out qualities | 24, 24, 24 | 12, 12, 12 | 3, 3, 4 | 23, 22, 23 | 8, 8, 8 |
| `setup5` | + gap questions without a recommendation (final for fresh projects) | 24, 24 | 12, 12 | 5, 3 | – | – |

Every build's tests passed (47–115 tests). H12 (live by 1 March) can't be shown in code, so it
scores at most 1 there. `setup-r2`'s documents never recorded the Python-only maintainer, and
its build came out in Node.js.

Regression on the existing suite: [results/regression/](results/regression/README.md). Longer
first turns cost two process rules that the old runs passed. In S06 the "did you leave out"
question came with a pre-filled answer, which `setup5` removed. In undocumented projects (S09,
S10) the recovery report and the hold on sections 4–8 and 11 slipped, and the last two fixes
addressed those. On the final skills (`b219ab3`) 5 of 6 runs pass every grader check and 5 of 6
pass every judged criterion. The two misses come from steps this work did not change: S09-r15
proposed 7 ADRs where the grader allows 6, and S07-r14 named ADR-0003 `proposed` without saying
it waits for approval.

## Limits

- 2–3 runs per arm, one product, Haiku as designer and builder.
- The simulated architect gives a whole cluster of facts when a broad question touches them,
  which rewards open questions.
- The judge saw the hidden list. It quotes evidence for every score, but nobody reviewed the
  scores by hand.
