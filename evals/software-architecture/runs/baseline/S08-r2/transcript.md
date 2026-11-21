### user

/sa:improve-codebase-architecture Look for architecture improvements in HeatingLib. I'm not available for questions until you
have the report ready.

### assistant

I'll start by checking the repo layout, recent history, and any glossary or ADRs.

### tool_use Bash

```json
{
 "command": "git status --short | head -5; echo \"---LOG\"; git log --oneline | head -50; echo \"---FILES\"; git ls-files | head -300; echo \"---COUNT\"; git ls-files | wc -l; echo \"---GLOSS/ADR\"; ls GLOSSARY.md docs/adr 2>&1",
 "description": "Inspect repo state, history, and file list"
}
```

### tool_result

```
Exit code 2
---LOG
421e27c fixture
---FILES
HeatingLib/Interfaces.mo
HeatingLib/Room.mo
HeatingLib/System.mo
HeatingLib/Thermostat.mo
HeatingLib/package.mo
HeatingLib/package.order
README.md
docs/adr/0001-record-architecture-decisions.md
docs/architecture/arc42.md
tests/check.mos
---COUNT
10
---GLOSS/ADR
ls: cannot access 'GLOSSARY.md': No such file or directory
docs/adr:
0001-record-architecture-decisions.md
```

### assistant

The repo is small (10 tracked files, one commit), so I'll read the whole HeatingLib package directly.

### tool_use Bash

```json
{
 "command": "for f in HeatingLib/package.order HeatingLib/package.mo HeatingLib/Interfaces.mo HeatingLib/Room.mo HeatingLib/System.mo HeatingLib/Thermostat.mo tests/check.mos; do echo \"=================== $f\"; cat -n \"$f\"; done",
 "description": "Read all HeatingLib source and test files"
}
```

### tool_result

```
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
=================== tests/check.mos
     1	// Run from the project root: omc tests/check.mos
     2	loadFile("HeatingLib/package.mo"); getErrorString();
     3	checkModel(HeatingLib.System); getErrorString();
```

### tool_use Bash

```json
{
 "command": "cat -n README.md; echo \"=========ADR\"; cat -n docs/adr/0001-record-architecture-decisions.md; echo \"=========ARC42\"; cat -n docs/architecture/arc42.md",
 "description": "Read README, ADR, and architecture docs"
}
```

### tool_result

```
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
=========ADR
     1	# 1. Record architecture decisions
     2	
     3	## Status
     4	
     5	accepted 2026-10-01
     6	
     7	## Context
     8	
     9	The architect decides the architecture; modellers implement it. We need a line between
    10	decisions the architect makes centrally and decisions left to whoever builds a block (R-2,
    11	QG-2).
    12	
    13	## Decision
    14	
    15	We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.
    16	
    17	Decided centrally (needs an ADR the architect accepts):
    18	
    19	- the connector definitions in `Interfaces` and their units;
    20	- the dependency rule between blocks: `System` → `Room`, `Thermostat` → `Interfaces`; blocks
    21	  do not depend on each other;
    22	- library dependencies.
    23	
    24	Left to the building blocks (no ADR): equations inside a block, parameter defaults, test
    25	scripts.
    26	
    27	## Consequences
    28	
    29	Work that depends on a decision on the list waits until its ADR is accepted.
=========ARC42
     1	# HeatingLib: architecture
     2	
     3	Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.
     4	
     5	## 1. Introduction and goals
     6	
     7	### Requirements overview
     8	
     9	| ID | requirement | rank | status | reason |
    10	|---|---|---|---|---|
    11	| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | core use |
    12	| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | building variants are compared side by side |
    13	| R-3 | Every model checks and simulates in OpenModelica without errors. | 3 | active | results feed design decisions |
    14	
    15	### Quality goals
    16	
    17	| ID | goal (ISO/IEC 25010) | from | scenario |
    18	|---|---|---|---|
    19	| QG-1 | Maintainability: modifiability | R-1 | QS-1 |
    20	| QG-2 | Flexibility: replaceability | R-2 | QS-2 |
    21	| QG-3 | Reliability: faultlessness | R-3 | QS-3 |
    22	
    23	### Stakeholders
    24	
    25	| role | expectation |
    26	|---|---|
    27	| Architect (project owner) | decides the architecture; accepts ADRs |
    28	| Modellers | add a room or controller variant without learning the whole library |
    29	
    30	## 2. Constraints
    31	
    32	- OpenModelica 1.27 or later; no libraries beyond the Modelica language itself.
    33	
    34	## 3. Context and scope
    35	
    36	## 4. Solution strategy
    37	
    38	Blocks exchange signals only through the connectors in `Interfaces`; `System` wires them.
    39	
    40	## 5. Building block view
    41	
    42	| block | responsibility | may use |
    43	|---|---|---|
    44	| `Interfaces` | connectors and units shared by all blocks | - |
    45	| `Room` | heat balance of the room air | `Interfaces` |
    46	| `Thermostat` | heating power from the measured temperature | `Interfaces` |
    47	| `System` | instantiates and connects the blocks | `Room`, `Thermostat`, `Interfaces` |
    48	
    49	## 6. Runtime view
    50	
    51	## 7. Deployment view
    52	
    53	## 8. Crosscutting concepts
    54	
    55	- Units: SI, declared on every parameter and connector.
    56	
    57	## 9. Architecture decisions
    58	
    59	Decisions are recorded as ADRs in [docs/adr/](../adr/). What is decided centrally is listed in
    60	[ADR-0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md).
    61	
    62	## 10. Quality requirements
    63	
    64	| ID | goal | stimulus | environment | resp
[... 522 chars cut]
```

### assistant

I've read the whole library. Before writing the report, I'll check whether `omc` is available so I can confirm the failure scenario I suspect, and get a timestamp for the report filename.

### tool_use Bash

```json
{
 "command": "echo \"TMP=${TMPDIR:-/tmp}\"; date +%Y%m%d-%H%M%S; command -v omc && (omc tests/check.mos 2>&1 | tail -20) || echo \"omc not installed\"; command -v xdg-open open start 2>/dev/null",
 "description": "Check tmpdir, timestamp, and whether omc is installed"
}
```

### tool_result

```
TMP=/tmp
20261121-210132
/usr/bin/omc
true
""
"Check of HeatingLib.System completed successfully.
Class HeatingLib.System has 4 equation(s) and 4 variable(s).
2 of these are trivial equation(s)."
""
/usr/bin/open
```

### assistant

`omc` is installed. I'll test the suspected coupling directly: override the room's heat capacity in `System` and see whether the thermostat gain follows. The probe script goes outside the repo.

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/arch-probe && cd /tmp/sa-eval-8gveqzxd/project && cat > /tmp/arch-probe/probe.mos <<'EOF'\nloadFile(\"HeatingLib/package.mo\");\nloadFile(\"HeatingLib/Interfaces.mo\");\nloadFile(\"HeatingLib/Room.mo\");\nloadFile(\"HeatingLib/Thermostat.mo\");\nloadFile(\"HeatingLib/System.mo\");\ngetErrorString();\nsimulate(HeatingLib.System(room(C=1e6)), stopTime=86400, outputFormat=\"mat\");\ngetErrorString();\nprint(\"room.C      = \" + String(val(room.C, 0.0)) + \"\\n\");\nprint(\"thermostat.k= \" + String(val(thermostat.k, 0.0)) + \"\\n\");\nprint(\"room.C / tau = \" + String(val(room.C, 0.0) / 1800) + \"\\n\");\nEOF\ncd /tmp/arch-probe && omc probe.mos 2>&1 | tail -30",
 "description": "Probe thermostat gain when room capacity is overridden"
}
```

### tool_result

```
false
false
false
false
false
"Error: Failed to load file HeatingLib/package.mo: file does not exist.
Error: Failed to load file HeatingLib/Interfaces.mo: file does not exist.
Error: Failed to load file HeatingLib/Room.mo: file does not exist.
Error: Failed to load file HeatingLib/Thermostat.mo: file does not exist.
Error: Failed to load file HeatingLib/System.mo: file does not exist.
"

"[/tmp/arch-probe/probe.mos:7:1-7:77:writable] Error: Class simulate not found in scope <global scope> (looking for a function or record).
"
Shell cwd was reset to /tmp/sa-eval-8gveqzxd/project
```

### assistant

The probe ran from the wrong directory, so the relative paths failed. I'll run it from the project root.

### tool_use Bash

```json
{
 "command": "omc /tmp/arch-probe/probe.mos 2>&1 | tail -30; echo \"--- cleanup of any omc output in repo:\"; git status --short",
 "description": "Run gain probe from project root and check repo stays clean"
}
```

### tool_result

```
true
true
true
true
true
""

"[/tmp/arch-probe/probe.mos:7:1-7:77:writable] Error: Class simulate not found in scope <global scope> (looking for a function or record).
"



--- cleanup of any omc output in repo:
```

### assistant

The model loads now, but `simulate` isn't recognised. I'll check whether this `omc` build supports simulation at all before drawing conclusions.

### tool_use Bash

```json
{
 "command": "omc --version 2>&1 | head -3; printf 'loadFile(\"HeatingLib/package.mo\");\\nloadFile(\"HeatingLib/Interfaces.mo\");\\nloadFile(\"HeatingLib/Room.mo\");\\nloadFile(\"HeatingLib/Thermostat.mo\");\\nloadFile(\"HeatingLib/System.mo\");\\nlookupClass(\"HeatingLib.System\");\\ngetErrorString();\\n' > /tmp/arch-probe/lookup.mos; omc /tmp/arch-probe/lookup.mos 2>&1 | tail -5; ls -la /usr/bin/omc; file /usr/bin/omc 2>/dev/null | head -1",
 "description": "Check omc version and whether simulation is supported"
}
```

### tool_result

```
OpenModelica 1.27.2
true
true

"[/tmp/arch-probe/lookup.mos:6:1-6:33:writable] Error: Class lookupClass not found in scope <global scope> (looking for a function or record).
"
-rwxr-xr-x 1 root root 14496 Oct 30 11:31 /usr/bin/omc
/usr/bin/omc: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=29ab25a5265efa9aa9ee58623a90b669c93ddcde, for GNU/Linux 3.2.0, stripped
```

### assistant

The local `omc` is OpenModelica 1.27.2, but the binary is only 14 KB and can't run `simulate`, so I can't run the gain probe. I'll rely on reading the code for that finding and say so in the report. Now I'll write the report.

### tool_use Write

```json
{
 "file_path": "/tmp/architecture-review-20261121-210132.html",
 "content": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>HeatingLib architecture review</title>\n<script src=\"https://cdn.tailwindcss.com\"></script>\n<script src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js\"></script>\n<style>\n  .block-box { border: 2px solid #334155; border-radius: .5rem; padding: .6rem .8rem; background: #fff; font-size: .875rem; }\n  .block-bad { border-color: #dc2626; background: #fef2f2; }\n  .block-good { border-color: #16a34a; background: #f0fdf4; }\n  .arrow { color: #64748b; font-size: .8rem; text-align: center; }\n  .stub { border: 1px dashed #94a3b8; color: #475569; }\n</style>\n</head>\n<body class=\"bg-slate-50 text-slate-800 antialiased\">\n<main class=\"max-w-5xl mx-auto px-6 py-10 space-y-10\">\n\n  <header>\n    <p class=\"text-xs uppercase tracking-widest text-slate-500\">Architecture review</p>\n    <h1 class=\"text-3xl font-bold\">HeatingLib: deepening opportunities</h1>\n    <p class=\"mt-2 text-slate-600\">Scope: the whole library (6 Modelica files plus test script and docs). Git history has a single commit, so there is no change-frequency signal; the whole package was read directly.</p>\n    <p class=\"mt-2 text-sm text-slate-500\">Vocabulary: <em>module, interface, depth, seam, adapter, leverage, locality</em>. Domain names come from the code and from <code>docs/architecture/arc42.md</code>. There is no <code>GLOSSARY.md</code> in the repo.</p>\n  </header>\n\n  <section class=\"bg-white rounded-lg shadow-sm border border-slate-200 p-6\">\n    <h2 class=\"text-lg font-semibold mb-3\">Module map today</h2>\n    <div class=\"mermaid\">\ngraph LR\n  System[\"System (module)\"] --> Room[\"Room (module)\"]\n  System --> Thermostat[\"Thermostat (module)\"]\n  Room --> Interfaces[\"Interfaces (module)\"]\n  Thermostat --> Interfaces\n  Room -. \"reads roomHeatCapacity\" .-> Pkg[\"HeatingLib package constant\"]\n  Thermostat -. \"reads roomHeatCapacity\" .-> Pkg\n  classDef leak fill:#fef2f2,stroke:#dc2626;\n  class Pkg leak;\n    </div>\n    <p class=\"text-sm text-slate-600 mt-3\">Solid arrows are the dependency rule from ADR-0001 and arc42 §5. The dashed arrows are the leak that candidate 1 is about: two blocks read the same package-level constant, which is outside <code>Interfaces</code>.</p>\n  </section>\n\n  <!-- ============ CANDIDATE 1 ============ -->\n  <section class=\"bg-white rounded-lg shadow-sm border border-slate-200 p-6 space-y-5\">\n    <div class=\"flex items-start justify-between gap-4\">\n      <div>\n        <p class=\"text-xs text-slate-500\">Candidate 1</p>\n        <h2 class=\"text-xl font-semibold\">Stop the controller reading the room's physics from a package constant</h2>\n      </div>\n      <span class=\"shrink-0 rounded-full bg-green-100 text-green-800 px-3 py-1 text-sm font-semibold\">Strong</span>\n    </div>\n\n    <dl class=\"grid grid-cols-1 md:grid-cols-[8rem_1fr] gap-x-4 gap-y-3 text-sm\">\n      <dt class=\"font-semibold text-slate-600\">Files</dt>\n      <dd><code>HeatingLib/package.mo</code>, <code>HeatingLib/Room.mo</code> (<code>C</code>), <code>HeatingLib/Thermostat.mo</code> (<code>k</code>), <code>HeatingLib/System.mo</code></dd>\n\n      <dt class=\"font-semibold text-slate-600\">Problem</dt>\n      <dd>\n        <code>Thermostat.k = roomHeatCapacity / tau</code> is computed from a package constant, not from the room the controller is connected to.\n        <code>Room.C</code> defaults to the same constant, but it is a parameter, so it can be overridden. <code>System</code> does not pass the room's <code>C</code> to the thermostat.\n        A room built with <code>System(room(C = 1e6))</code> still gets a gain of 5e5/1800 ≈ 278 W/K, not 1e6/1800 ≈ 556 W/K. The controller is then tuned to the wrong time constant with no error or warning.\n        This also breaks QS-2: swapping in a two-zone room cannot leave <code>Thermostat</code> unchanged if the gain depends on the old room's capacity.\n      </dd>\n\n      <dt class=\"font-semibold text-slate-600\">Solution</dt>\n      <dd>\n        Make the controller take the capacity it needs through its own interface. Two options:\n        <ol class=\"list-decimal ml-5 mt-1 space-y-1\">\n          <li><strong>A (preferred):</strong> add a <code>parameter Real C</code> to <code>Thermostat</code> and have <code>System</code> bind it to the room: <code>Thermostat thermostat(C = room.C)</code>. Remove the package-level constant from both blocks.</li>\n          <li><strong>B:</strong> move the capacity constant into <code>Interfaces</code> so both blocks read it through the declared interface package. This is smaller, but it makes a physical default a central interface decision and needs an ADR (ADR-0001 says <code>Interfaces</code> is decided centrally).</li>\n        </ol>\n      </dd>\n\n      <dt class=\"font-semibold text-slate-600\">Benefits</dt>\n      <dd>\n        <strong>Locality:</strong> the room's capacity is set in one place, the room, and the controller sees its value at the seam. <strong>Leverage:</strong> any room variant that exposes <code>C</code> keeps the controller correct without edits to <code>Thermostat.mo</code>, which is the QS-2 scenario. <strong>Tests:</strong> the gain can be tested by setting <code>C</code> on the room and checking <code>k</code>, which the current design cannot express.\n      </dd>\n    </dl>\n\n    <div class=\"rounded-md border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900\">\n      <strong>ADR note:</strong> this does not contradict ADR-0001. ADR-0001 says that <code>Thermostat</code> depends only on <code>Interfaces</code>, and arc42 §5 says <code>Room</code> may use only <code>Interfaces</code>. The code breaks that rule through the package root. Fixing it complies with the ADR and does not need the ADR reopened.\n    </div>\n\n    <div>\n      <h3 class=\"text-sm font-semibold text-slate-600 mb-2\">Before / After</h3>\n      <div class=\"grid md:grid-cols-2 gap-6\">\n        <div>\n          <p class=\"text-xs uppercase tracking-wide text-red-700 mb-2\">Before: controller reads a shared constant</p>\n          <div class=\"space-y-2\">\n            <div class=\"block-box\">System</div>\n            <div class=\"arrow\">↓ wires room and controller, but not their capacity</div>\n            <div class=\"grid grid-cols-2 gap-3\">\n              <div class=\"block-box block-bad\">Room<br><span class=\"text-xs\">C = package constant (default)</span></div>\n              <div class=\"block-box block-bad\">Thermostat<br><span class=\"text-xs\">k = package constant / tau</span></div>\n            </div>\n            <div class=\"arrow\">↓ both read</div>\n            <div class=\"block-box block-bad\">HeatingLib.roomHeatCapacity (package root)</div>\n          </div>\n        </div>\n        <div>\n          <p class=\"text-xs uppercase tracking-wide text-green-700 mb-2\">After (option A): capacity flows through the seam</p>\n          <div class=\"space-y-2\">\n            <div class=\"block-box\">System</div>\n            <div class=\"arrow\">room.C → thermostat.C (binding in System)</div>\n            <div class=\"grid grid-cols-2 gap-3\">\n              <div class=\"block-box block-good\">Room<br><span class=\"text-xs\">C: owns the value</span></div>\n              <div class=\"block-box block-good\">Thermostat<br><span class=\"text-xs\">C: input parameter, k = C / tau</span></div>\n            </div>\n            <div class=\"arrow\">↓ both depend only on</div>\n            <div class=\"block-box block-good\">Interfaces</div>\n          </div>\n        </div>\n      </div>\n    </div>\n  </section>\n\n  <!-- ============ CANDIDATE 2 ============ -->\n  <section class=\"bg-white rounded-lg shadow-sm border border-slate-200 p-6 space-y-5\">\n    <div class=\"flex items-start justify-between gap-4\">\n      <div>\n        <p class=\"text-xs text-slate-500\">Candidate 2</p>\n        <h2 class=\"text-xl font-semibold\">Give <code>System</code> a seam for room and controller variants</h2>\n      </div>\n      <span class=\"shrink-0 rounded-full bg-amber-100 text-amber-800 px-3 py-1 text-sm font-semibold\">Worth exploring</span>\n    </div>\n\n    <dl class=\"grid grid-cols-1 md:grid-cols-[8rem_1fr] gap-x-4 gap-y-3 text-sm\">\n      <dt class=\"font-semibold text-slate-600\">Files</dt>\n      <dd><code>HeatingLib/System.mo</code>, <code>HeatingLib/Room.mo</code>, <code>HeatingLib/Thermostat.mo</code>, <code>HeatingLib/Interfaces.mo</code></dd>\n\n      <dt class=\"font-semibold text-slate-600\">Problem</dt>\n      <dd>\n        R-2 says a room or controller variant can be swapped \"without touching the rest\", and the two-zone room is named in QS-2. Today <code>System</code> declares <code>Room room;</code> and <code>Thermostat thermostat;</code>, so every swap means editing <code>System.mo</code>.\n        The connectors already form a seam, but the component choice is hard-wired, so there is no way to choose a variant from outside.\n        Only one adapter per role exists today, so this is a seam with one adapter. It is still justified because R-2 and QS-2 name the second variant.\n      </dd>\n\n      <dt class=\"font-semibold text-slate-600\">Solution</dt>\n      <dd>\n        Declare <code>partial</code> base classes for the room and the controller: they expose only the connectors (<code>T</code>, <code>Q_heat</code>, <code>Q</code>) and their parameters. Then declare <code>System</code>'s components as <code>replaceable Room room constrainedby RoomBase</code> and <code>replaceable Thermostat thermostat constrainedby ControllerBase</code>.\n        Depends on candidate 1: the base must not expose the room's capacity through a package constant.\n      </dd>\n\n      <dt class=\"font-semibold text-slate-600\">Benefits</dt>\n      <dd>\n        <strong>Leverage:</strong> a variant is a new class that extends the base; <code>System</code> does not change. <strong>Locality:</strong> the connector set in <code>Interfaces</code> becomes the one place where the contract is written. <strong>Tests:</strong> the partial bases become the test surface, so a stub room can test the controller in isolation.\n      </dd>\n    </dl>\n\n    <div class=\"rounded-md border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900\">\n      <strong>ADR note:</strong> the partial bases define the shape of the block contract, which is a central decision (ADR-0001: \"the connector definitions in <code>Interfaces</code>\"). Propose an ADR before adding the bases, so that the placement of <code>RoomBase</code> and <code>ControllerBase</code> is recorded.\n    </div>\n\n    <div>\n      <h3 class=\"text-sm font-semibold text-slate-600 mb-2\">Before / After</h3>\n      <div class=\"grid md:grid-cols-2 gap-6\">\n        <div>\n          <p class=\"text-xs uppercase tracking-wide text-red-700 mb-2\">Before: concrete components in System</p>\n          <div class=\"space-y-2\">\n            <div class=\"block-box block-bad\">System: <code>Room room;</code> <code>Thermostat thermostat;</code><br><span class=\"text-xs\">a variant means editing this file</span></div>\n            <div class=\"arrow\">↓ concrete types</div>\n            <div class=\"grid grid-cols-2 gap-3\">\n              <div class=\"block-box\">Room</div>\n              <div class=\"block-box\">Thermostat</div>\n            </div>\n            <div class=\"block-box stub text-xs\">TwoZoneRoom: would need its own System</div>\n          </div>\n        </div>\n        <div>\n          <p class=\"text-xs uppercase tracking-wide text-green-700 mb-2\">After: replaceable components with constrainedby</p>\n          <div class=\"space-y-2\">\n            <div class=\"block-box block-good\">System: <code>replaceable Room room constrainedby RoomBase</code><br><code>replaceable Thermostat thermostat constrainedby ControllerBase</code></div>\n            <div class=\"arrow\">↓ constrained by partial bases (connectors only)</div>\n            <div class=\"grid grid-cols-2 gap-3\">\n              <div class=\"block-box block-good\">RoomBase (partial)<br><span class=\"text-xs\">Room, TwoZoneRoom extend it</span></div>\n              <div class=\"block-box block-good\">ControllerBase (partial)<br><span class=\"text-xs\">Thermostat extends it</span></div>\n            </div>\n          </div>\n        </div>\n      </div>\n    </div>\n  </section>\n\n  <!-- ============ CANDIDATE 3 ============ -->\n  <section class=\"bg-white rounded-lg shadow-sm border border-slate-200 p-6 space-y-5\">\n    <div class=\"flex items-start justify-between gap-4\">\n      <div>\n        <p class=\"text-xs text-slate-500\">Candidate 3</p>\n        <h2 class=\"text-xl font-semibold\">Test behaviour, not just compilation</h2>\n      </div>\n      <span class=\"shrink-0 rounded-full bg-amber-100 text-amber-800 px-3 py-1 text-sm font-semibold\">Worth exploring</span>\n    </div>\n\n    <dl class=\"grid grid-cols-1 md:grid-cols-[8rem_1fr] gap-x-4 gap-y-3 text-sm\">\n      <dt class=\"font-semibold text-slate-600\">Files</dt>\n      <dd><code>tests/check.mos</code>, <code>HeatingLib/Room.mo</code> (heat balance), <code>HeatingLib/Thermostat.mo</code> (control law and saturation)</dd>\n\n      <dt class=\"font-semibold text-slate-600\">Problem</dt>\n      <dd>\n        <code>tests/check.mos</code> only runs <code>checkModel(HeatingLib.System)</code>. QS-3 measures \"0 errors\". Nothing checks that the room settles at <code>T_amb + Q/G</code>, that the controller saturates at <code>Q_max</code>, or that the room approaches <code>T_set</code>.\n        The physics lives in one equation each in <code>Room</code> and <code>Thermostat</code>, and their only observable behaviour is through a full simulation of <code>System</code>. So any regression in the equations passes the current check.\n      </dd>\n\n      <dt class=\"font-semibold text-slate-600\">Solution</dt>\n      <dd>\n        Add simulation test models next to the library (for example <code>HeatingLib.Test.RoomSteadyState</code>, <code>HeatingLib.Test.ThermostatSaturation</code>) with <code>assert</code> statements on the expected values, and run them from <code>tests/</code>. Test at the <code>System</code> seam unless candidate 2 gives isolated bases.\n      </dd>\n\n      <dt class=\"font-semibold text-slate-600\">Benefits</dt>\n      <dd>\n        <strong>Locality:</strong> a regression in the heat balance or the control law shows up at the block where it was made. <strong>Tests:</strong> expected values come from the design equations, so each test documents one rule. No ADR is needed: ADR-0001 leaves test scripts to the building blocks.\n      </dd>\n    </dl>\n\n    <div>\n      <h3 class=\"text-sm font-semibold text-slate-600 mb-2\">Before / After: what the check covers</h3>\n      <div class=\"grid md:grid-cols-2 gap-6\">\n        <div>\n          <p class=\"text-xs uppercase tracking-wide text-red-700 mb-2\">Before</p>\n          <div class=\"space-y-2 text-sm\">\n            <div class=\"flex items-center gap-3\"><span class=\"w-40\">Compiles</span><span class=\"h-4 rounded bg-slate-700\" style=\"width:100%\"></span></div>\n            <div class=\"flex items-center gap-3\"><span class=\"w-40\">Steady-state temperature</span><span class=\"h-4 rounded stub\" style=\"width:4%\"></span><span class=\"text-xs text-slate-500\">not tested</span></div>\n            <div class=\"flex items-center gap-3\"><span class=\"w-40\">Controller saturation</span><span class=\"h-4 rounded stub\" style=\"width:4%\"></span><span class=\"text-xs text-slate-500\">not tested</span></div>\n            <div class=\"flex items-center gap-3\"><span class=\"w-40\">Set-point approach</span><span class=\"h-4 rounded stub\" style=\"width:4%\"></span><span class=\"text-xs text-slate-500\">not tested</span></div>\n          </div>\n        </div>\n        <div>\n          <p class=\"text-xs uppercase tracking-wide text-green-700 mb-2\">After</p>\n          <div class=\"space-y-2 text-sm\">\n            <div class=\"flex items-center gap-3\"><span class=\"w-40\">Compiles</span><span class=\"h-4 rounded bg-slate-700\" style=\"width:100%\"></span></div>\n            <div class=\"flex items-center gap-3\"><span class=\"w-40\">Steady-state temperature</span><span class=\"h-4 rounded bg-green-600\" style=\"width:100%\"></span></div>\n            <div class=\"flex items-center gap-3\"><span class=\"w-40\">Controller saturation</span><span class=\"h-4 rounded bg-green-600\" style=\"width:100%\"></span></div>\n            <div class=\"flex items-center gap-3\"><span class=\"w-40\">Set-point approach</span><span class=\"h-4 rounded bg-green-600\" style=\"width:100%\"></span></div>\n          </div>\n        </div>\n      </div>\n    </div>\n  </section>\n\n  <!-- ============ CONSIDERED AND REJECTED ============ -->\n  <section class=\"bg-white rounded-lg shadow-sm border border-slate-200 p-6\">\n    <h2 class=\"text-lg font-semibold mb-3\">Considered and rejected</h2>\n    <ul class=\"list-disc ml-5 space-y-2 text-sm\">\n      <li><strong><code>Thermostat</code> as a shallow module:</strong> the deletion test fails. Deleting it would move the control law into <code>System</code>, which is a different place, not a simpler one. It has a narrow interface and holds the one rule it is responsible for.</li>\n      <li><strong><code>Interfaces</code>:</strong> it contains only declarations, but they are the shared contract and cannot be made deeper without changing what they declare. Candidate 1 option B would add a constant to it; that is a choice, not a defect.</li>\n      <li><strong><code>Room</code>:</strong> one equation with four parameters. The heat balance is the whole module, so there is no friction to remove.</li>\n    </ul>\n  </section>\n\n  <!-- ============ TOP RECOMMENDATION ============ -->\n  <section class=\"bg-slate-900 text-slate-100 rounded-lg p-6\">\n    <h2 class=\"text-lg font-semibold mb-2\">Top recommendation</h2>\n    <p class=\"text-sm leading-relaxed\">Start with <strong>candidate 1</strong>. It is the only one that is a correctness hazard today: a room with a different capacity silently gets a controller tuned to the default. The change is small (one parameter, one binding in <code>System</code>, two lines removed), it complies with the ADR-0001 dependency rule that the code already breaks, and it is a prerequisite for candidate 2, whose partial bases must not carry the package constant. Candidate 3 should follow, because it would catch a regression from candidate 1.</p>\n  </section>\n\n  <section class=\"text-xs text-slate-500 space-y-1\">\n    <p><strong>Verification limits.</strong> <code>omc</code> 1.27.2 is installed, and <code>tests/check.mos</code> reported success. A probe that overrides <code>room(C = 1e6)</code> and simulates could not run: the local <code>omc</code> reported <code>simulate</code> as not found. The coupling in candidate 1 comes from reading the code (<code>Thermostat.k</code> is computed only from the package constant, and <code>System</code> passes nothing to it), not from a simulation result.</p>\n    <p><strong>Not done.</strong> No sub-agents were used; the library is six files, read directly. No ADR was written, and no GLOSSARY.md was created. Those decisions are for the user.</p>\n  </section>\n\n</main>\n<script>\n  mermaid.initialize({ startOnLoad: true, theme: \"default\", flowchart: { htmlLabels: true } });\n</script>\n</body>\n</html>\n"
}
```

### tool_result

```
File created successfully at: /tmp/architecture-review-20261121-210132.html (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "open /tmp/architecture-review-20261121-210132.html 2>&1 || xdg-open /tmp/architecture-review-20261121-210132.html 2>&1; ls -la /tmp/architecture-review-20261121-210132.html; cd /tmp/sa-eval-8gveqzxd/project && git status --short && echo \"repo clean\"",
 "description": "Open the report and confirm the repo is unchanged"
}
```

### tool_result

```
/usr/bin/sensible-browser: 1: eval: www-browser: not found
Couldn't find a suitable web browser!
Set the $BROWSER environment variable to your desired browser.
Warning: program returned non-zero exit code #256
/bin/bash: line 1: xdg-open: command not found
-rw-r--r-- 1 root root 19031 Nov 21 21:02 /tmp/architecture-review-20261121-210132.html
repo clean
```

### assistant

The architecture report is ready: `/tmp/architecture-review-20261121-210132.html`

I couldn't open it because this machine has no browser. Open it directly in a browser. It loads Tailwind and Mermaid from CDNs, so it needs internet access.

I read the whole library, which is six Modelica files. The git history has one commit, so there was no change-frequency signal to narrow the scope. The repo is unchanged.

**Candidates**

1. **Strong: the controller reads the room's physics from a package constant.** `Thermostat.k` is computed from `HeatingLib.roomHeatCapacity`, and `Room.C` defaults to the same constant. `System` passes nothing between them. Overriding `room(C = 1e6)` leaves the controller gain at about 278 W/K instead of about 556 W/K, with no warning. This also undermines QS-2, the two-zone room swap. The fix is to pass the room's capacity to the thermostat through its interface. The code already breaks the ADR-0001 dependency rule here, so fixing it doesn't require reopening the ADR.
2. **Worth exploring: `System` hard-wires concrete `Room` and `Thermostat`.** Swapping a variant means editing `System.mo`, which conflicts with R-2. The proposal is `partial` base classes with `replaceable` components. There is only one adapter per role today, but R-2 and QS-2 name the second variant. This would need an ADR first, because the base classes shape the central connector contract.
3. **Worth exploring: the test checks only compilation.** `tests/check.mos` runs `checkModel`. Nothing verifies steady state, saturation, or set-point approach. The proposal is simulation test models with assertions.

I also considered and rejected `Thermostat` as a shallow module. The deletion test would only move the control law into `System`, so it is not shallow. `Room` and `Interfaces` have no friction worth removing.

**Top recommendation:** candidate 1. It is the only current correctness hazard, the change is small, and candidate 2 depends on it.

**Verification limits:** the `omc` binary on this machine is 14 KB and reports `simulate` as not found. I could not run the override probe. The candidate 1 finding comes from reading the code, not from a simulation.

Which of these would you like to explore?

### result (success)

### user

I accept your top recommendation. Take it forward; I'm offline after this, so finish without
asking me again.

### assistant

I'll implement candidate 1 (option A) and verify it with `omc` where the local binary allows. First I'll re-read the three files I'm editing.

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-8gveqzxd/project/HeatingLib/Thermostat.mo"
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
 "file_path": "/tmp/sa-eval-8gveqzxd/project/HeatingLib/Room.mo"
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
 "file_path": "/tmp/sa-eval-8gveqzxd/project/HeatingLib/System.mo"
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
 "file_path": "/tmp/sa-eval-8gveqzxd/project/HeatingLib/package.mo"
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

### assistant

The current code matches the report: the controller reads the package constant, and `System` wires nothing between room and controller. I'll make the change. `Room` owns its capacity default, the thermostat takes `C` as a required parameter, and `System` binds it from the room. The package constant goes away because nothing else uses it.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-8gveqzxd/project/HeatingLib/Thermostat.mo",
 "old_string": "  parameter Real tau(unit = \"s\") = 1800 \"Time to close the gap to the set point\";\n  parameter Interfaces.HeatFlowRate Q_max = 3000 \"Heater power limit\";\n  Interfaces.TemperatureInput T \"Measured room temperature\";\n  Interfaces.HeatFlowOutput Q \"Heating power demand\";\nprotected\n  // The gain needs the room's heat capacity, so it is read from the package constant\n  // the room model uses as well.\n  parameter Real k(unit = \"W/K\") = HeatingLib.roomHeatCapacity / tau \"Controller gain\";",
 "new_string": "  parameter Real tau(unit = \"s\") = 1800 \"Time to close the gap to the set point\";\n  parameter Real C(unit = \"J/K\") \"Heat capacity of the controlled room; bind to the room's C\";\n  parameter Interfaces.HeatFlowRate Q_max = 3000 \"Heater power limit\";\n  Interfaces.TemperatureInput T \"Measured room temperature\";\n  Interfaces.HeatFlowOutput Q \"Heating power demand\";\nprotected\n  parameter Real k(unit = \"W/K\") = C / tau \"Controller gain\";"
}
```

### tool_result

```
The file /tmp/sa-eval-8gveqzxd/project/HeatingLib/Thermostat.mo has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-8gveqzxd/project/HeatingLib/Room.mo",
 "old_string": "  parameter Real C(unit = \"J/K\") = HeatingLib.roomHeatCapacity \"Heat capacity\";",
 "new_string": "  parameter Real C(unit = \"J/K\") = 5e5 \"Heat capacity\";"
}
```

### tool_result

```
The file /tmp/sa-eval-8gveqzxd/project/HeatingLib/Room.mo has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-8gveqzxd/project/HeatingLib/System.mo",
 "old_string": "  Thermostat thermostat;",
 "new_string": "  Thermostat thermostat(C = room.C);"
}
```

### tool_result

```
The file /tmp/sa-eval-8gveqzxd/project/HeatingLib/System.mo has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-8gveqzxd/project/HeatingLib/package.mo",
 "old_string": "package HeatingLib \"Room heating: a room, a thermostat and the system that connects them\"\n  constant Real roomHeatCapacity(unit = \"J/K\") = 5e5\n    \"Heat capacity of the room; read by Room and by Thermostat\";\nend HeatingLib;",
 "new_string": "package HeatingLib \"Room heating: a room, a thermostat and the system that connects them\"\nend HeatingLib;"
}
```

### tool_result

```
The file /tmp/sa-eval-8gveqzxd/project/HeatingLib/package.mo has been updated successfully. (file state is current in your context — no need to Read it back)
```

### assistant

Now I'll verify. The repo's own check runs first, then a probe that prints the flattened gain for the default room and for an overridden room.

### tool_use Bash

```json
{
 "command": "echo \"== repo check\"; omc tests/check.mos 2>&1 | tail -8; echo \"== gain probe\"; cat > /tmp/arch-probe/gain.mos <<'EOF'\nloadFile(\"HeatingLib/package.mo\");\nloadFile(\"HeatingLib/Interfaces.mo\");\nloadFile(\"HeatingLib/Room.mo\");\nloadFile(\"HeatingLib/Thermostat.mo\");\nloadFile(\"HeatingLib/System.mo\");\nprint(instantiateModel(HeatingLib.System));\nprint(instantiateModel(HeatingLib.System(room(C=1e6))));\ngetErrorString();\nEOF\nomc /tmp/arch-probe/gain.mos 2>&1 | grep -E \"k =|C =|room|Error|error\" | head -30; echo \"== repo status\"; git status --short",
 "description": "Run repo check and gain probe on the modified library"
}
```

### tool_result

```
== repo check
true
"[/tmp/sa-eval-8gveqzxd/project/HeatingLib/package.mo:2:1-3:15:writable] Warning: roomHeatCapacity was referenced in the package.order file, but was not found in package.mo, roomHeatCapacity/package.mo or roomHeatCapacity.mo.
"
"Check of HeatingLib.System completed successfully.
Class HeatingLib.System has 4 equation(s) and 4 variable(s).
2 of these are trivial equation(s)."
""
== gain probe
class HeatingLib.System "A room heated by a thermostat-controlled heater"
  parameter Real room.C(unit = "J/K") = 5e5 "Heat capacity";
  parameter Real room.G(unit = "W/K") = 150.0 "Heat loss conductance of the walls";
  parameter Real room.T_amb(quantity = "ThermodynamicTemperature", unit = "K", displayUnit = "degC", min = 0.0) = 273.15 "Outdoor temperature";
  parameter Real room.T_start(quantity = "ThermodynamicTemperature", unit = "K", displayUnit = "degC", min = 0.0) = 288.15 "Initial room temperature";
  Real room.Q_heat(quantity = "Power", unit = "W") "Heating power into the room";
  Real room.T(quantity = "ThermodynamicTemperature", unit = "K", displayUnit = "degC", min = 0.0) "Room temperature";
  parameter Real thermostat.C(unit = "J/K") = room.C "Heat capacity of the controlled room; bind to the room's C";
  Real thermostat.T(quantity = "ThermodynamicTemperature", unit = "K", displayUnit = "degC", min = 0.0) "Measured room temperature";
  room.T = room.T_start;
  room.T = thermostat.T;
  thermostat.Q = room.Q_heat;
  room.C * der(room.T) = room.Q_heat - room.G * (room.T - room.T_amb);
"[/tmp/sa-eval-8gveqzxd/project/HeatingLib/package.mo:2:1-3:15:writable] Warning: roomHeatCapacity was referenced in the package.order file, but was not found in package.mo, roomHeatCapacity/package.mo or roomHeatCapacity.mo.
[/tmp/arch-probe/gain.mos:7:1-7:56:writable] Error: Class instantiateModel not found in scope <global scope> (looking for a function or record).
== repo status
 M HeatingLib/Room.mo
 M HeatingLib/System.mo
 M HeatingLib/Thermostat.mo
 M HeatingLib/package.mo
```

### assistant

The flattened output shows `thermostat.C = room.C`, and the repo check still passes. The warning is left over from the removed constant: `package.order` still lists `roomHeatCapacity`. I'll remove that line and recheck.

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-8gveqzxd/project/HeatingLib/package.order",
 "old_string": "roomHeatCapacity\nInterfaces",
 "new_string": "Interfaces"
}
```

### tool_result

```
The file /tmp/sa-eval-8gveqzxd/project/HeatingLib/package.order has been updated successfully.
```

### tool_use Bash

```json
{
 "command": "omc tests/check.mos 2>&1; echo \"== grep leftovers\"; grep -rn \"roomHeatCapacity\" . --exclude-dir=.git || echo \"none\"; echo \"== diff\"; git diff --stat",
 "description": "Recheck library after removing stale package.order entry"
}
```

### tool_result

```
true
""
"Check of HeatingLib.System completed successfully.
Class HeatingLib.System has 4 equation(s) and 4 variable(s).
2 of these are trivial equation(s)."
""
== grep leftovers
none
== diff
 HeatingLib/Room.mo       | 2 +-
 HeatingLib/System.mo     | 2 +-
 HeatingLib/Thermostat.mo | 5 ++---
 HeatingLib/package.mo    | 2 --
 HeatingLib/package.order | 1 -
 5 files changed, 4 insertions(+), 8 deletions(-)
```

### assistant

I implemented candidate 1 (option A) in the working tree. I did not commit it.

**Changes**
- `Thermostat.mo`: the gain now comes from a required `C` parameter, `k = C / tau`. The package-constant read is gone.
- `System.mo`: `Thermostat thermostat(C = room.C);` binds the controller to the room's capacity.
- `Room.mo`: `C` defaults to `5e5` directly, so the room owns its value.
- `package.mo`: the `roomHeatCapacity` constant is removed. Nothing else used it.
- `package.order`: removed the stale `roomHeatCapacity` entry, which otherwise triggered an `omc` warning.

**Verification**
- `omc tests/check.mos` passes with no warnings.
- Instantiating `System` shows `thermostat.C = room.C`, so the controller gain follows the room's capacity.
- No `roomHeatCapacity` references remain in the repo.

**Not verified:** the override case, `System(room(C = 1e6))`. The local `omc` can't run `instantiateModel` or `simulate`. The binding is by reference, so the gain should follow the override, but I couldn't confirm it by running it.

**Choices I made**
- Option A over option B, so no constant goes into `Interfaces` and no new ADR is needed.
- `Thermostat.C` has no default. Standalone use must bind it, which makes the dependency explicit.
- The package constant is deleted rather than kept as an alias.

Candidates 2 and 3 are untouched. The change is uncommitted, so you can review the diff with `git diff` before committing.

### result (success)
