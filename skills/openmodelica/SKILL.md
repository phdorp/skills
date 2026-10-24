---
name: OpenModelica
description: Use when building, checking, or simulating Modelica models with OpenModelica - modelling a physical system, a modular model library, or validating and plotting simulation results.
---

# OpenModelica projects

This skill covers both a single model and a multi-module library. For a large project with
several coupled modules, also use `design-dialogue` and `spec-and-plan` to settle the structure
and requirements before writing equations.

The shell sandbox has OpenModelica 1.27 with the Modelica Standard Library 4.1.0 (offline), and
Python with numpy, scipy, pandas and matplotlib.

## Work in small, checked steps

A model that simulates is not yet a correct model: most wrong results run fine. So:

1. Write down what correct means before modelling: the requirements, and for each the behaviour
   that shows it (final or steady-state values, signs, bounds, conservation, a known analytic
   case). Compute every expected number with python3 before you simulate, never in your head (seen:
   a factor 2 lost in a tank's analytic solution); when it disagrees with the simulation, check the
   formula first (a second derivation, a limit), then the model. In a project, keep them as a
   checklist in NOTES.md under "Requirements", each with the check that covers it (an om-sim
   CHECK or an assert in a test model) and whether it passes.
2. Write a coarse plan into PLAN.md before any code: the structure (packages, interfaces, which
   parts are exchangeable) and 5-10 one-line steps. Break a step down into small ones (one file
   or class each, with the check that shows it works) only when you start it. Equations,
   frames, sign conventions and decisions go into PLAN.md's Notes as soon as you have them.
   Don't write the code in your thinking. Look up every library
   class you use (om-search, om-info, om-example) instead of writing its name, parameters or
   connectors from memory: names change between versions.
3. Write a minimal model first and run it with om-sim. Only continue once it simulates.
4. Add one component or variant at a time, writing each in its own file operation, and check
   again after each addition. Fix errors before adding anything else. Keep files short: one class
   or a few functions per file. Split a file over ~150 lines into classes rather than writing it
   in one operation.
5. After every change, run all checks again (om-test for the test models). Results from before
   the last edit don't count: never report them as the current state. Besides the checks per
   class, keep at least one test model that combines modules and compares with a known result
   (e.g. a body at rest on the rotating Earth: gravity plus frame rotation give the known
   effective gravity); it finds mismatched conventions between modules that single tests miss.
6. Done means every requirement's check passes on the current files. Before you call a task or
   ticket done (or change its status), read its acceptance criteria again and list each one
   with the check that proves it and that check's current result; a criterion without a passing
   check isn't done. Then tell the user the files, the main model to run, how to switch
   variants, and which checks pass.

## Modelica syntax: copy tested forms

[SyntaxCard.mo](SyntaxCard.mo), next to this skill, is one package with tested
forms of the common constructs: records as parameter sets and extending them, functions with
several outputs, a partial interface and models extending it, replaceable parts swapped with
redeclare, events (when/reinit/pre), values recorded at events (discrete), a value switched by two
events (hysteresis, algorithm section), sampled data (sample()), modes
switched by events (stick-slip friction), arrays with for loops, initial equations, library
components with connect, test models with assert. Copy from it instead of writing syntax from
memory. The forms omc reports most misleadingly:

- Inheritance: `extends Base;` on its own line inside the class, never in the header
  (`model B extends A` gives "No viable alternative near token: A").
- Changing an inherited value: `extends Base(mass = 100);`, not `redeclare parameter Real
  mass = 100` (that produces errors at unrelated lines).
- Parameter sets are records; a derived record in place of a base one needs `replaceable
  parameter Vehicle v;` and `extends Body(redeclare parameter Warhead v);`. A model can't be
  a parameter with a value.

A syntax error means your file differs from Modelica, not that omc is broken: OpenModelica
parses the whole standard library. Compare the reported line with the card and with real
library code (`om-example CLASS`) before anything else. Try out a construct in one scratch
folder (`probe/`), and delete it when you know the answer.

## Commands (run them in the shell; they are not tools)

    om-search TEXT [TEXT ...]          find library classes: om-search Translational Mass
    om-info CLASS                      parameters (defaults), connectors, equations, extends; a
                                       type's unit; "Use:" line
    om-example CLASS [COUNT]           how the library itself declares, connects or extends it
    om-sim FILE.mo CLASS [STOPTIME] [CHECK ...]
    om-test FILE.mo [NAME-PART]        simulate every model in Tests/Examples packages

om-sim checks and simulates one model, prints all errors and warnings, writes CLASS_res.csv next
to the model's file and ends with a summary (equations, variables, warnings, checks passed); when
it fails, the line before the summary says why. STOPTIME defaults to the model's
experiment(StopTime=...). CHECKs, quoted in the shell:

    h                      min, max (with times) and final value: judge behaviour by these
    max(v)                 a peak and the time it occurs (no need to read the CSV for it; for
                           a sharp peak set experiment(Interval = ...) finer)
    h@2                    value at t=2
    'h@2=1.2+-0.01'        PASS/FAIL; also <= >= < >; the value may be arithmetic: 'x@5=25/3+-0.01'
    'max(v)<=30'  'min(h)>=0'  'final(T)=293.15+-0.5'   final(n)   value at the end
    'events(n)'            the times a discrete variable (a counter, a value set in a when) changes:
                           measure event times with it instead of reading values at a guessed time

Checks work on variables and parameters (computed ones too); for an array (e0) they apply to
each element (e0[1], e0[2], ...). A FAIL is always a real failure, including "not in the
results" (a misspelled or protected name): fix it, don't explain it away. A bound missed by solver noise (about
1e-10 at an event) passes, marked as such. `tFree=2.5` without a time compares the final value of
a variable that changes only at events (a recorded event time, a counter).

Exit code 1 means loading, simulating or a check failed, or a unit error: read the errors, fix
the file, run again. "Class X not found" comes with the closest existing names. Messages that
point at the model, not at the tools:

- `UNIT ERROR`: an equation mixes units (`der(h) = m` with h a length, m a mass). It simulates,
  but the result is wrong. Fix the equation or the declared types.
- `TIME LIMIT`: a simulation stops after 60 s. Almost always chattering (an `if` or `when`
  condition switching back and forth at one point; "Chattering detected around time ..."), very
  many events, or a stiff model with an explicit solver: fix the model, e.g. with hysteresis
  or a `when` instead of an `if` on a state. Only a long run that is right gets more time:
  `OM_TIME_LIMIT=600 om-sim ...` with a shell timeout above it.
- "Assuming fixed start value for the following N variables": those states start from their
  start value (0 when none is given) because nothing fixes them. Give each state of your own
  models `(start = ..., fixed = true)` or an initial equation.
- An assertion violated "at time t" without a message: a built-in check failed there (sqrt or
  log of a negative argument, division by zero, a nonlinear system without a solution). Check the
  arguments just before t with VAR@T. A NOTE instead of a HINT marks a warning that did no harm
  (e.g. a solver step past the stop time): don't chase it.

Don't use plain omc scripts: they hide errors unless you call getErrorString().

om-test runs the test models (non-partial models in packages named Tests, TestCases or
Examples) with their experiment(StopTime=...), and prints PASS/FAIL per model with the violated
assert. Put lasting checks there as asserts, so one om-test call re-checks everything. A PASS
with "no assert" checks nothing but that the model simulates: it doesn't count for a requirement.

Both print the stop time a run used ("until t=5"). "(default)" means the model has no
experiment(StopTime=...) and ran for 1 s: give every model and test its StopTime.

om-sim works. If it fails, the error is in your model files, not in om-sim or omc: don't write
your own .mos scripts, `omc --cmd` calls or OMPython probes to work around it. Guessed scripting
calls fail with misleading errors (there is no `exists()`; `simulate("A.B")` with a string
argument gives "Class simulate not found").

For a library in a folder, write `package.mo` plus one file per class. Pass any one of its files
(e.g. `MyLib/package.mo` or the test model's file): om-sim loads the top-level `package.mo`, and
OpenModelica loads the whole folder from there. Each file starts with `within PackageName;`, and a
`package.order` file lists the classes in order.

Every folder is a package and needs its own file named exactly `package.mo`:

    MyLib/package.mo                 within ;                package MyLib end MyLib;
    MyLib/package.order              Sub
    MyLib/Sub/package.mo             within MyLib;           package Sub end Sub;
    MyLib/Sub/package.order          Model1 and Tests, one name per line
    MyLib/Sub/Model1.mo              within MyLib.Sub;       model Model1 ... end Model1;
    MyLib/Sub/Tests/package.mo       within MyLib.Sub;       package Tests end Tests;
    MyLib/Sub/Tests/Test1.mo         within MyLib.Sub.Tests; model Test1 ... end Test1;

A `package.mo` holds only the package line, its `end` and optionally constants or imports; the
classes in their own files are not declared in it (no `model Model1;` lines).

A file named like its folder (`Sub/Sub.mo`) is not loaded, and nothing below it either. The
`within` line is the folder path with dots, without the class itself. "Class MyLib.Sub.X not
found in scope <top>" means exactly this: a `package.mo` is missing or misnamed, or a `within`
line does not match the folder. Check with `find MyLib -name '*.mo'` and `head -2` of each file.

## Modelica rules that trip models up

- Plain ASCII only in .mo files, also in comments and description strings: no em-dashes, no
  degree signs, no Greek letters, no typographic quotes.
- Exchangeable parts: define a `partial model` (the interface), several models that `extend` it,
  and use them as `replaceable SomeVariant comp constrainedby Interface;`. Switch with
  `redeclare` in an example model: `extends Base(redeclare Variant2 comp);`.
- Real literals: `9.81`, not `9,81`; parameters need a value or a `start`; every variable needs
  exactly one equation (om-sim reports "too many/few equations" otherwise). A binding already is
  that equation: `Real x = 1.0;` must not get another `x = 1.0;` in the equation section, and a
  `parameter` never appears in the equation section.
- Function outputs are returned, not passed in: `ecef := ToECEF(lat, lon, alt);` and
  `(lat, lon, alt) := FromECEF(ecef);`, never `ToECEF(lat, lon, alt, ecef);`.
- Use Modelica.Units.SI types (`import Modelica.Units.SI;` as the line after `model Name`, then
  `SI.Length`) and Modelica.Constants (`pi`, `g_n`). Names that exist: Length, Height, Area, Volume,
  VolumeFlowRate, MassFlowRate, Time, Velocity, Acceleration, Mass, Force, Pressure, Density,
  Temperature, HeatFlowRate, HeatCapacity, ThermalConductance, Voltage, Current, Resistance,
  Capacitance, Inductance, Angle, AngularVelocity, Torque, Inertia. Not: Level, VolumeFlow, Speed
  (guessed in the evals). Others: `om-search SI WORD`.
- sqrt, exp, log, sin, cos, abs, min, max are built in: `sqrt(x)`, never `Modelica.Math.sqrt`.
- Use `der(x)` for derivatives, `when` for events and `reinit` for state jumps; `if` expressions
  need both branches.
- A `when` fires only at the instant its condition becomes true, and not again while it stays
  true: `when h <= 0 then` is "h has just reached 0". It needs no pre(h) > 0 and no extra guard
  against firing again (seen: two thinking loops over this).
- A function with a limited domain (sqrt, log, division) of a state that runs into its boundary
  (a tank running empty: sqrt(h)) needs the argument guarded: `sqrt(max(h, 0))`. An `if h > 0`
  around it or an event at h = 0 doesn't help: the solver evaluates the expression in trial steps
  past the boundary before either takes effect (seen in every tank run).
- If-expressions are allowed anywhere in an equation, also inside der() equations. After an
  operator they need parentheses: `der(h) = -(if full then q else 0);`, not `-if ...` (seen: read
  as "if is not allowed here", three thinking loops).

## Functions and test models

This pattern simulates; follow it (`om-sim Lib/Geo/Tests/RoundTrip.mo Lib.Geo.Tests.RoundTrip`):

    // Lib/Geo/package.mo
    within Lib;
    package Geo
      constant Real a = 6378137.0 "Semi-major axis, m";

      function toECEF
        input Real lat;
        input Real lon;
        input Real alt;
        output Real ecef[3];
      protected
        Real N "local variables: declared here, never inside the algorithm section";
      algorithm
        N := a;  // in an algorithm section always :=, never =
        ecef := {(N + alt)*cos(lat)*cos(lon), (N + alt)*cos(lat)*sin(lon), (N + alt)*sin(lat)};
      end toECEF;

      function fromECEF
        input Real ecef[3];
        output Real lat;
        output Real lon;
        output Real alt;
      algorithm
        lon := atan2(ecef[2], ecef[1]);
        lat := atan2(ecef[3], sqrt(ecef[1]^2 + ecef[2]^2));
        alt := sqrt(ecef[1]^2 + ecef[2]^2 + ecef[3]^2) - a;
      end fromECEF;
    end Geo;

    // Lib/Geo/Tests/RoundTrip.mo (plus Lib/Geo/Tests/package.mo)
    within Lib.Geo.Tests;
    model RoundTrip
      Real e[3] = Lib.Geo.toECEF(0, 0, 0);
      Real lat;
      Real lon;
      Real alt;
    equation
      (lat, lon, alt) = Lib.Geo.fromECEF(e);  // several outputs: a tuple equation
      assert(abs(e[1] - Lib.Geo.a) < 1e-3, "toECEF(0,0,0) wrong: " + String(e[1], significantDigits = 15));
      assert(abs(lat) < 1e-6 and abs(alt) < 1e-3, "round trip wrong: alt=" + String(alt, significantDigits = 15));
    end RoundTrip;

In a test model, give the checked values `Real` variables with an equation (a binding or the
equation section), not `parameter`s and not an `initial algorithm`: values set only there leave
the model with too few equations. A variable missing from the results was dropped by the solver
(it is a constant or an alias); check it with `assert` instead of VAR@TIME.

`String(x)` shows only 6 significant digits ("9.8062" for 9.8062012345), so a precision failure
reads like a pass. In assert messages write `String(x, significantDigits = 15)`.

Results are stored at output points only, 500 per run by default (om-sim prints "results every
... s"): VAR@T interpolates between them, and max(VAR) and min(VAR) miss a peak between two. For
short peaks or events, set `experiment(Interval = ...)` finer, or check inside the model (an
assert in a `when` at the event, or the peak tracked in a variable).

## Solvers

The solver is part of the model, in its annotation, so om-sim and om-test both use it:

    annotation(experiment(StopTime = 10, Tolerance = 1e-8),
      __OpenModelica_simulationFlags(s = "gbode", gbm = "radauIIA4"));

om-sim and om-test print the solver that actually ran ("Solver: gbode (radauIIA4), tolerance
1e-8"); read that line after changing it. Without `s` the solver is dassl. Tested in this
sandbox (OpenModelica 1.27):

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

- `radau5`, `radau3`, `lobatto6`, `impeuler` (old names): "unrecognized option -s" or "Unknown
  flag value", which lists the valid gbm names.
- `experiment(__OpenModelica_Algorithm = "radau5")` or `__Dymola_Algorithm = "Radau"`: ignored,
  the model runs with dassl; om-sim prints a WARNING.
- The gbm without `s = "gbode"`: ignored.
- `symSolver` (needs a compiler flag), `qss` (experimental, wrong at events): don't use.

gbode prints "Numerical Jacobians without coloring are currently not supported by GBODE":
harmless, om-sim hides it. A result's accuracy is bounded by the tolerance: a check against an
analytic value needs a tolerance looser than the solver's, e.g. 1e-6 relative with Tolerance
= 1e-8.

## Standard Library conventions

The library's conventions may differ from the project's (its conventions ADR). Where a ticket
uses a library class, convert at its connectors and test the conversion:

- Quaternions (`Modelica.Mechanics.MultiBody.Frames.Quaternions`): **scalar last**,
  `Q = {n*sin(phi/2), cos(phi/2)}`, so `Q[4]` is the scalar part.
- Orientations are **passive**: `Frames.Orientation` R holds `T`, the transformation matrix from
  frame 1 (usually world) to frame 2 (local); `resolve2(R, v1)` gives the same vector's
  coordinates in frame 2, `resolve1(R, v2)` back. Nothing is rotated.
- `World`: uniform gravity `g = g_n` along `n = {0, -1, 0}`, i.e. **minus y is down**; point
  gravity with `gravityType = PointGravity` and `mu`. Set both explicitly.
- `Parts.Body`: quaternion states by default (`useQuaternions = true`); Euler angle states use
  `sequence_angleStates = {1, 2, 3}`. A Body without `r_CM` warns "Parameter body.r_CM has no
  value": harmless, it uses {0, 0, 0}; give `r_CM` to silence it.
- Angles in radians (`Modelica.Units.Conversions.from_deg`), all units SI.
- `Translational.Components.Mass` (and the other sliding masses) has a length `L` (default 1 m):
  its flanges sit at `s - L/2` and `s + L/2`, and `s` is its centre.
  With a `Fixed` at s0 = 0 and a spring with `s_rel0 = 0`, set `L = 0`; then `mass.s` is the
  displacement from the spring's rest position (seen: L = 0.2 left the spring unstretched).

## Results

Judge results by numbers (om-sim VAR and checks), not by looking at plots. For the user, plot
with Python (matplotlib, `matplotlib.use("Agg")`) from CLASS_res.csv and save PNGs in the
project folder. Tell the user their paths.
