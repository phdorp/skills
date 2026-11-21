# OpenModelica skill benchmark

Measures whether the `openmodelica` skill changes the outcome of Modelica modelling tasks,
against agents that work without it. Re-run it when the model or the skill changes.

## Contents

- `TASKS.md`: eight tasks (T1–T8), given verbatim to each agent in an empty directory.
- `grader/`: `grade.py` grades one run directory with omc; `summarize.py` grades every run and
  writes `results/<arm>.json`; `selftest.py` checks the grader against `reference/` solutions
  (every check passes) and `broken/` variants (each fails exactly the checks it should).
- `runs/<arm>/<task>-r<k>/`: the source files each agent left (build output removed).
- `results/`: grades of the runs below.

## Run it

Needs OpenModelica 1.27 with MSL 4.1.0 and python3 (standard library only).

```sh
cd evals/openmodelica/grader
python3 -I selftest.py -j 3          # grader self-test
python3 -I summarize.py ../runs -j 3 # grade every run, write ../results/<arm>.json
```

To add a run, give an agent one task from `TASKS.md` in an empty directory under
`runs/<arm>/<task>-r<k>/`, with or without the skill loaded.

## Results (2026-11, Opus 5.5, OpenModelica 1.27.2, 2 runs per task and arm)

| task | no skill | skill |
|---|---:|---:|
| T1 tank | 1.000 | 1.000 |
| T2 ball | 1.000 | 1.000 |
| T3 mass-spring-damper | 1.000 | 1.000 |
| T4 vehicle library | 1.000 | 1.000 |
| T5 pendulum (MultiBody) | 1.000 | 1.000 |
| T6 Robertson (stiff) | 0.909 | 0.909 |
| T7 thermostat | 1.000 | 1.000 |
| T8 fleet library | 0.964 | 1.000 |
| cost, all 16 runs | ≈ $5.5 | ≈ $16 |

- No difference in correctness. Every T6 miss is gbode's harmless "Numerical Jacobians without
  coloring" warning, which the grader counts strictly. The no-skill T8 miss is a grader false
  negative: that run's asserts live in a partial base model the tests extend, and the grader
  only looks for `assert` in the test files.
- With the skill, agents kept test models with asserts and ran `scripts/run_tests.py`, which
  caught a redeclare that dropped its modifiers (`runs/skill/T4-r1`) and an `==` on Reals
  (`runs/skill/T8-r1`) before they reported. Both are now gotchas in the skill.
- 17 agents shared 4 cores, so wall times are not comparable and the skill arm's cost is
  inflated by agents waiting on compiles. Two runs per task cannot detect small effects, and
  T1–T4 sit at the ceiling for this model.

## Known gaps

- The grader misses asserts inherited from a base model (see T8 above).
- No task covers a large multi-file project, where the skill's planning steps would matter.
