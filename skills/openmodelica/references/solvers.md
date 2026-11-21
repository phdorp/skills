# Choosing a solver

The solver is part of the model, in its annotation, so `simulate()` and `run_tests.py` both use it:

    annotation(experiment(StopTime = 10, Tolerance = 1e-8),
      __OpenModelica_simulationFlags(s = "gbode", gbm = "radauIIA4"));

The `simflags` field of the `simulationOptions` that `simulate()` prints shows the flags that ran
(`simflags = '-s=\'gbode\' -gbm=\'radauIIA4\''`); its `method` field says `dassl` whatever ran.
Read that field after changing the solver. Without `s` the solver is dassl. A `simflags`
argument to `simulate()` replaces the annotation's flags, so repeat the solver there:
`simflags = "-alarm=60 -s=gbode -gbm=radauIIA4"`. Tested with OpenModelica 1.27:

| s = | gbm = | Use |
|---|---|---|
| `"dassl"` (default) | | BDF, variable step and order, stiff and non-stiff: the safe choice |
| `"ida"`, `"cvode"` | | SUNDIALS BDF (cvode also Adams); ida with a sparse solver for large models |
| `"gbode"` | `"radauIIA2"` ... `"radauIIA7"` | Radau IIA, implicit, L-stable, for stiff models; the number is the stages, order 2n-1 (radauIIA4: order 7) |
| `"gbode"` | `"radauIA2"` ... `"radauIA4"`, `"lobattoIIIA3"`, `"lobattoIIIA4"` (also IIIB, IIIC), `"gauss2"` ... `"gauss6"` | other implicit Runge-Kutta families |
| `"gbode"` | `"sdirk2"` ... `"sdirk4"`, `"esdirk2"` ... `"esdirk4"`, `"esdirk4s7"`, `"impl_euler"`, `"trapezoid"`, `"adams"` | cheaper implicit methods |
| `"gbode"` | `"dopri45"`, `"tsit5"`, `"fehlberg45"`, `"fehlberg78"`, `"rk810"`, `"rk1012"`, `"rk1214"`, `"merson"`, `"heun"`, `"expl_euler"`, `"rungekutta"` | explicit, variable step: smooth non-stiff models (orbits, trajectories) |
| `"euler"`, `"rungekutta"` | | fixed step: one step per output interval, set with `experiment(Interval = 1e-3)`; Tolerance doesn't apply |

Stiff (fast and slow time constants together, e.g. stiff springs, chemistry, controllers): dassl,
ida or a Radau gbm. Forms that look right but are wrong:

- `radau5`, `radau3`, `lobatto6`, `impeuler` (old names): the simulation fails with "unrecognized
  option -s radau5" or 'Unknown flag value "radau5" for flag gbm.', followed by the valid names.
- `experiment(__OpenModelica_Algorithm = "radau5")` or `__Dymola_Algorithm = "Radau"`: ignored
  without a message; the model runs with dassl and `simflags = ''`.
- The gbm without `s = "gbode"`: ignored without a message, dassl runs.
- `symSolver` (needs the compiler flag `--symSolver`), `qss` (experimental): use the solvers above.

gbode prints "Numerical Jacobians without coloring are currently not supported by GBODE" as a
runtime warning: harmless, and `run_tests.py` ignores it. A result's accuracy is bounded by the
tolerance: a check against an analytic value needs a tolerance looser than the solver's, e.g.
1e-6 relative with Tolerance = 1e-8.
