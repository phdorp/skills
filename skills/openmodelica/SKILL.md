---
name: openmodelica
description: Use when building, checking, or simulating Modelica models with OpenModelica - modelling a physical system, a modular model library, or validating and plotting simulation results.
---

# OpenModelica projects

This skill covers both a single model and a multi-module library. For a large project with
several coupled modules, also use `design-dialogue` and `spec-and-plan` to settle the structure
and requirements before writing equations.

The shell has OpenModelica 1.27 (`omc`) with the Modelica Standard Library 4.1.0 (offline), and
python3; the sandbox also has numpy, scipy, pandas and matplotlib.

Load a reference when the task reaches it:

- [references/library-layout.md](references/library-layout.md): the project spans several
  files or folders, or omc reports "Class MyLib.X not found in scope <top>".
- [references/solvers.md](references/solvers.md): choosing a solver, a stiff model, or a run
  that is slow or ends in a solver error.
- [references/msl-conventions.md](references/msl-conventions.md): the model uses MultiBody
  (frames, quaternions, World, Body) or Translational masses with springs.

## Work in small, checked steps

A model that simulates is not yet a correct model: most wrong results run fine. So:

1. Write down what correct means before modelling: the requirements, and for each the behaviour
   that shows it (final or steady-state values, signs, bounds, conservation, a known analytic
   case). Compute every expected number with python3 before you simulate, never in your head (seen:
   a factor 2 lost in a tank's analytic solution); when it disagrees with the simulation, check the
   formula first (a second derivation, a limit), then the model. In a project, keep them as a
   checklist in NOTES.md under "Requirements", each with the check that covers it (an assert in
   a test model) and whether it passes.
2. Write a coarse plan into PLAN.md before any code: the structure (packages, interfaces, which
   parts are exchangeable) and 5-10 one-line steps. Break a step down into small ones (one file
   or class each, with the check that shows it works) only when you start it. Equations,
   frames, sign conventions and decisions go into PLAN.md's Notes as soon as you have them.
   Don't write the code in your thinking. Look up every library class you use (see "Look up
   library classes") instead of writing its name, parameters or connectors from memory: names
   change between versions.
3. Write a minimal model first and simulate it. Only continue once it simulates without errors
   or warnings.
4. Add one component or variant at a time, writing each in its own file operation, and check
   again after each addition. Fix errors before adding anything else. Keep files short: one class
   or a few functions per file. Split a file over ~150 lines into classes rather than writing it
   in one operation.
5. After every change, run all checks again (`run_tests.py` for the test models). Results from
   before the last edit don't count: never report them as the current state. Besides the checks
   per class, keep at least one test model that combines modules and compares with a known result
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
  parameter Vehicle v;` and `extends Body(redeclare parameter Variant v);`. A model can't be
  a parameter with a value.

A syntax error means your file differs from Modelica, not that omc is broken: OpenModelica
parses the whole standard library. Compare the reported line with the card and with real
library code (see "Look up library classes") before anything else. Try out a construct in one
scratch folder (`probe/`), and delete it when you know the answer.

## Simulate one model: a .mos script

omc runs a script of scripting calls. Keep one per model you work on, e.g. `sim.mos` next to it:

    loadModel(Modelica, {"4.1.0"}); getErrorString();
    loadFile("../Tank.mo"); getErrorString();
    checkModel(Tank); getErrorString();
    simulate(Tank, stopTime = 10, outputFormat = "csv", simflags = "-alarm=60"); getErrorString();

Run it from a build folder, because omc writes some 60 build files per model into the working
directory: `mkdir -p build && cd build && omc ../sim.mos`. Paths in the script are relative to
that folder; for a library, load its top-level `package.mo`.

- A failing call prints only `false` or `""`; its message waits in `getErrorString()`, which is
  why every call above is followed by one. omc exits 0 even when the simulation failed: read the
  output.
- `checkModel` prints the equation and variable counts and is the only call that checks units.
  It can report success for a model with too few equations; `simulate` then fails with "Too few
  equations".
- `simulate` prints a record: `resultFile` (`""` when the run failed), `simulationOptions` (the
  stop time, tolerance and flags that ran) and `messages` (the runtime log: violated asserts,
  solver trouble). Leave out `stopTime` to use the model's `experiment(StopTime = ...)`; without
  one it runs for 1 s, so give every model and test its StopTime.
- `simflags = "-alarm=60"` stops the run after 60 s ("Alarm clock" in `messages`). It replaces
  the model's `__OpenModelica_simulationFlags`; for a model that sets its solver there, repeat it:
  `simflags = "-alarm=60 -s=gbode -gbm=radauIIA4"`.
- Name classes without quotes: `simulate(A.B)`. `simulate("A.B")` gives "Class simulate not
  found in scope <global scope>". Guessed calls fail the same way (there is no `exists()`; use
  `isModel(A.B)`). Look up a call before using it: `getClassNames(OpenModelica.Scripting)` lists
  all of them, `list(OpenModelica.Scripting.simulate, interfaceOnly = true)` shows one's inputs.

## Run the test models

    python3 SKILL_DIR/scripts/run_tests.py FILE.mo [NAME-PART ...] [--timeout SECONDS]

SKILL_DIR is the folder holding this file; the script is executed, not read. It loads FILE.mo
(for a library, any of its files) with the Standard Library, runs checkModel and simulate on every
non-partial model in a package named Tests, TestCases or Examples with its own experiment
annotation, and prints PASS or FAIL per model with the stop time used and the omc and runtime
messages behind a FAIL. Any error, warning, violated assert or failed simulation fails a model;
exit code 0 means all passed. Put lasting checks into test models as asserts, so one call
re-checks everything. A test model without an assert checks only that the model simulates: it
doesn't count for a requirement.

## Look up library classes

The Standard Library's source is in `~/.openmodelica/libraries/Modelica 4.1.0+maint.om/`, one
folder per package. In a script after `loadModel(Modelica, {"4.1.0"});`:

    getClassNames(Modelica.Mechanics.Translational.Components); getErrorString();  // a package's classes
    instantiateModel(Modelica.Mechanics.Translational.Components.Mass); getErrorString();
    list(Modelica.Mechanics.Translational.Components.Mass); getErrorString();  // source as written
    getSourceFile(Modelica.Mechanics.Translational.Components.Mass); getErrorString();

`instantiateModel` shows every parameter with its unit and default, every connector variable and
every equation, inherited ones included; `getParameterNames` leaves out inherited parameters
(Mass's `L`). To find a class by a word, or how the library itself declares, connects or extends
it, grep the source:

    grep -rln "Components.Mass" ~/.openmodelica/libraries/"Modelica 4.1.0+maint.om"/Mechanics/Translational/Examples

## Read results

Judge results by numbers, not by looking at plots. With `outputFormat = "csv"` the result is
`CLASS_res.csv` in the build folder, one column per variable:

    python3 -c "
    import csv
    rows = list(csv.DictReader(open('Tank_res.csv')))
    t = [float(r['time']) for r in rows]; h = [float(r['h']) for r in rows]
    print(min(h), max(h), h[-1], next(v for s, v in zip(t, h) if s >= 4))"

With the default outputFormat (mat), `val(h, 4.0, "Tank_res.mat")` in a script gives one value;
val() can't read csv. After a failed run the file still holds the values up to the failure,
though `resultFile` is `""`: read the variables just before the failure time there.

Results are stored at output points only, 500 per run by default: a peak or an event between two
points is missed. For short peaks or events, set `experiment(Interval = ...)` finer, or check
inside the model (an assert in a `when` at the event, or the peak tracked in a variable). The
CSV leaves out parameters; the .mat result holds them (`val(k, 0, "Tank_res.mat")`).

For the user, plot with Python (matplotlib, `matplotlib.use("Agg")`) from the CSV and save PNGs
in the project folder. Tell the user their paths.

## Messages

Compile-time messages come from `getErrorString()`, runtime messages in `simulate`'s `messages`.
Those that point at the model, not at omc:

- "Warning: The following equation is INCONSISTENT due to specified unit information: der(h) =
  m", then the unit of each side (from checkModel): the equation mixes units. It simulates, but
  the result is wrong. Fix the equation or the declared types.
- "Warning: The initial conditions are not fully specified.": some states start from their start
  value (0 when none is given) because nothing fixes them. Add
  `setCommandLineOptions("-d=initialization");` before `simulate` to list them ("Assuming fixed
  start value for the following N variables"). Give each state of your own models
  `(start = ..., fixed = true)` or an initial equation.
- "The following assertion has been violated at time 0.500000" followed by `((x < 0.5)) -->
  "message"`: your assert, at that time. Followed by "Model error: Argument of sqrt(h) was
  -0.00052 should be >= 0" or by nothing: a built-in check failed there (sqrt or log of an
  argument out of its domain). "Variable violating min constraint: 0.0 <= h" means a variable
  crossed its type's min or max (SI.Height has min = 0). Read the arguments just before that time
  in the result file.
- A run that doesn't end: "Alarm clock" with `-alarm`, or no result from `run_tests.py` before
  its timeout. Almost always chattering (an `if` or `when` condition switching back and forth at
  one point; `messages` shows "Chattering detected around time ..."), very many events, or a stiff
  model with an explicit solver: fix the model, e.g. with hysteresis or a `when` instead of an
  `if` on a state. Only a long run that is right gets more time (`-alarm=600`, `--timeout 600`).

## Modelica rules that trip models up

- Plain ASCII only in .mo files, also in comments and description strings: no em-dashes, no
  degree signs, no Greek letters, no typographic quotes.
- Exchangeable parts: define a `partial model` (the interface), several models that `extend` it,
  and use them as `replaceable SomeVariant comp constrainedby Interface;`. Switch with
  `redeclare` in an example model: `extends Base(redeclare Variant2 comp);`.
- Real literals: `9.81`, not `9,81`; parameters need a value or a `start`; every variable needs
  exactly one equation (simulate reports "Too few equations" or "Too many equations" otherwise).
  A binding already is that equation: `Real x = 1.0;` must not get another `x = 1.0;` in the
  equation section, and a `parameter` never appears in the equation section.
- Function outputs are returned, not passed in: `ecef := ToECEF(lat, lon, alt);` and
  `(lat, lon, alt) := FromECEF(ecef);`, never `ToECEF(lat, lon, alt, ecef);`.
- Use Modelica.Units.SI types (`import Modelica.Units.SI;` as the line after `model Name`, then
  `SI.Length`) and Modelica.Constants (`pi`, `g_n`). Names that exist: Length, Height, Area, Volume,
  VolumeFlowRate, MassFlowRate, Time, Velocity, Acceleration, Mass, Force, Pressure, Density,
  Temperature, HeatFlowRate, HeatCapacity, ThermalConductance, Voltage, Current, Resistance,
  Capacitance, Inductance, Angle, AngularVelocity, Torque, Inertia. Not: Level, VolumeFlow, Speed
  (guessed in the evals). Others: `getClassNames(Modelica.Units.SI)`.
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

This pattern simulates; follow it (`python3 SKILL_DIR/scripts/run_tests.py Lib/package.mo RoundTrip`):

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

    // Lib/Geo/Tests/RoundTrip.mo (plus Lib/package.mo and Lib/Geo/Tests/package.mo)
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
      annotation(experiment(StopTime = 1));
    end RoundTrip;

In a test model, give the checked values `Real` variables with an equation (a binding or the
equation section), not `parameter`s and not an `initial algorithm`: values set only there leave
the model with too few equations.

`String(x)` shows only 6 significant digits ("9.8062" for 9.8062012345), so a precision failure
reads like a pass. In assert messages write `String(x, significantDigits = 15)`.
