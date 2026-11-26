### user

/sa:improve-codebase-architecture Look for architecture improvements in HeatingLib. I'm not available for questions until you
have the report ready.

### assistant

I'll start by reading the skill's report template, the project's domain docs and ADRs, and the recent history of HeatingLib.

### tool_use Bash

```json
{
 "command": "git log --oneline | head -50 && echo --- && git log --since=\"6 months ago\" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -40 && echo --- && ls -la && echo --- && find . -path ./node_modules -prune -o -path ./.git -prune -o -type f -print | head -300",
 "description": "Inspect repo history, hot files, and layout"
}
```

### tool_result

```
421e27c fixture
---
      1 tests/check.mos
      1 docs/architecture/arc42.md
      1 docs/adr/0001-record-architecture-decisions.md
      1 README.md
      1 HeatingLib/package.order
      1 HeatingLib/package.mo
      1 HeatingLib/Thermostat.mo
      1 HeatingLib/System.mo
      1 HeatingLib/Room.mo
      1 HeatingLib/Interfaces.mo
---
total 28
drwxr-xr-x 6 root root 4096 Nov 21 21:01 .
drwx------ 3 root root 4096 Nov 21 21:01 ..
drwxr-xr-x 8 root root 4096 Nov 21 21:01 .git
drwxr-xr-x 2 root root 4096 Nov 21 20:59 HeatingLib
-rw-r--r-- 1 root root  336 Nov 21 20:59 README.md
drwxr-xr-x 4 root root 4096 Nov 21 20:59 docs
drwxr-xr-x 2 root root 4096 Nov 21 20:59 tests
---
./README.md
./HeatingLib/package.order
./HeatingLib/System.mo
./HeatingLib/Thermostat.mo
./HeatingLib/Interfaces.mo
./HeatingLib/Room.mo
./HeatingLib/package.mo
./tests/check.mos
./docs/adr/0001-record-architecture-decisions.md
./docs/architecture/arc42.md
```

### tool_use Bash

```json
{
 "command": "cat /tmp/sa-arm-ztzxghfk/sa/skills/improve-codebase-architecture/HTML-REPORT.md",
 "description": "Read the HTML report scaffold guidance"
}
```

### tool_result

```
# HTML Report Format

The architectural review is rendered as a single self-contained HTML file in the OS temp directory. Tailwind and Mermaid both come from CDNs. Mermaid handles graph-shaped diagrams reliably; hand-built divs and inline SVG handle the more editorial visuals (mass diagrams, cross-sections). Mix the two: don't lean on Mermaid for everything, it'll start to look generic.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Repo name, date, and a compact legend: solid box = module, dashed line = seam, red arrow = leakage, thick dark box = deep module. No introduction paragraph. Straight into the candidates.

## Candidate card

The diagrams carry the weight. Prose is sparse, plain, and uses the glossary terms (from the `/codebase-design` skill) without ceremony.

Each candidate is one `<article>`:

- **Title**: short, names the deepening (e.g. "Collapse the Order intake pipeline").
- **Badge row**: recommendation strength (`Strong` = emerald, `Worth exploring` = amber, `Speculative` = slate), plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`).
- **Files**: monospaced list, `font-mono text-sm`.
- **Before / After diagram**: the centrepiece. Two columns, side by side. See patterns below.
- **Problem**: one sentence. What hurts.
- **Solution**: one sentence. What changes.
- **Wins**: bullets, ≤6 words each. e.g. "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR callout** (if applicable): one line in an amber-tinted box.

No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same. Variety is part of the point.

### Mermaid graph (the workhorse for dependencies / call flow)

Use a Mermaid `flowchart` or `graph` when the point is "X calls Y calls Z, and look at the mess." Wrap it in a Tailwind-styled card so it doesn't feel parachuted in. Style with classDef to colour leakage edges red and the deep module dark. Sequence diagrams work well for "before: 6 round-trips; after: 1."

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### Hand-built boxes-and-arrows (when Mermaid's layout fights you)

Modules as `<div>`s with borders and labels. Arrows as inline SVG `<line>` or `<path>` elements positioned absolutely over a relative container. Reach for this when you want the "after" diagram to feel like one thick-bordered deep module with greyed-out internals, since Mermaid won't render that with the right weight.

### Cross-section (good for layered shallowness)

Stack horizontal bands (`h-12 border-l-4`) to show layers a call passes through
[... 2633 chars cut]
```

### tool_use Skill

```json
{
 "skill": "sa:codebase-design"
}
```

### tool_result

```
Launching skill: sa:codebase-design
```

### assistant

The repo is small (a Modelica library), so I'll read the sources directly rather than spawn a sub-agent.

### tool_use Bash

```json
{
 "command": "for f in README.md HeatingLib/package.order HeatingLib/package.mo HeatingLib/Interfaces.mo HeatingLib/Room.mo HeatingLib/Thermostat.mo HeatingLib/System.mo tests/check.mos docs/adr/0001-record-architecture-decisions.md docs/architecture/arc42.md; do echo \"=================== $f\"; cat -n \"$f\"; done",
 "description": "Read all project sources and docs"
}
```

### tool_result

```
=================== README.md
     1	# HeatingLib
     2	
     3	A Modelica library that heats one room: `Room` stores and loses heat, `Thermostat` sets the
     4	heating power from the measured temperature, `System` connects them.
     5	
     6	Check the library with OpenModelica:
     7	
     8	```sh
     9	omc tests/check.mos
    10	```
    11	
    12	The architecture is described in [docs/architecture/arc42.md](docs/architecture/arc42.md).
=================== HeatingLib/package.order
     1	roomHeatCapacity
     2	Interfaces
     3	Room
     4	Thermostat
     5	System
=================== HeatingLib/package.mo
     1	within ;
     2	package HeatingLib "Room heating: a room, a thermostat and the system that connects them"
     3	  constant Real roomHeatCapacity(unit = "J/K") = 5e5
     4	    "Heat capacity of the room; read by Room and by Thermostat";
     5	end HeatingLib;
=================== HeatingLib/Interfaces.mo
     1	within HeatingLib;
     2	package Interfaces "Connectors and units shared by all blocks"
     3	  type Temperature = Real(final quantity = "ThermodynamicTemperature", final unit = "K",
     4	    min = 0, displayUnit = "degC");
     5	  type HeatFlowRate = Real(final quantity = "Power", final unit = "W");
     6	  connector TemperatureInput = input Temperature "Temperature signal into a block";
     7	  connector TemperatureOutput = output Temperature "Temperature signal out of a block";
     8	  connector HeatFlowInput = input HeatFlowRate "Heating power signal into a block";
     9	  connector HeatFlowOutput = output HeatFlowRate "Heating power signal out of a block";
    10	end Interfaces;
=================== HeatingLib/Room.mo
     1	within HeatingLib;
     2	model Room "Lumped room air: stores heat, loses it through the walls"
     3	  parameter Real C(unit = "J/K") = HeatingLib.roomHeatCapacity "Heat capacity";
     4	  parameter Real G(unit = "W/K") = 150 "Heat loss conductance of the walls";
     5	  parameter Interfaces.Temperature T_amb = 273.15 "Outdoor temperature";
     6	  parameter Interfaces.Temperature T_start = 288.15 "Initial room temperature";
     7	  Interfaces.HeatFlowInput Q_heat "Heating power into the room";
     8	  Interfaces.TemperatureOutput T "Room temperature";
     9	initial equation
    10	  T = T_start;
    11	equation
    12	  C * der(T) = Q_heat - G * (T - T_amb);
    13	end Room;
=================== HeatingLib/Thermostat.mo
     1	within HeatingLib;
     2	block Thermostat "Proportional heating controller with a set point"
     3	  parameter Interfaces.Temperature T_set = 293.15 "Set point";
     4	  parameter Real tau(unit = "s") = 1800 "Time to close the gap to the set point";
     5	  parameter Interfaces.HeatFlowRate Q_max = 3000 "Heater power limit";
     6	  Interfaces.TemperatureInput T "Measured room temperature";
     7	  Interfaces.HeatFlowOutput Q "Heating power demand";
     8	protected
     9	  // The gain needs the room's heat capacity, so it is read from the package constant
    10	  // the room model uses as well.
    11	  parameter Real k(unit = "W/K") = HeatingLib.roomHeatCapacity / tau "Controller gain";
    12	equation
    13	  Q = min(Q_max, max(0, k * (T_set - T)));
    14	end Thermostat;
=================== HeatingLib/System.mo
     1	within HeatingLib;
     2	model System "A room heated by a thermostat-controlled heater"
     3	  Room room;
     4	  Thermostat thermostat;
     5	equation
     6	  connect(room.T, thermostat.T);
     7	  connect(thermostat.Q, room.Q_heat);
     8	  annotation(experiment(StopTime = 86400));
     9	end System;
=================== tests/check.mos
     1	// Run from the project root: omc tests/check.mos
     2	loadFile("HeatingLib/package.mo"); getErrorString();
     3	checkModel(HeatingLib.System); getErrorString();
=================== docs/adr/0001-record-architecture-decisions.md
     1	# 1. Record architecture decisions
     2	
     3	## Status
     4	
     5	accepted 2026-10-01
     6	
     7	## Context
     
[... 3988 chars cut]
```

### assistant

I've read every source file and doc. One thing needs checking before I write it up: `Thermostat` reads `HeatingLib.roomHeatCapacity` directly, which the arc42 may-use table doesn't allow. I'll see whether OpenModelica is available so I can verify the model behaviour as well as read it.

### tool_use Bash

```json
{
 "command": "which omc xdg-open open 2>&1; echo \"TMPDIR=${TMPDIR:-unset}\"; date +%Y%m%d-%H%M%S; echo ---; grep -rn \"roomHeatCapacity\\|C(\" HeatingLib/ ; echo ---; if command -v omc >/dev/null; then timeout 120 omc tests/check.mos 2>&1 | tail -20; fi",
 "description": "Check for OpenModelica, temp dir, and coupling references"
}
```

### tool_result

```
/usr/bin/omc
/usr/bin/open
TMPDIR=unset
20261121-210149
---
HeatingLib/package.order:1:roomHeatCapacity
HeatingLib/package.mo:3:  constant Real roomHeatCapacity(unit = "J/K") = 5e5
HeatingLib/Thermostat.mo:11:  parameter Real k(unit = "W/K") = HeatingLib.roomHeatCapacity / tau "Controller gain";
HeatingLib/Room.mo:3:  parameter Real C(unit = "J/K") = HeatingLib.roomHeatCapacity "Heat capacity";
---
true
""
"Check of HeatingLib.System completed successfully.
Class HeatingLib.System has 4 equation(s) and 4 variable(s).
2 of these are trivial equation(s)."
""
```

### assistant

OpenModelica is installed and `check.mos` passes. Since `Room.C` and `Thermostat.k` are both derived from the same package constant, I'll probe the effect by overriding `room.C` in a scratch model outside the repo. This is a baseline run and a run with the room's heat capacity doubled.

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/arch-probe && cd /tmp/arch-probe && cat > ProbeBigRoom.mo <<'EOF'\nmodel ProbeBigRoom \"Room with twice the heat capacity; Thermostat unchanged\"\n  extends HeatingLib.System(room(C = 1e6));\nend ProbeBigRoom;\nEOF\ncat > run.mos <<'EOF'\nloadFile(\"/tmp/sa-eval-wd2gqb_e/project/HeatingLib/package.mo\");\nloadFile(\"/tmp/arch-probe/ProbeBigRoom.mo\");\nsimulate(HeatingLib.System, stopTime=86400, numberOfIntervals=864, outputFormat=\"csv\", fileNamePrefix=\"base\");\ngetErrorString();\nsimulate(ProbeBigRoom, stopTime=86400, numberOfIntervals=864, outputFormat=\"csv\", fileNamePrefix=\"big\");\ngetErrorString();\nEOF\ntimeout 300 omc run.mos 2>&1 | tail -15; ls; for f in base_res.csv big_res.csv; do echo \"== $f\"; head -1 \"$f\" | tr ',' '\\n' | grep -n \"room.T\\|thermostat.Q\\|^\\\"time\\\"\" ; done",
 "description": "Simulate baseline and doubled-capacity probe in scratch dir"
}
```

### tool_result

```
record SimulationResult
    resultFile = "/tmp/arch-probe/big_res.csv",
    simulationOptions = "startTime = 0.0, stopTime = 86400.0, numberOfIntervals = 864, tolerance = 1e-6, method = 'dassl', fileNamePrefix = 'big', options = '', outputFormat = 'csv', variableFilter = '.*', cflags = '', simflags = ''",
    messages = "LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
",
    timeFrontend = 0.0018622080000000002,
    timeBackend = 0.0032155770000000003,
    timeSimCode = 0.001374107,
    timeTemplates = 0.002118921,
    timeCompile = 0.896242318,
    timeSimulation = 0.017106236,
    timeTotal = 0.921985843
end SimulationResult;
""
ProbeBigRoom.mo
base
base.c
base.libs
base.log
base.makefile
base.o
base_01exo.c
base_01exo.o
base_02nls.c
base_02nls.o
base_03lsy.c
base_03lsy.o
base_04set.c
base_04set.o
base_05evt.c
base_05evt.o
base_06inz.c
base_06inz.o
base_07dly.c
base_07dly.o
base_08bnd.c
base_08bnd.o
base_09alg.c
base_09alg.o
base_10asr.c
base_10asr.o
base_11mix.c
base_11mix.h
base_11mix.o
base_12jac.c
base_12jac.h
base_12jac.o
base_13opt.c
base_13opt.h
base_13opt.o
base_14lnz.c
base_14lnz.o
base_15syn.c
base_15syn.o
base_16dae.c
base_16dae.h
base_16dae.o
base_17inl.c
base_17inl.o
base_18spd.c
base_18spd.o
base_JacA.bin
base_external_functions.json
base_functions.c
base_functions.h
base_functions.o
base_includes.h
base_info.json
base_init.xml
base_literals.h
base_model.h
base_records.c
base_records.o
base_res.csv
big
big.c
big.libs
big.log
big.makefile
big.o
big_01exo.c
big_01exo.o
big_02nls.c
big_02nls.o
big_03lsy.c
big_03lsy.o
big_04set.c
big_04set.o
big_05evt.c
big_05evt.o
big_06inz.c
big_06inz.o
big_07dly.c
big_07dly.o
big_08bnd.c
big_08bnd.o
big_09alg.c
big_09alg.o
big_10asr.c
big_10asr.o
big_11mix.c
big_11mix.h
big_11mix.o
big_12jac.c
big_12jac.h
big_12jac.o
big_13opt.c
big_13opt.h
big_13opt.o
big_14lnz.c
big_14lnz.o
big_15syn.c
big_15syn.o
big_16dae.c
big_16dae.h
big_16dae.o
big_17inl.c
big_17inl.o
big_18spd.c
big_18spd.o
big_JacA.bin
big_external_functions.json
big_functions.c
big_functions.h
big_functions.o
big_includes.h
big_info.json
big_init.xml
big_literals.h
big_model.h
big_records.c
big_records.o
big_res.csv
lookup.mos
probe.mos
run.mos
== base_res.csv
1:"time"
2:"room.T"
3:"der(room.T)"
4:"thermostat.Q"
== big_res.csv
1:"time"
2:"room.T"
3:"der(room.T)"
4:"thermostat.Q"
Shell cwd was reset to /tmp/sa-eval-wd2gqb_e/project
```

### assistant

Both simulations ran. Next I'll extract the response: the time for the room to close 63% of its gap to the steady state, which is the closed-loop time constant. I'll compare that with the `tau` the Thermostat claims to implement.

### tool_use Bash

```json
{
 "command": "cd /tmp/arch-probe && for f in base big; do awk -F, -v name=\"$f\" 'NR==1{next} { t[NR]=$1; T[NR]=$2; n=NR } END {\n  T0=T[2]; Tss=T[n]; target=T0-(T0-Tss)*(1-1/exp(1));\n  tc=\"none\";\n  for(i=2;i<=n;i++){ if ((T0>Tss && T[i]<=target) || (T0<Tss && T[i]>=target)) { tc=t[i]; break } }\n  printf \"%s: T0=%.2f K  T_final=%.2f K  time to 63%% of gap = %s s  (thermostat.tau design = 1800 s)\\n\", name, T0, Tss, tc\n}' ${f}_res.csv; done; echo; awk -F, 'NR==1{next} NR==2{print \"t=0 Q=\" $4} ' base_res.csv; awk -F, 'NR>1 && ($1==1800||$1==3600){print \"base t=\"$1\" T=\"$2}' base_res.csv; awk -F, 'NR>1 && ($1==1800||$1==3600){print \"big  t=\"$1\" T=\"$2}' big_res.csv",
 "description": "Compute closed-loop time constants from both runs"
}
```

### tool_result

```
base: T0=288.15 K  T_final=286.14 K  time to 63% of gap = 1200 s  (thermostat.tau design = 1800 s)
big: T0=288.15 K  T_final=286.14 K  time to 63% of gap = 2400 s  (thermostat.tau design = 1800 s)

t=0 Q=1388.888888888889
base t=1800 T=286.5686127593881
base t=3600 T=286.2296082491034
big  t=1800 T=287.068842130837
big  t=3600 T=286.5683372664384
Shell cwd was reset to /tmp/sa-eval-wd2gqb_e/project
```

### assistant

Both runs confirm the coupling. Doubling `room.C` doubled the closed-loop time constant (1200 s → 2400 s) and the Thermostat was untouched. One more check: whether `checkModel` on that probe would still pass, since that decides whether the current test suite can catch this.

### tool_use Bash

```json
{
 "command": "cd /tmp/arch-probe && printf '%s\\n' 'loadFile(\"/tmp/sa-eval-wd2gqb_e/project/HeatingLib/package.mo\");' 'loadFile(\"/tmp/arch-probe/ProbeBigRoom.mo\");' 'checkModel(ProbeBigRoom); getErrorString();' > probe.mos && timeout 120 omc probe.mos 2>&1 | tail -4; cd /tmp/sa-eval-wd2gqb_e/project && git status --short && echo \"repo clean check done\"",
 "description": "Run checkModel on probe and confirm repo untouched"
}
```

### tool_result

```
"Check of ProbeBigRoom completed successfully.
Class ProbeBigRoom has 4 equation(s) and 4 variable(s).
2 of these are trivial equation(s)."
""
repo clean check done
```

### assistant

The mis-tuned variant passes `checkModel`, so the existing check cannot catch this. The repo is untouched. Now I'll write the report.

### tool_use Write

```json
{
 "file_path": "/tmp/architecture-review-20261121-210149.html",
 "content": "<!doctype html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"utf-8\" />\n    <title>Architecture review for HeatingLib</title>\n    <script src=\"https://cdn.tailwindcss.com\"></script>\n    <script type=\"module\">\n      import mermaid from \"https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs\";\n      mermaid.initialize({ startOnLoad: true, theme: \"neutral\", securityLevel: \"loose\" });\n    </script>\n    <style>\n      .seam { border-style: dashed; }\n      .leak { color: #dc2626; }\n      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); color: #f8fafc; }\n    </style>\n  </head>\n  <body class=\"bg-stone-50 text-slate-900 font-sans\">\n    <main class=\"max-w-5xl mx-auto px-6 py-12 space-y-12\">\n\n      <header class=\"space-y-4\">\n        <p class=\"text-xs uppercase tracking-wider text-slate-500\">Architecture review · 2026-11-21</p>\n        <h1 class=\"font-serif text-4xl\">HeatingLib</h1>\n        <div class=\"flex flex-wrap gap-4 text-xs text-slate-600\">\n          <span><span class=\"inline-block w-4 h-4 bg-white border border-slate-400 align-middle\"></span> module</span>\n          <span><span class=\"inline-block w-4 h-4 border-2 border-dashed border-slate-500 align-middle\"></span> seam</span>\n          <span><span class=\"inline-block w-4 h-1 bg-red-600 align-middle\"></span> leakage</span>\n          <span><span class=\"inline-block w-4 h-4 deep align-middle\"></span> deep module</span>\n        </div>\n        <p class=\"text-sm text-slate-600\">Scope: whole library. The repo has one commit, so there is no churn signal; every block was read. Baseline: <code class=\"font-mono\">omc tests/check.mos</code> passes.</p>\n      </header>\n\n      <section id=\"candidates\" class=\"space-y-10\">\n\n        <!-- Candidate A -->\n        <article id=\"a\" class=\"bg-white rounded-lg border border-slate-200 p-6 space-y-6\">\n          <div class=\"flex flex-wrap items-center gap-2\">\n            <span class=\"text-xs uppercase tracking-wider bg-emerald-100 text-emerald-800 rounded px-2 py-1\">Strong</span>\n            <span class=\"text-xs uppercase tracking-wider bg-slate-100 text-slate-700 rounded px-2 py-1\">in-process</span>\n          </div>\n          <h2 class=\"font-serif text-2xl\">Derive the controller gain from the room it controls</h2>\n          <ul class=\"font-mono text-sm text-slate-700 space-y-1\">\n            <li>HeatingLib/Thermostat.mo:11</li>\n            <li>HeatingLib/Room.mo:3</li>\n            <li>HeatingLib/package.mo:3</li>\n            <li>HeatingLib/System.mo:4-6</li>\n          </ul>\n\n          <div class=\"grid md:grid-cols-2 gap-4\">\n            <div class=\"rounded-lg border border-slate-200 bg-white p-4 space-y-2\">\n              <p class=\"text-xs uppercase tracking-wider text-slate-500\">Before</p>\n              <pre class=\"mermaid\">\nflowchart TB\n  P[\"package constant roomHeatCapacity\"]\n  R[\"Room: C defaults to constant\"]\n  H[\"Thermostat: k = constant / tau\"]\n  P -->|default| R\n  P -->|read directly| H\n  classDef leak stroke:#dc2626,stroke-width:2px;\n  class H leak\n              </pre>\n            </div>\n            <div class=\"rounded-lg border border-slate-200 bg-white p-4 space-y-2\">\n              <p class=\"text-xs uppercase tracking-wider text-slate-500\">After</p>\n              <pre class=\"mermaid\">\nflowchart TB\n  R[\"Room: owns C and G\"]\n  S[\"System: binds room values\"]\n  H[\"Thermostat: gain from C and G inputs\"]\n  R -->|C, G| S\n  S -->|binds C, G| H\n              </pre>\n            </div>\n          </div>\n\n          <div class=\"rounded-lg border border-slate-200 p-4 space-y-3\">\n            <p class=\"text-xs uppercase tracking-wider text-slate-500\">Measured closed-loop time constant (scratch models outside the repo)</p>\n            <div class=\"space-y-2 font-mono text-xs\">\n              <div class=\"flex items-center gap-3\"><span class=\"w-40\">Design tau</span><div class=\"h-4 bg-slate-300\" style=\"width:45%\"></div><span>1800 s</span></div>\n              <div class=\"flex items-center gap-3\"><span class=\"w-40\">Baseline model</span><div class=\"h-4 bg-emerald-600\" style=\"width:30%\"></div><span>1200 s</span></div>\n              <div class=\"flex items-center gap-3\"><span class=\"w-40\">room.C = 1e6, same Thermostat</span><div class=\"h-4 bg-red-600\" style=\"width:60%\"></div><span>2400 s</span></div>\n            </div>\n            <p class=\"text-xs text-slate-600\">Steady state settles at 286.14 K, 7.0 K below the 293.15 K set point. Both runs pass <code class=\"font-mono\">checkModel</code>.</p>\n          </div>\n\n          <div class=\"space-y-2\">\n            <p><span class=\"font-semibold\">Problem.</span> The Thermostat's interface does not say it needs the room's heat capacity. It reads the package constant instead, which is also the default for <code class=\"font-mono\">Room.C</code>. Overriding <code class=\"font-mono\">room.C</code> in a <code class=\"font-mono\">System</code> makes the loop respond twice as slowly, and nothing reports it. The gain uses only <code class=\"font-mono\">C</code>, but the loop's real time constant is C/(k+G), so the wall loss <code class=\"font-mono\">G</code> in Room also matters. The advertised <code class=\"font-mono\">tau = 1800 s</code> is therefore not met even at the default values.</p>\n            <p><span class=\"font-semibold\">Solution.</span> Give Thermostat the plant values it needs as inputs, bound by System (<code class=\"font-mono\">thermostat(C = room.C, G = room.G)</code>). Compute the gain from them. Then the package constant has no reader outside Room and can move into Room.</p>\n          </div>\n\n          <div>\n            <p class=\"text-xs uppercase tracking-wider text-slate-500 mb-2\">Wins</p>\n            <ul class=\"list-disc pl-5 text-sm space-y-1\">\n              <li>locality: plant values live with the room that owns them</li>\n              <li>locality: one gain formula, one place to change it</li>\n              <li>leverage: a two-zone room gets a correctly tuned controller</li>\n              <li>tests: Thermostat tested with explicit C and G</li>\n            </ul>\n          </div>\n\n          <div class=\"rounded border border-amber-300 bg-amber-50 p-3 text-sm\">\n            <span class=\"font-semibold\">Architecture note:</span> Thermostat currently reads a package constant, which arc42 §5 (\"may use: Interfaces\") does not allow. This fix restores that rule. System still does the wiring, so ADR-0001 is not touched. QS-2 currently passes with the wrong tuning, because its measure (\"0 changes to Thermostat.mo\") cannot see the coupling.\n          </div>\n        </article>\n\n        <!-- Candidate B -->\n        <article id=\"b\" class=\"bg-white rounded-lg border border-slate-200 p-6 space-y-6\">\n          <div class=\"flex flex-wrap items-center gap-2\">\n            <span class=\"text-xs uppercase tracking-wider bg-amber-100 text-amber-800 rounded px-2 py-1\">Worth exploring</span>\n            <span class=\"text-xs uppercase tracking-wider bg-slate-100 text-slate-700 rounded px-2 py-1\">ports &amp; adapters</span>\n          </div>\n          <h2 class=\"font-serif text-2xl\">Make the room a replaceable seam in System</h2>\n          <ul class=\"font-mono text-sm text-slate-700 space-y-1\">\n            <li>HeatingLib/System.mo:3-7</li>\n            <li>HeatingLib/Room.mo:7-8</li>\n            <li>HeatingLib/Interfaces.mo</li>\n          </ul>\n\n          <div class=\"grid md:grid-cols-2 gap-4\">\n            <div class=\"rounded-lg border border-slate-200 p-4 space-y-3\">\n              <p class=\"text-xs uppercase tracking-wider text-slate-500\">Before</p>\n              <div class=\"border-2 border-slate-700 rounded p-3 space-y-3\">\n                <p class=\"text-xs uppercase tracking-wider\">System</p>\n                <div class=\"grid grid-cols-2 gap-3\">\n                  <div class=\"border border-slate-500 rounded p-2 text-center text-sm\">Room <span class=\"block text-xs text-slate-500\">hard-coded type</span></div>\n                  <div class=\"border border-slate-500 rounded p-2 text-center text-sm\">Thermostat</div>\n                </div>\n                <p class=\"text-xs text-slate-600\">connect(room.T, thermostat.T) and connect(thermostat.Q, room.Q_heat): the seam is only the names.</p>\n              </div>\n            </div>\n            <div class=\"rounded-lg border border-slate-200 p-4 space-y-3\">\n              <p class=\"text-xs uppercase tracking-wider text-slate-500\">After</p>\n              <div class=\"border-2 border-slate-700 rounded p-3 space-y-3\">\n                <p class=\"text-xs uppercase tracking-wider\">System</p>\n                <div class=\"border-2 border-dashed border-slate-500 rounded p-2 text-center text-sm\">replaceable room</div>\n                <div class=\"text-center text-xs text-slate-500\">constrainedby RoomBase</div>\n                <div class=\"grid grid-cols-2 gap-3\">\n                  <div class=\"border border-slate-700 rounded p-2 text-center text-sm\">Room <span class=\"block text-xs text-slate-500\">adapter</span></div>\n                  <div class=\"border border-dashed border-slate-400 rounded p-2 text-center text-sm text-slate-500\">two-zone room <span class=\"block text-xs\">hypothetical</span></div>\n                </div>\n              </div>\n            </div>\n          </div>\n\n          <div class=\"space-y-2\">\n            <p><span class=\"font-semibold\">Problem.</span> System names <code class=\"font-mono\">Room</code> directly, and the seam is an implicit pair of connector names. A replacement room has no declared type to satisfy, so QS-2 relies on convention.</p>\n            <p><span class=\"font-semibold\">Solution.</span> Declare a partial base model with the <code class=\"font-mono\">T</code> and <code class=\"font-mono\">Q_heat</code> connectors, and make System's room <code class=\"font-mono\">replaceable ... constrainedby</code> it. The seam then has a type that a second variant must satisfy.</p>\n          </div>\n\n          <div>\n            <p class=\"text-xs uppercase tracking-wider text-slate-500 mb-2\">Wins</p>\n            <ul class=\"list-disc pl-5 text-sm space-y-1\">\n              <li>leverage: variants compared side by side (R-2)</li>\n              <li>locality: a room swap touches no other file</li>\n              <li>seam has a type; a bad replacement fails to check</li>\n            </ul>\n          </div>\n\n          <div class=\"rounded border border-amber-300 bg-amber-50 p-3 text-sm\">\n            <span class=\"font-semibold\">ADR callout:</span> the new base model sits in <code class=\"font-mono\">Interfaces</code>, which ADR-0001 lists as centrally decided. It needs the architect's acceptance before work starts. R-2 names several variants, so the seam is justified now, although there is only one adapter today.\n          </div>\n        </article>\n\n        <!-- Candidate C -->\n        <article id=\"c\" class=\"bg-white rounded-lg border border-slate-200 p-6 space-y-6\">\n          <div class=\"flex flex-wrap items-center gap-2\">\n            <span class=\"text-xs uppercase tracking-wider bg-amber-100 text-amber-800 rounded px-2 py-1\">Worth exploring</span>\n            <span class=\"text-xs uppercase tracking-wider bg-slate-100 text-slate-700 rounded px-2 py-1\">mock &amp; in-process</span>\n          </div>\n          <h2 class=\"font-serif text-2xl\">Give each block its own test surface</h2>\n          <ul class=\"font-mono text-sm text-slate-700 space-y-1\">\n            <li>tests/check.mos:2-3</li>\n          </ul>\n\n          <div class=\"grid md:grid-cols-2 gap-4\">\n            <div class=\"rounded-lg border border-slate-200 p-4 space-y-3\">\n              <p class=\"text-xs uppercase tracking-wider text-slate-500\">Before</p>\n              <div class=\"space-y-2\">\n                <div class=\"border-2 border-slate-700 rounded p-2 text-sm text-center bg-slate-100\">check: System only</div>\n                <div class=\"border border-slate-400 rounded p-2 text-sm text-center\">Room</div>\n                <div class=\"border border-slate-400 rounded p-2 text-sm text-center\">Thermostat</div>\n              </div>\n              <p class=\"text-xs text-slate-600\">Room and Thermostat have no entry point of their own. Only compile-checks, no simulation.</p>\n            </div>\n            <div class=\"rounded-lg border border-slate-200 p-4 space-y-3\">\n              <p class=\"text-xs uppercase tracking-wider text-slate-500\">After</p>\n              <div class=\"space-y-2\">\n                <div class=\"border border-slate-400 rounded p-2 text-sm text-center\">checkModel Room</div>\n                <div class=\"border border-slate-400 rounded p-2 text-sm text-center\">checkModel Thermostat</div>\n                <div class=\"border-2 border-slate-700 rounded p-2 text-sm text-center bg-slate-100\">simulate System: assert time constant</div>\n              </div>\n              <p class=\"text-xs text-slate-600\">Each block is checked on its own interface. The system simulation asserts the closed-loop response.</p>\n            </div>\n          </div>\n\n          <div class=\"space-y-2\">\n            <p><span class=\"font-semibold\">Problem.</span> The suite checks <code class=\"font-mono\">System</code> only. R-3 says models \"check and simulate\", but <code class=\"font-mono\">check.mos</code> never simulates, so the mis-tuned variant in Candidate A passes.</p>\n            <p><span class=\"font-semibold\">Solution.</span> Add per-block checks, plus one simulation assertion on the closed-loop response.</p>\n          </div>\n\n          <div>\n            <p class=\"text-xs uppercase tracking-wider text-slate-500 mb-2\">Wins</p>\n            <ul class=\"list-disc pl-5 text-sm space-y-1\">\n              <li>tests: each block tested through its own interface</li>\n              <li>locality: a regression is reported at the block that caused it</li>\n              <li>tests catch the tuning error in A</li>\n            </ul>\n          </div>\n        </article>\n\n        <!-- Considered, not proposed -->\n        <article class=\"bg-white rounded-lg border border-slate-200 p-6 space-y-3\">\n          <h2 class=\"font-serif text-xl\">Considered, not proposed</h2>\n          <ul class=\"list-disc pl-5 text-sm space-y-1 text-slate-700\">\n            <li><code class=\"font-mono\">Interfaces</code>: deletion test fails. Deleting it scatters the unit declarations across Room and Thermostat, so it earns its keep.</li>\n            <li><code class=\"font-mono\">System</code> has no parameters of its own. Modifiers reach through to the blocks (<code class=\"font-mono\">System(room(G = 200))</code>), which is adequate for now.</li>\n            <li>Hygiene: <code class=\"font-mono\">HeatingLib/package.order</code> lists <code class=\"font-mono\">roomHeatCapacity</code>, a constant rather than a file. Check whether OpenModelica ignores it.</li>\n            <li>Open question, not architecture: the Thermostat is proportional-only, so the room settles 7.0 K below the set point. The interface still promises to \"close the gap to the set point\".</li>\n          </ul>\n        </article>\n\n      </section>\n\n      <section id=\"top-recommendation\">\n        <article class=\"bg-white rounded-lg border-2 border-emerald-600 p-6 space-y-3\">\n          <p class=\"text-xs uppercase tracking-wider text-emerald-700\">Top recommendation</p>\n          <h2 class=\"font-serif text-2xl\"><a href=\"#a\" class=\"underline\">Derive the controller gain from the room it controls</a></h2>\n          <p class=\"text-sm\">It is the only candidate with a measured wrong behaviour: a 2× slower loop with no warning. It is a small change, it restores the arc42 may-use rule, and it does not touch any ADR. Candidate C then makes this class of error visible in the test suite.</p>\n        </article>\n      </section>\n\n    </main>\n  </body>\n</html>\n"
}
```

### tool_result

```
File created successfully at: /tmp/architecture-review-20261121-210149.html (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "f=/tmp/architecture-review-20261121-210149.html; ls -l \"$f\"; (command -v xdg-open >/dev/null && xdg-open \"$f\") || open \"$f\" 2>/dev/null || echo \"could not auto-open\"; echo \"$f\"",
 "description": "Open the report and print its absolute path"
}
```

### tool_result

```
-rw-r--r-- 1 root root 15576 Nov 21 21:02 /tmp/architecture-review-20261121-210149.html
could not auto-open
/tmp/architecture-review-20261121-210149.html
```

### assistant

The architecture report is ready: `/tmp/architecture-review-20261121-210149.html`. It couldn't be opened automatically here, so open that path in a browser.

HeatingLib is a small Modelica library (three blocks plus interfaces and a check script), and it has a single commit, so I read every file rather than sampling hot spots. I didn't spawn a sub-agent. Nothing in the repo was changed.

**Candidates**

- **A. Derive the controller gain from the room it controls — Strong.** `Thermostat` reads the package constant `roomHeatCapacity` directly, which arc42 §5 doesn't allow. I measured the effect with scratch models outside the repo. The loop's time constant is 1200 s at defaults, against the 1800 s that `tau` promises. Doubling `room.C` doubles it to 2400 s with the Thermostat unchanged, and that variant still passes `checkModel`. The fix is to have System bind `C` and `G` into the Thermostat, so the gain comes from the room it controls.
- **B. Make the room a replaceable seam in System — Worth exploring.** A partial base model in `Interfaces` would give the room seam a type. It touches the centrally decided `Interfaces` package under ADR-0001, so it needs the architect's acceptance first.
- **C. Give each block its own test surface — Worth exploring.** `check.mos` only checks `System` and never simulates. Per-block checks plus one simulation assertion would have caught the error in A.

**Top recommendation:** A. It's the only candidate with a measured wrong behaviour, and it's a small change.

**Not proposed:** `Interfaces` passes the deletion test, so it stays. The `package.order` entry for a constant and the 7 K steady-state offset from proportional-only control are noted in the report as hygiene and an open question.

No `GLOSSARY.md` exists, so I used the block names from arc42. I didn't create one; that happens in the grilling step if a term needs adding.

Which of these would you like to explore?

### result (success)

### user

I accept your top recommendation. Take it forward; I'm offline after this, so finish without
asking me again.

### assistant

I'll implement candidate A now. Before editing, I'll make one design call: the gain stays `C/tau`, so the default behaviour doesn't change. The report's `C/tau - G` formula would meet the advertised `tau`, but it also raises the steady-state offset, which is a tuning decision for you, not part of this refactor.

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/Thermostat.mo"
}
```

### tool_result

```
1	within HeatingLib;
2	block Thermostat "Proportional heating controller with a set point"
3	  parameter Interfaces.Temperature T_set = 293.15 "Set point";
4	  parameter Real tau(unit = "s") = 1800 "Time to close the gap to the set point";
5	  parameter Interfaces.HeatFlowRate Q_max = 3000 "Heater power limit";
6	  Interfaces.TemperatureInput T "Measured room temperature";
7	  Interfaces.HeatFlowOutput Q "Heating power demand";
8	protected
9	  // The gain needs the room's heat capacity, so it is read from the package constant
10	  // the room model uses as well.
11	  parameter Real k(unit = "W/K") = HeatingLib.roomHeatCapacity / tau "Controller gain";
12	equation
13	  Q = min(Q_max, max(0, k * (T_set - T)));
14	end Thermostat;
15	
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/Room.mo"
}
```

### tool_result

```
1	within HeatingLib;
2	model Room "Lumped room air: stores heat, loses it through the walls"
3	  parameter Real C(unit = "J/K") = HeatingLib.roomHeatCapacity "Heat capacity";
4	  parameter Real G(unit = "W/K") = 150 "Heat loss conductance of the walls";
5	  parameter Interfaces.Temperature T_amb = 273.15 "Outdoor temperature";
6	  parameter Interfaces.Temperature T_start = 288.15 "Initial room temperature";
7	  Interfaces.HeatFlowInput Q_heat "Heating power into the room";
8	  Interfaces.TemperatureOutput T "Room temperature";
9	initial equation
10	  T = T_start;
11	equation
12	  C * der(T) = Q_heat - G * (T - T_amb);
13	end Room;
14	
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/package.mo"
}
```

### tool_result

```
1	within ;
2	package HeatingLib "Room heating: a room, a thermostat and the system that connects them"
3	  constant Real roomHeatCapacity(unit = "J/K") = 5e5
4	    "Heat capacity of the room; read by Room and by Thermostat";
5	end HeatingLib;
6	
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/System.mo"
}
```

### tool_result

```
1	within HeatingLib;
2	model System "A room heated by a thermostat-controlled heater"
3	  Room room;
4	  Thermostat thermostat;
5	equation
6	  connect(room.T, thermostat.T);
7	  connect(thermostat.Q, room.Q_heat);
8	  annotation(experiment(StopTime = 86400));
9	end System;
10	
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/package.order"
}
```

### tool_result

```
1	roomHeatCapacity
2	Interfaces
3	Room
4	Thermostat
5	System
6	
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/Thermostat.mo",
 "old_string": "  parameter Interfaces.HeatFlowRate Q_max = 3000 \"Heater power limit\";\n  Interfaces.TemperatureInput T \"Measured room temperature\";\n  Interfaces.HeatFlowOutput Q \"Heating power demand\";\nprotected\n  // The gain needs the room's heat capacity, so it is read from the package constant\n  // the room model uses as well.\n  parameter Real k(unit = \"W/K\") = HeatingLib.roomHeatCapacity / tau \"Controller gain\";",
 "new_string": "  parameter Interfaces.HeatFlowRate Q_max = 3000 \"Heater power limit\";\n  parameter Real C(unit = \"J/K\") \"Heat capacity of the controlled room; bind to the room's C\";\n  Interfaces.TemperatureInput T \"Measured room temperature\";\n  Interfaces.HeatFlowOutput Q \"Heating power demand\";\nprotected\n  parameter Real k(unit = \"W/K\") = C / tau \"Controller gain\";"
}
```

### tool_result

```
The file /tmp/sa-eval-wd2gqb_e/project/HeatingLib/Thermostat.mo has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/Room.mo",
 "old_string": "  parameter Real C(unit = \"J/K\") = HeatingLib.roomHeatCapacity \"Heat capacity\";",
 "new_string": "  parameter Real C(unit = \"J/K\") = 5e5 \"Heat capacity\";"
}
```

### tool_result

```
The file /tmp/sa-eval-wd2gqb_e/project/HeatingLib/Room.mo has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/package.mo",
 "old_string": "package HeatingLib \"Room heating: a room, a thermostat and the system that connects them\"\n  constant Real roomHeatCapacity(unit = \"J/K\") = 5e5\n    \"Heat capacity of the room; read by Room and by Thermostat\";\nend HeatingLib;",
 "new_string": "package HeatingLib \"Room heating: a room, a thermostat and the system that connects them\"\nend HeatingLib;"
}
```

### tool_result

```
The file /tmp/sa-eval-wd2gqb_e/project/HeatingLib/package.mo has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/package.order",
 "old_string": "roomHeatCapacity\nInterfaces",
 "new_string": "Interfaces"
}
```

### tool_result

```
The file /tmp/sa-eval-wd2gqb_e/project/HeatingLib/package.order has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-wd2gqb_e/project/HeatingLib/System.mo",
 "old_string": "  Thermostat thermostat;",
 "new_string": "  Thermostat thermostat(C = room.C);"
}
```

### tool_result

```
The file /tmp/sa-eval-wd2gqb_e/project/HeatingLib/System.mo has been updated successfully. (file state is current in your context — no need to Read it back)
```

### assistant

Edits are in. Now I'll verify: the repo check, a fresh simulation compared with the baseline CSV from before the edit, and the doubled-capacity probe. The gain should now follow the room's `C`, so the controller's t=0 power should be 2778 W instead of 1389 W.

### tool_use Bash

```json
{
 "command": "timeout 120 omc tests/check.mos 2>&1 | tail -4; cd /tmp/arch-probe && cat > verify.mos <<'EOF'\nloadFile(\"/tmp/sa-eval-wd2gqb_e/project/HeatingLib/package.mo\");\nloadFile(\"/tmp/arch-probe/ProbeBigRoom.mo\");\ncheckModel(HeatingLib.Thermostat); getErrorString();\nsimulate(HeatingLib.System, stopTime=86400, numberOfIntervals=864, outputFormat=\"csv\", fileNamePrefix=\"new\");\ngetErrorString();\nsimulate(ProbeBigRoom, stopTime=86400, numberOfIntervals=864, outputFormat=\"csv\", fileNamePrefix=\"newbig\");\ngetErrorString();\nEOF\ntimeout 300 omc verify.mos 2>&1 | grep -iE \"error|warning|success|completed|Check of\" ; echo \"--- trajectory diff vs pre-change baseline (new_res.csv vs base_res.csv):\"; diff <(cut -d, -f1-4 base_res.csv) <(cut -d, -f1-4 new_res.csv) && echo \"IDENTICAL at default values\"; echo \"--- t=0 thermostat power, default vs room.C=1e6:\"; awk -F, 'NR==2{print \"default: Q=\" $4}' new_res.csv; awk -F, 'NR==2{print \"room.C=1e6: Q=\" $4}' newbig_res.csv; echo \"--- before change, big probe t=0 Q was 1388.9 W (fixed gain).\"",
 "description": "Verify check, default trajectory, and doubled-capacity probe"
}
```

### tool_result

```
"Check of HeatingLib.System completed successfully.
Class HeatingLib.System has 4 equation(s) and 4 variable(s).
2 of these are trivial equation(s)."
""
"Check of HeatingLib.Thermostat completed successfully.
    messages = "LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
    messages = "LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
--- trajectory diff vs pre-change baseline (new_res.csv vs base_res.csv):
IDENTICAL at default values
--- t=0 thermostat power, default vs room.C=1e6:
default: Q=1388.888888888889
room.C=1e6: Q=2777.777777777778
--- before change, big probe t=0 Q was 1388.9 W (fixed gain).
Shell cwd was reset to /tmp/sa-eval-wd2gqb_e/project
```

### assistant

Everything checks out. One last look at the working-tree diff.

### tool_use Bash

```json
{
 "command": "git status --short && git diff --stat",
 "description": "Show changed files in the working tree"
}
```

### tool_result

```
 M HeatingLib/Room.mo
 M HeatingLib/System.mo
 M HeatingLib/Thermostat.mo
 M HeatingLib/package.mo
 M HeatingLib/package.order
 HeatingLib/Room.mo       | 2 +-
 HeatingLib/System.mo     | 2 +-
 HeatingLib/Thermostat.mo | 5 ++---
 HeatingLib/package.mo    | 2 --
 HeatingLib/package.order | 1 -
 5 files changed, 4 insertions(+), 8 deletions(-)
```

### assistant

Candidate A is implemented in the working tree. The Thermostat now gets the room's heat capacity from System instead of reading a package constant. I haven't committed anything.

**What changed**
- `Thermostat.mo`: takes `C` as a required parameter with no default, and computes the gain as `k = C / tau`.
- `Room.mo`: owns the heat capacity directly (`C = 5e5`).
- `System.mo`: binds the controller to the room with `Thermostat thermostat(C = room.C)`.
- `package.mo` and `package.order`: the `roomHeatCapacity` constant is removed. Nothing else in the repo read it.

**Verification (OpenModelica)**
- `omc tests/check.mos` passes.
- A fresh 24 h simulation matches the pre-change baseline exactly, so default behaviour is unchanged.
- With `room.C = 1e6`, the controller's initial power is now 2778 W, up from 1389 W. The gain follows the room, which is the point of the change.

**Decisions I made for you**
- I kept the gain as `C/tau`, so default behaviour doesn't change. The report's `C/tau − G` formula would make the advertised 1800 s time constant true, but it also raises the steady-state offset from 7 K to about 11 K. That's a tuning decision, so I left it open.
- I removed the package constant rather than leaving it in place. This breaks any external code that reads `HeatingLib.roomHeatCapacity`.

**Not done**
- Candidates B (replaceable room seam, which needs your ADR acceptance) and C (per-block tests) are untouched.
- Nothing was committed or pushed.

### result (success)
