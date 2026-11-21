### user

/sa:setup-architecture Set up the architecture documentation for HeatingLib. There is none yet: the code is all we
have. My requirements:
1. Simulate a heated room over a day and show its temperature.
2. Swap the room or the controller for another variant without touching the rest.
3. Every model checks in OpenModelica without errors.

### assistant

I'll start by reading the project and the skill references the setup depends on.

### tool_use Bash

```json
{
 "command": "git status --short && git log --oneline | head && find . -path ./.git -prune -o -type f -print | head -200",
 "description": "Inspect repo state and file layout"
}
```

### tool_result

```
fd442ef fixture
./README.md
./HeatingLib/package.order
./HeatingLib/System.mo
./HeatingLib/Thermostat.mo
./HeatingLib/Interfaces.mo
./HeatingLib/Room.mo
./HeatingLib/package.mo
./tests/check.mos
```

### tool_use Skill

```json
{
 "skill": "sa:quality-requirements"
}
```

### tool_result

```
Launching skill: sa:quality-requirements
```

### tool_use Skill

```json
{
 "skill": "sa:domain-modeling"
}
```

### tool_result

```
Launching skill: sa:domain-modeling
```

### tool_use Skill

```json
{
 "skill": "sa:add-requirements"
}
```

### tool_result

```
Launching skill: sa:add-requirements
```

### tool_use Bash

```json
{
 "command": "for f in README.md HeatingLib/package.order HeatingLib/package.mo HeatingLib/System.mo HeatingLib/Room.mo HeatingLib/Thermostat.mo HeatingLib/Interfaces.mo tests/check.mos; do echo \"=== $f\"; cat \"$f\"; echo; done",
 "description": "Read README, package files and all Modelica sources"
}
```

### tool_result

```
=== README.md
# HeatingLib

A Modelica library that simulates a heated room over a day.

Check the library with OpenModelica:

```sh
omc tests/check.mos
```

=== HeatingLib/package.order
roomHeatCapacity
Interfaces
Room
Thermostat
System

=== HeatingLib/package.mo
within ;
package HeatingLib "Room heating: a room, a thermostat and the system that connects them"
  constant Real roomHeatCapacity(unit = "J/K") = 5e5
    "Heat capacity of the room; read by Room and by Thermostat";
end HeatingLib;

=== HeatingLib/System.mo
within HeatingLib;
model System "A room heated by a thermostat-controlled heater"
  Room room;
  Thermostat thermostat;
equation
  connect(room.T, thermostat.T);
  connect(thermostat.Q, room.Q_heat);
  annotation(experiment(StopTime = 86400));
end System;

=== HeatingLib/Room.mo
within HeatingLib;
model Room "Lumped room air: stores heat, loses it through the walls"
  parameter Real C(unit = "J/K") = HeatingLib.roomHeatCapacity "Heat capacity";
  parameter Real G(unit = "W/K") = 150 "Heat loss conductance of the walls";
  parameter Interfaces.Temperature T_amb = 273.15 "Outdoor temperature";
  parameter Interfaces.Temperature T_start = 288.15 "Initial room temperature";
  Interfaces.HeatFlowInput Q_heat "Heating power into the room";
  Interfaces.TemperatureOutput T "Room temperature";
initial equation
  T = T_start;
equation
  C * der(T) = Q_heat - G * (T - T_amb);
end Room;

=== HeatingLib/Thermostat.mo
within HeatingLib;
block Thermostat "Proportional heating controller with a set point"
  parameter Interfaces.Temperature T_set = 293.15 "Set point";
  parameter Real tau(unit = "s") = 1800 "Time to close the gap to the set point";
  parameter Interfaces.HeatFlowRate Q_max = 3000 "Heater power limit";
  Interfaces.TemperatureInput T "Measured room temperature";
  Interfaces.HeatFlowOutput Q "Heating power demand";
protected
  // The gain needs the room's heat capacity, so it is read from the package constant
  // the room model uses as well.
  parameter Real k(unit = "W/K") = HeatingLib.roomHeatCapacity / tau "Controller gain";
equation
  Q = min(Q_max, max(0, k * (T_set - T)));
end Thermostat;

=== HeatingLib/Interfaces.mo
within HeatingLib;
package Interfaces "Connectors and units shared by all blocks"
  type Temperature = Real(final quantity = "ThermodynamicTemperature", final unit = "K",
    min = 0, displayUnit = "degC");
  type HeatFlowRate = Real(final quantity = "Power", final unit = "W");
  connector TemperatureInput = input Temperature "Temperature signal into a block";
  connector TemperatureOutput = output Temperature "Temperature signal out of a block";
  connector HeatFlowInput = input HeatFlowRate "Heating power signal into a block";
  connector HeatFlowOutput = output HeatFlowRate "Heating power signal out of a block";
end Interfaces;

=== tests/check.mos
// Run from the project root: omc tests/check.mos
loadFile("HeatingLib/package.mo"); getErrorString();
checkModel(HeatingLib.System); getErrorString();
```

### tool_use Bash

```json
{
 "command": "ls -la /tmp/sa-arm-_d6ir7gx/sa/skills/setup-architecture/references/ 2>/dev/null; ls /tmp/sa-arm-_d6ir7gx/sa/skills/quality-requirements/references/ /tmp/sa-arm-_d6ir7gx/sa/skills/domain-modeling/ 2>/dev/null; which omc omc.exe 2>/dev/null; echo \"omc: $?\"",
 "description": "List skill reference files and check for OpenModelica"
}
```

### tool_result

```
total 20
drwxrwxr-x 2 root root 4096 Nov 21 22:42 .
drwxrwxr-x 3 root root 4096 Nov 21 22:42 ..
-rw-rw-r-- 1 root root 2983 Nov 21 22:42 arc42-skeleton.md
-rw-rw-r-- 1 root root 1652 Nov 21 22:42 made-centrally-adr.md
-rw-rw-r-- 1 root root 3359 Nov 21 22:42 recovery.md
/tmp/sa-arm-_d6ir7gx/sa/skills/domain-modeling/:
ADR-FORMAT.md
GLOSSARY-FORMAT.md
SKILL.md
agents

/tmp/sa-arm-_d6ir7gx/sa/skills/quality-requirements/references/:
iso-25010.md
quality-scenario.md
/usr/bin/omc
omc: 1
```

### assistant

The project has source and a README that only covers the product and how to run it, so this is the undocumented case. Next I'll read the setup references and run the existing check to see the baseline.

### tool_use Bash

```json
{
 "command": "cd /tmp/sa-arm-_d6ir7gx/sa/skills && cat setup-architecture/references/arc42-skeleton.md; echo ======; cat setup-architecture/references/made-centrally-adr.md; echo ======; cat setup-architecture/references/recovery.md; echo ======; cat quality-requirements/references/quality-scenario.md; echo =====; cat quality-requirements/references/iso-25010.md; echo =====; cat domain-modeling/ADR-FORMAT.md",
 "description": "Read setup-architecture and quality references"
}
```

### tool_result

```
# arc42 skeleton

Write `docs/architecture/arc42.md` with these twelve sections, in this order, each as a level-2
heading `## <n>. <name>`. The section names and one-line purposes are our own wording of the
arc42 template; for its full explanations and examples see [arc42.org](https://arc42.org) and
[docs.arc42.org](https://docs.arc42.org) (link, do not copy). Leave a section empty until there
is something to write: the document grows with the project.

```markdown
# <project>: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals
## 2. Constraints
## 3. Context and scope
## 4. Solution strategy
## 5. Building block view
## 6. Runtime view
## 7. Deployment view
## 8. Crosscutting concepts
## 9. Architecture decisions
## 10. Quality requirements
## 11. Risks and technical debt
## 12. Glossary
```

| section | holds |
|---|---|
| 1. Introduction and goals | `### Requirements overview` (the R-list), `### Quality goals`, `### Stakeholders`; tables as in `quality-requirements` › Where they live |
| 2. Constraints | what the architect cannot change: platforms, licences, mandated technology |
| 3. Context and scope | the system boundary and everything outside it the system talks to |
| 4. Solution strategy | the few fundamental ideas the solution rests on, each traced to a goal |
| 5. Building block view | the table `\| block \| responsibility \| may use \|`: the parts of the system, what each is responsible for, and which other blocks it may use |
| 6. Runtime view | how the parts work together in the scenarios that matter |
| 7. Deployment view | where it runs and how it gets there |
| 8. Crosscutting concepts | rules every part follows: naming, units, error handling, logging |
| 9. Architecture decisions | one sentence saying where the ADRs are, linked relative to this file (`../adr/` for `docs/adr/`), and a link to the "Record architecture decisions" ADR |
| 10. Quality requirements | the quality scenario table (`quality-requirements` › references/quality-scenario.md) |
| 11. Risks and technical debt | known risks and debt, each with what it threatens |
| 12. Glossary | a link to `GLOSSARY.md`; without one, the line "`GLOSSARY.md` is created with the first resolved term." |

## Existing documents

In a project that already documents its architecture, each section whose content lives in
another document (a README section, a wiki page, a design doc) gets one line linking it, such
as "See README › How it works", linked as `../../README.md#how-it-works`. That document stays where
and as it is; the arc42 file holds the link, never a copy of its content. A section whose
content lives nowhere yet starts empty, as in a fresh project.

## At setup

At setup, sections 1, 5 and 10 get their empty tables and sections 9 and 12 their links in the
first turn. Rows follow once the architect confirms; section 5's rows follow once building
blocks are decided.
======
# "Record architecture decisions" ADR

The ADR that draws the line between decisions the architect makes centrally and decisions left
to whoever builds a block. It takes the next free number in the project's ADR directory (0001 in a
fresh project); skills find it by its title, never by its number. Format and status rules: `domain-modeling`.

```markdown
# <n>. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. <One sentence on
what this product needs from that line, citing the R- and QG-IDs it serves, e.g. "Sightings
must survive crashes (R-2, QG-1) and work everywhere with only Python (R-3, QG-2)".>

## Decision

We record architecture decisions as ADRs in `<the project's ADR directory>`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- <items from the default list below, made concrete for this product>

Left to the building blocks (no ADR):

- <internal helpers, structure inside one bloc
[... 11128 chars cut]
```

### tool_use Bash

```json
{
 "command": "timeout 300 omc tests/check.mos 2>&1 | tail -30",
 "description": "Run existing OpenModelica check to get baseline"
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
```

### assistant

The baseline check passes for `System` only. `check.mos` never checks `Room` or `Thermostat` on their own, so requirement 3 is not yet covered by the existing check. I'll check each model and run the one-day simulation in a scratch directory so the repo stays clean.

### tool_use Bash

```json
{
 "command": "mkdir -p /tmp/sa-scratch-heat && cd /tmp/sa-scratch-heat && P=/tmp/sa-eval-yzarbn9i/project && cat > /tmp/sa-scratch-heat/verify.mos <<EOF\nloadFile(\"$P/HeatingLib/package.mo\"); getErrorString();\ncheckModel(HeatingLib.Interfaces.Temperature); getErrorString();\ncheckModel(HeatingLib.Room); getErrorString();\ncheckModel(HeatingLib.Thermostat); getErrorString();\ncheckModel(HeatingLib.System); getErrorString();\nsimulate(HeatingLib.System, stopTime=86400, numberOfIntervals=24); getErrorString();\nval(room.T, 0); val(room.T, 3600); val(room.T, 86400);\nEOF\ntimeout 600 omc verify.mos 2>&1 | tail -40; ls",
 "description": "Check each model and simulate one day in scratch dir"
}
```

### tool_result

```
true
""
"Check of HeatingLib.Interfaces.Temperature completed successfully.
Class HeatingLib.Interfaces.Temperature has 0 equation(s) and 0 variable(s).
0 of these are trivial equation(s)."
""
"Check of HeatingLib.Room completed successfully.
Class HeatingLib.Room has 2 equation(s) and 2 variable(s).
1 of these are trivial equation(s)."
""
"Check of HeatingLib.Thermostat completed successfully.
Class HeatingLib.Thermostat has 2 equation(s) and 2 variable(s).
1 of these are trivial equation(s)."
""
"Check of HeatingLib.System completed successfully.
Class HeatingLib.System has 4 equation(s) and 4 variable(s).
2 of these are trivial equation(s)."
""
record SimulationResult
    resultFile = "/tmp/sa-scratch-heat/HeatingLib.System_res.mat",
    simulationOptions = "startTime = 0.0, stopTime = 86400.0, numberOfIntervals = 24, tolerance = 1e-6, method = 'dassl', fileNamePrefix = 'HeatingLib.System', options = '', outputFormat = 'mat', variableFilter = '.*', cflags = '', simflags = ''",
    messages = "LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
",
    timeFrontend = 0.002154787,
    timeBackend = 0.004154195,
    timeSimCode = 0.0016055210000000002,
    timeTemplates = 0.002345532,
    timeCompile = 0.963037874,
    timeSimulation = 0.014482638,
    timeTotal = 0.987887185
end SimulationResult;
""
288.15
286.22960824910336
286.1370129885084
HeatingLib.System
HeatingLib.System.c
HeatingLib.System.libs
HeatingLib.System.log
HeatingLib.System.makefile
HeatingLib.System.o
HeatingLib.System_01exo.c
HeatingLib.System_01exo.o
HeatingLib.System_02nls.c
HeatingLib.System_02nls.o
HeatingLib.System_03lsy.c
HeatingLib.System_03lsy.o
HeatingLib.System_04set.c
HeatingLib.System_04set.o
HeatingLib.System_05evt.c
HeatingLib.System_05evt.o
HeatingLib.System_06inz.c
HeatingLib.System_06inz.o
HeatingLib.System_07dly.c
HeatingLib.System_07dly.o
HeatingLib.System_08bnd.c
HeatingLib.System_08bnd.o
HeatingLib.System_09alg.c
HeatingLib.System_09alg.o
HeatingLib.System_10asr.c
HeatingLib.System_10asr.o
HeatingLib.System_11mix.c
HeatingLib.System_11mix.h
HeatingLib.System_11mix.o
HeatingLib.System_12jac.c
HeatingLib.System_12jac.h
HeatingLib.System_12jac.o
HeatingLib.System_13opt.c
HeatingLib.System_13opt.h
HeatingLib.System_13opt.o
HeatingLib.System_14lnz.c
HeatingLib.System_14lnz.o
HeatingLib.System_15syn.c
HeatingLib.System_15syn.o
HeatingLib.System_16dae.c
HeatingLib.System_16dae.h
HeatingLib.System_16dae.o
HeatingLib.System_17inl.c
HeatingLib.System_17inl.o
HeatingLib.System_18spd.c
HeatingLib.System_18spd.o
HeatingLib.System_JacA.bin
HeatingLib.System_external_functions.json
HeatingLib.System_functions.c
HeatingLib.System_functions.h
HeatingLib.System_functions.o
HeatingLib.System_includes.h
HeatingLib.System_info.json
HeatingLib.System_init.xml
HeatingLib.System_literals.h
HeatingLib.System_model.h
HeatingLib.System_records.c
HeatingLib.System_records.o
HeatingLib.System_res.mat
verify.mos
Shell cwd was reset to /tmp/sa-eval-yzarbn9i/project
```

### assistant

The simulation runs and matches a closed-form check. Next I'll write the skeleton, the only file this first turn changes.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md",
 "content": "# HeatingLib: architecture\n\nStructured after the arc42 template (https://arc42.org). Empty sections are filled when needed.\n\n## 1. Introduction and goals\n\n### Requirements overview\n\n| ID | requirement | rank | status | reason |\n|---|---|---|---|---|\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n\n### Stakeholders\n\n## 2. Constraints\n\n## 3. Context and scope\n\n## 4. Solution strategy\n\n## 5. Building block view\n\n| block | responsibility | may use |\n|---|---|---|\n\n## 6. Runtime view\n\n## 7. Deployment view\n\n## 8. Crosscutting concepts\n\n## 9. Architecture decisions\n\nADRs live in `../adr/` (that is, `docs/adr/`); the directory does not exist yet. The \"Record architecture decisions\" ADR is proposed to the architect and not yet written.\n\n## 10. Quality requirements\n\n| ID | goal | stimulus | environment | response | measure |\n|---|---|---|---|---|---|\n\n## 11. Risks and technical debt\n\n## 12. Glossary\n\n`GLOSSARY.md` is created with the first resolved term.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "rm -rf /tmp/sa-scratch-heat && cd /tmp/sa-eval-yzarbn9i/project && git status --short",
 "description": "Remove scratch dir and confirm only arc42.md is new"
}
```

### tool_result

```
?? docs/
```

### assistant

The skeleton is written, and the repo now has one new file: `docs/architecture/arc42.md`. I did not write any R-list rows, goals, or ADRs yet. Those wait for your confirmation.

**Situation: undocumented.** The code is Modelica with no architecture documentation. The README covers the product and how to run the check, not how the system is built.

## Verified in the code (scratch runs, nothing added to the repo)

- `checkModel` passes for `Interfaces.Temperature`, `Room`, `Thermostat` and `System`. The existing `tests/check.mos` checks only `System`, so R-3 holds today but nothing enforces it for the other models.
- The one-day simulation (`StopTime = 86400`) finishes. The room starts at 288.15 K (15 °C), is at 286.23 K after 1 h, and at 286.14 K (≈13.0 °C) after 24 h.
- That 286.14 K is the closed-form steady state of the proportional controller: the set point is 293.15 K (20 °C), and the room settles 7 K below it. Heat demand there is about 1950 W, under the 3000 W limit, so this is the controller's offset, not the power cap.

## Findings for you, not fixed

- **Possible R-1 issue:** is the 7 K offset intended? A proportional-only controller with `tau = 1800 s` cannot reach the set point.
- **R-2 coupling:** `Room.C` and `Thermostat.k` both read `HeatingLib.roomHeatCapacity`. Swapping in a room with another heat capacity silently changes the controller gain, so a swap is not yet clean.
- **R-1 output:** `simulate` writes a `.mat` file. Nothing in the repo shows the temperature.

## Triage (proposed, pending your confirmation)

| ID | requirement | proposed outcome | reason |
|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature | system-level, active | Shapes the room, controller and system structure |
| R-2 | Swap the room or controller for another variant without touching the rest | system-level, active | Constrains interfaces and dependencies between blocks |
| R-3 | Every model checks in OpenModelica without errors | system-level, active | Applies to every block; the check gate is architectural |

No conflicts between them. Wording sharpening is offered as a proposal only: for R-2, "a variant with the same connectors replaces Room or Thermostat, and no other file changes."

## Rank (proposed, you set the order)

1. R-1: the product's purpose.
2. R-2: it constrains how every block can change.
3. R-3: it protects the other two.

Tie-breakers to answer: "If only one of R-1 and R-2 can be fully met, which?" and "If only one of R-2 and R-3 can be fully met, which?"

## Quality goal candidates (ISO/IEC 25010)

| ID | goal | from | scenario (proposed) | status |
|---|---|---|---|---|
| QG-1 | Functional suitability: functional correctness | R-1 | Stimulus: a 86400 s run with default parameters. Response: it finishes and T is available each interval. Measure: T at 86400 s is within 0.1 K of the expected value. | Depends on the offset question above |
| QG-2 | Maintainability: modifiability | R-2 | Stimulus: a Room variant with the same connectors replaces the original. Measure: 0 files change outside the swapped block; the controller gain follows the room's C. | Not met today (see coupling) |
| QG-3 | Maintainability: testability | R-3 | Stimulus: `checkModel` on every model. Measure: 100% of models pass. | Measurable today: 1 of 4 covered by `tests/check.mos`; all 4 pass when checked |

## Gap questions

- Interoperability: did you leave out exporting results beyond `.mat`, for example CSV?
- Time behaviour: did you leave out a limit on how long a one-day run may take? (Today the simulation takes about 0.015 s; the whole run including compile takes about 1 s.)
- Fail safe: did you leave out a safe state when the temperature signal is missing, for example heater off?

## Decisions made centrally (draft for "Record architecture decisions", number 0001)

Centrally, needs an ADR you accept:

- Connector types and the dependency rule between blocks (`Interfaces`; blocks read each other only through connections).
- Shared parameters and constants: whether blocks may read package constants such as `roomHeatCapacity` (this is the R-2 coupling).
- Units: SI, with Kelvin internally and degC for display only.
- Result output format (`simulate` `.mat` today).
- Third-party libraries (none in use yet).

Left to the building blocks: the equations inside `Room` and `Thermostat`, parameter defaults, and test file layout.

Once you approve this ADR, I will run recovery from the code. Until then, sections 2–8 and 11 stay empty.

## Open for you

1. Confirm or change the triage, R-1 to R-3.
2. Set the rank and answer the two tie-breakers.
3. Confirm or change QG-1 to QG-3, and give the measure for R-1 once you decide the intended temperature.
4. Is the 7 K offset intended?
5. Answer the three gap questions.
6. Name the stakeholders for section 1.
7. Approve, change or reject the decisions list for ADR 0001.

### result (success)

### user

Confirmed as proposed: your triage, your ranking, the quality goals (except any without a
measure: keep those open) and your list of decisions made centrally. To your "did you leave
out" questions: no, nothing is missing. Write it down.

### assistant

I'll record the confirmed items: the R-list, the goals with measures, and the gap answers. QG-1 stays open because its measure depends on the offset question you have not answered. First I'll re-read the file before editing.

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md"
}
```

### tool_result

```
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
11	
12	### Quality goals
13	
14	| ID | goal (ISO/IEC 25010) | from | scenario |
15	|---|---|---|---|
16	
17	### Stakeholders
18	
19	## 2. Constraints
20	
21	## 3. Context and scope
22	
23	## 4. Solution strategy
24	
25	## 5. Building block view
26	
27	| block | responsibility | may use |
28	|---|---|---|
29	
30	## 6. Runtime view
31	
32	## 7. Deployment view
33	
34	## 8. Crosscutting concepts
35	
36	## 9. Architecture decisions
37	
38	ADRs live in `../adr/` (that is, `docs/adr/`); the directory does not exist yet. The "Record architecture decisions" ADR is proposed to the architect and not yet written.
39	
40	## 10. Quality requirements
41	
42	| ID | goal | stimulus | environment | response | measure |
43	|---|---|---|---|---|---|
44	
45	## 11. Risks and technical debt
46	
47	## 12. Glossary
48	
49	`GLOSSARY.md` is created with the first resolved term.
50	
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md",
 "old_string": "| ID | requirement | rank | status | reason |\n|---|---|---|---|---|\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n\n### Stakeholders",
 "new_string": "| ID | requirement | rank | status | reason |\n|---|---|---|---|---|\n| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | Purpose of the product; its structure follows from it. |\n| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | Constrains the interfaces and dependencies between blocks. |\n| R-3 | Every model checks in OpenModelica without errors. | 3 | active | Applies to every block; the check gate is architectural. |\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n| QG-2 | Maintainability: modifiability | R-2 | QS-2 |\n| QG-3 | Maintainability: testability | R-3 | QS-3 |\n\nQG-1 (Functional suitability: functional correctness, from R-1) is open: it has no measure yet. Open question: what is the intended room temperature after 24 h with the default parameters?\n\nGap review: the architect was asked about interoperability, time behaviour and fail safe, and answered that nothing is missing. No further goals.\n\n### Stakeholders"
}
```

### tool_result

```
The file /tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md",
 "old_string": "ADRs live in `../adr/` (that is, `docs/adr/`); the directory does not exist yet. The \"Record architecture decisions\" ADR is proposed to the architect and not yet written.",
 "new_string": "ADRs live in `../adr/` (that is, `docs/adr/`). The ADR that records the line between central and local decisions is [0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md); it is `proposed` until the architect approves its text."
}
```

### tool_result

```
The file /tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md",
 "old_string": "| ID | goal | stimulus | environment | response | measure |\n|---|---|---|---|---|---|\n",
 "new_string": "| ID | goal | stimulus | environment | response | measure |\n|---|---|---|---|---|---|\n| QS-2 | QG-2 | a Room or Thermostat variant with the same connectors replaces the original | a swap test in the project | only the variant's file changes; the other blocks behave as before | 0 files changed outside the swapped block in a swap test |\n| QS-3 | QG-3 | `checkModel` is run on every model of HeatingLib | OpenModelica, the project's version | each model reports success with no error | 100% of models pass (4 of 4 today; `tests/check.mos` covers only `System`) |\n"
}
```

### tool_result

```
The file /tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/adr/0001-record-architecture-decisions.md",
 "content": "# 1. Record architecture decisions\n\n## Status\n\nproposed\n\n## Context\n\nThe architect decides the architecture; contributors and agents build it. HeatingLib must keep its blocks swappable without touching the rest (R-2, QG-2) and every model must check in OpenModelica (R-3, QG-3), so the decisions that cross block boundaries are made centrally. The product itself is the simulation of a heated room over a day (R-1).\n\n## Decision\n\nWe record architecture decisions as ADRs in `docs/adr/`, in Nygard form.\n\nDecided centrally (needs an ADR the architect accepts):\n\n- Connector types and the dependency rule between blocks: blocks are connected only through the connectors in `Interfaces`, and no block reads another block's internals.\n- Shared parameters and constants: whether blocks may read package constants such as `roomHeatCapacity`. Today `Room` and `Thermostat` both do, which is the coupling against R-2.\n- Units: SI, with Kelvin internally and degC for display only.\n- Result output format: the `.mat` file that `simulate` writes.\n- Third-party libraries: none in use yet; adding one is central.\n\nLeft to the building blocks (no ADR):\n\n- Equations inside `Room` and `Thermostat`.\n- Parameter defaults.\n- Test file layout.\n\n## Consequences\n\nWork that depends on a decision on the list waits until its ADR is accepted. In particular, removing the constant coupling between `Room` and `Thermostat` waits for a decision on shared constants.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-yzarbn9i/project/docs/adr/0001-record-architecture-decisions.md (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "git status --short && grep -n \"R-1\\|QG-\\|QS-\" docs/architecture/arc42.md | head -20",
 "description": "Confirm changed files and IDs written"
}
```

### tool_result

```
?? docs/
11:| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | Purpose of the product; its structure follows from it. |
19:| QG-2 | Maintainability: modifiability | R-2 | QS-2 |
20:| QG-3 | Maintainability: testability | R-3 | QS-3 |
22:QG-1 (Functional suitability: functional correctness, from R-1) is open: it has no measure yet. Open question: what is the intended room temperature after 24 h with the default parameters?
53:| QS-2 | QG-2 | a Room or Thermostat variant with the same connectors replaces the original | a swap test in the project | only the variant's file changes; the other blocks behave as before | 0 files changed outside the swapped block in a swap test |
54:| QS-3 | QG-3 | `checkModel` is run on every model of HeatingLib | OpenModelica, the project's version | each model reports success with no error | 100% of models pass (4 of 4 today; `tests/check.mos` covers only `System`) |
```

### assistant

The confirmed parts are written. Two things still wait for you: approval of the ADR text, and the QG-1 measure.

## Written

- **`docs/architecture/arc42.md`**, section 1:
  - R-list: R-1, R-2, R-3, all `active`, ranked 1, 2, 3 as you confirmed. Your original wording is kept; no sharper wording was confirmed.
  - Quality goals: QG-2 (modifiability, from R-2) and QG-3 (testability, from R-3).
  - A note that QG-1 is open, and the gap review answer ("nothing is missing").
- **Section 10:** QS-2 and QS-3 with their measures.
  - QS-2: 0 files changed outside the swapped block in a swap test.
  - QS-3: 100% of models pass `checkModel` (4 of 4 today).
- **Section 9:** links to the ADR.
- **`docs/adr/0001-record-architecture-decisions.md`**, status `proposed`. Its Decision is your confirmed list: connector types and the dependency rule, shared parameters and constants, units, result output format, third-party libraries.

Nothing in the code changed.

## Still open for you

1. **Approve the text of ADR 0001.** You confirmed the list, but the ADR is `proposed` until you approve its written text. Recovery from the code waits for that approval, and sections 2–8 and 11 stay empty until then.
2. **QG-1 measure.** Its measure depends on whether the 7 K offset is intended: the room settles at about 13 °C against the 20 °C set point after 24 h. Tell me the intended temperature and I'll write QG-1 and QS-1. The ID stays reserved until then.
3. **Stakeholders.** Section 1 has the heading but no entries, because you did not answer that question.

## Waiting on ADR 0001

- Removing the constant coupling between `Room` and `Thermostat` (both read `roomHeatCapacity`) waits for a decision on shared constants. It is the R-2 issue.

### result (success)

### user

I approve the "Record architecture decisions" ADR as written. Now recover the rest of the
architecture from the code. I'm offline after this, so finish without asking me again.

### assistant

Recovery starts by accepting ADR 0001 and reading the files I need to edit.

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/adr/0001-record-architecture-decisions.md"
}
```

### tool_result

```
1	# 1. Record architecture decisions
2	
3	## Status
4	
5	proposed
6	
7	## Context
8	
9	The architect decides the architecture; contributors and agents build it. HeatingLib must keep its blocks swappable without touching the rest (R-2, QG-2) and every model must check in OpenModelica (R-3, QG-3), so the decisions that cross block boundaries are made centrally. The product itself is the simulation of a heated room over a day (R-1).
10	
11	## Decision
12	
13	We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.
14	
15	Decided centrally (needs an ADR the architect accepts):
16	
17	- Connector types and the dependency rule between blocks: blocks are connected only through the connectors in `Interfaces`, and no block reads another block's internals.
18	- Shared parameters and constants: whether blocks may read package constants such as `roomHeatCapacity`. Today `Room` and `Thermostat` both do, which is the coupling against R-2.
19	- Units: SI, with Kelvin internally and degC for display only.
20	- Result output format: the `.mat` file that `simulate` writes.
21	- Third-party libraries: none in use yet; adding one is central.
22	
23	Left to the building blocks (no ADR):
24	
25	- Equations inside `Room` and `Thermostat`.
26	- Parameter defaults.
27	- Test file layout.
28	
29	## Consequences
30	
31	Work that depends on a decision on the list waits until its ADR is accepted. In particular, removing the constant coupling between `Room` and `Thermostat` waits for a decision on shared constants.
32	
```

### tool_use Read

```json
{
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md"
}
```

### tool_result

```
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
11	| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | Purpose of the product; its structure follows from it. |
12	| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | Constrains the interfaces and dependencies between blocks. |
13	| R-3 | Every model checks in OpenModelica without errors. | 3 | active | Applies to every block; the check gate is architectural. |
14	
15	### Quality goals
16	
17	| ID | goal (ISO/IEC 25010) | from | scenario |
18	|---|---|---|---|
19	| QG-2 | Maintainability: modifiability | R-2 | QS-2 |
20	| QG-3 | Maintainability: testability | R-3 | QS-3 |
21	
22	QG-1 (Functional suitability: functional correctness, from R-1) is open: it has no measure yet. Open question: what is the intended room temperature after 24 h with the default parameters?
23	
24	Gap review: the architect was asked about interoperability, time behaviour and fail safe, and answered that nothing is missing. No further goals.
25	
26	### Stakeholders
27	
28	## 2. Constraints
29	
30	## 3. Context and scope
31	
32	## 4. Solution strategy
33	
34	## 5. Building block view
35	
36	| block | responsibility | may use |
37	|---|---|---|
38	
39	## 6. Runtime view
40	
41	## 7. Deployment view
42	
43	## 8. Crosscutting concepts
44	
45	## 9. Architecture decisions
46	
47	ADRs live in `../adr/` (that is, `docs/adr/`). The ADR that records the line between central and local decisions is [0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md); it is `proposed` until the architect approves its text.
48	
49	## 10. Quality requirements
50	
51	| ID | goal | stimulus | environment | response | measure |
52	|---|---|---|---|---|---|
53	| QS-2 | QG-2 | a Room or Thermostat variant with the same connectors replaces the original | a swap test in the project | only the variant's file changes; the other blocks behave as before | 0 files changed outside the swapped block in a swap test |
54	| QS-3 | QG-3 | `checkModel` is run on every model of HeatingLib | OpenModelica, the project's version | each model reports success with no error | 100% of models pass (4 of 4 today; `tests/check.mos` covers only `System`) |
55	
56	## 11. Risks and technical debt
57	
58	## 12. Glossary
59	
60	`GLOSSARY.md` is created with the first resolved term.
61	
```

### tool_use Edit

```json
{
 "replace_all": false,
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/adr/0001-record-architecture-decisions.md",
 "old_string": "## Status\n\nproposed",
 "new_string": "## Status\n\naccepted 2026-11-21"
}
```

### tool_result

```
The file /tmp/sa-eval-yzarbn9i/project/docs/adr/0001-record-architecture-decisions.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/adr/0002-blocks-connect-only-through-interfaces.md",
 "content": "# 2. Blocks connect only through the connectors in Interfaces\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not yet confirmed by the architect: `Interfaces.mo` defines the four connectors; `System.mo` connects `room.T` to `thermostat.T` and `thermostat.Q` to `room.Q_heat`; neither `Room` nor `Thermostat` refers to the other. This serves R-2 (a variant replaces a block without touching the rest) and QG-2.\n\n## Decision\n\nWe will connect blocks only through the connectors in `Interfaces` (`TemperatureInput`, `TemperatureOutput`, `HeatFlowInput`, `HeatFlowOutput`), and no block will refer to another block's internals.\n\n## Consequences\n\nA variant that keeps these connectors can replace a block without changes elsewhere (R-2). Shared constants are outside this rule; see ADR 0003. New connectors are a central decision under ADR 0001.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-yzarbn9i/project/docs/adr/0002-blocks-connect-only-through-interfaces.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/adr/0003-blocks-read-shared-room-heat-capacity-constant.md",
 "content": "# 3. Room and Thermostat read the shared constant roomHeatCapacity\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not yet confirmed by the architect: `HeatingLib.roomHeatCapacity` (5e5 J/K) is read by `Room` (default for `C`) and by `Thermostat` (controller gain `k = roomHeatCapacity / tau`). This strains R-2 and QG-2: see QS-2.\n\n## Decision\n\nWe will keep `roomHeatCapacity` as a package constant that `Room` and `Thermostat` both read.\n\n## Consequences\n\nA `Room` variant with a different heat capacity changes the controller gain without any change to `Thermostat`, so R-2 and QS-2 are not met for that case. Changing this is a decision for the architect: a different shape is recorded in a new ADR that supersedes this one. Work that removes the coupling waits for that decision.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-yzarbn9i/project/docs/adr/0003-blocks-read-shared-room-heat-capacity-constant.md (file state is current in your context — no need to Read it back)
```

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/adr/0004-units-si-temperatures-in-kelvin.md",
 "content": "# 4. Units: SI, temperatures in Kelvin internally\n\n## Status\n\nproposed\n\n## Context\n\nFound in the code, not yet confirmed by the architect: `Interfaces.Temperature` is a Real with unit K and display unit degC; `HeatFlowRate` is in W; parameters carry SI units (J/K, W/K, s). This serves R-1 (the temperature is shown) and R-2 (variants with the same connectors agree on units).\n\n## Decision\n\nWe will use SI units throughout: temperatures in K (displayed in degC), heat flow in W, time in s, heat capacity in J/K, conductance in W/K.\n\n## Consequences\n\nBlocks with the same connectors agree on units by construction. The degC display is presentation only. Changing the unit system would affect every block.\n"
}
```

### tool_result

```
File created successfully at: /tmp/sa-eval-yzarbn9i/project/docs/adr/0004-units-si-temperatures-in-kelvin.md (file state is current in your context — no need to Read it back)
```

### assistant

Now the arc42 file: sections 2–8 and 11 filled from the code, each marked as found and unconfirmed. Sections 1, 9, 10 and 12 carry no marker.

### tool_use Write

```json
{
 "file_path": "/tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md",
 "content": "# HeatingLib: architecture\n\nStructured after the arc42 template (https://arc42.org). Empty sections are filled when needed.\n\n## 1. Introduction and goals\n\n### Requirements overview\n\n| ID | requirement | rank | status | reason |\n|---|---|---|---|---|\n| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | Purpose of the product; its structure follows from it. |\n| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | Constrains the interfaces and dependencies between blocks. |\n| R-3 | Every model checks in OpenModelica without errors. | 3 | active | Applies to every block; the check gate is architectural. |\n\n### Quality goals\n\n| ID | goal (ISO/IEC 25010) | from | scenario |\n|---|---|---|---|\n| QG-2 | Maintainability: modifiability | R-2 | QS-2 |\n| QG-3 | Maintainability: testability | R-3 | QS-3 |\n\nQG-1 (Functional suitability: functional correctness, from R-1) is open: it has no measure yet. Open question: what is the intended room temperature after 24 h with the default parameters?\n\nGap review: the architect was asked about interoperability, time behaviour and fail safe, and answered that nothing is missing. No further goals.\n\n### Stakeholders\n\n## 2. Constraints\n\n*As found, unconfirmed.*\n\n- The models are Modelica, checked and simulated with OpenModelica (`omc`). The check runs from the project root with `omc tests/check.mos` (README, `tests/check.mos`).\n- No third-party library is used; the code relies only on Modelica built-ins (`der`, `min`, `max`) and its own package.\n\n## 3. Context and scope\n\n*As found, unconfirmed.*\n\nInside the system: the `HeatingLib` package. Outside it: OpenModelica (`omc`), which loads, checks and simulates the models, and whoever starts a run (the check script or a user at the `omc` prompt). HeatingLib talks to no other system: there are no sensors and no external data feeds. The outdoor temperature `T_amb` is a parameter of `Room`, not a connection.\n\n## 4. Solution strategy\n\n*As found, unconfirmed.*\n\n- **The room is one lumped heat-storing node** with a single loss conductance to the outdoors (`Room`). Traces to R-1.\n- **The controller is proportional with saturation:** `Q = min(Q_max, max(0, k (T_set − T)))`, with `k = roomHeatCapacity / tau` (`Thermostat`). Traces to R-1.\n- **Blocks meet only at connectors,** and `System` composes them by connections (`Interfaces`, `System`). Traces to R-2.\n- **One check script covers the whole package,** but it checks only `System` (`tests/check.mos`). Traces to R-3; see Risks.\n\n## 5. Building block view\n\n*As found, unconfirmed.*\n\n| block | responsibility | in | out | may use |\n|---|---|---|---|---|\n| `Interfaces` | connector and unit types shared by all blocks | none | none | nothing |\n| `Room` | lumped room air: stores heat, loses it through the walls | `Q_heat` (`HeatFlowInput`) | `T` (`TemperatureOutput`) | `Interfaces`; `HeatingLib.roomHeatCapacity` (default of `C`) |\n| `Thermostat` | proportional heating controller with a set point | `T` (`TemperatureInput`) | `Q` (`HeatFlowOutput`) | `Interfaces`; `HeatingLib.roomHeatCapacity` (in `k`) |\n| `System` | a room heated by a thermostat-controlled heater | none | none | `Room`, `Thermostat` |\n| `HeatingLib` (package) | constant `roomHeatCapacity` = 5e5 J/K, read by `Room` and `Thermostat` | none | none | nothing |\n\n`System` connects `room.T` to `thermostat.T` and `thermostat.Q` to `room.Q_heat`. `roomHeatCapacity` is the one shared constant; see [ADR 0003](../adr/0003-blocks-read-shared-room-heat-capacity-constant.md).\n\n## 6. Runtime view\n\n*As found, unconfirmed.*\n\nOne-day run of `System` (`StopTime = 86400` s, default parameters): the room starts at 288.15 K (15 °C). The thermostat demands heat `Q` from the set point 293.15 K (20 °C), with `k` ≈ 277.8 W/K and `Q_max` = 3000 W. The room integrates `C · dT/dt = Q − G (T − T_amb)` with `G` = 150 W/K and `T_amb` = 273.15 K.\n\nScratch run (not in the repo): 288.15 K at 0 s, 286.23 K at 1 h, 286.14 K at 24 h. The 24 h value is the closed-form steady state of this balance, so the simulation matches its equations.\n\nCheck run: `omc tests/check.mos` loads the package and runs `checkModel` on `HeatingLib.System` only.\n\n## 7. Deployment view\n\n*As found, unconfirmed.*\n\nNo deployment: the library is a set of `.mo` files, run locally with OpenModelica (`omc`). Setup is described in the README.\n\n## 8. Crosscutting concepts\n\n*As found, unconfirmed.*\n\n- **Units:** SI throughout. Temperatures in K, displayed as degC (`Interfaces.Temperature`); heat flow in W (`HeatFlowRate`); time in s (`tau`); heat capacity in J/K; conductance in W/K. Parameters carry `unit` attributes. See [ADR 0004](../adr/0004-units-si-temperatures-in-kelvin.md).\n- **Naming:** blocks in UpperCamelCase (`Room`, `Thermostat`, `System`); parameters and variables use short symbols (`T_set`, `Q_max`, `T_amb`) or camelCase (`roomHeatCapacity`).\n- **Shared constants:** `roomHeatCapacity` is the only package constant. See [ADR 0003](../adr/0003-blocks-read-shared-room-heat-capacity-constant.md).\n- **Error handling and logging:** none in the code.\n- **Result output:** `simulate` writes a `.mat` file with its default name; no project format is fixed.\n\n## 9. Architecture decisions\n\nADRs live in `../adr/` (that is, `docs/adr/`). The ADR that records the line between central and local decisions is [0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md), accepted 2026-11-21.\n\n## 10. Quality requirements\n\n| ID | goal | stimulus | environment | response | measure |\n|---|---|---|---|---|---|\n| QS-2 | QG-2 | a Room or Thermostat variant with the same connectors replaces the original | a swap test in the project | only the variant's file changes; the other blocks behave as before | 0 files changed outside the swapped block in a swap test |\n| QS-3 | QG-3 | `checkModel` is run on every model of HeatingLib | OpenModelica, the project's version | each model reports success with no error | 100% of models pass (4 of 4 today; `tests/check.mos` covers only `System`) |\n\n## 11. Risks and technical debt\n\n*As found, unconfirmed.*\n\n- **Controller offset:** the proportional-only controller settles 7 K below the set point (13.0 °C against 20 °C after 24 h). Threatens R-1 and QG-1, which is still open.\n- **Hidden coupling:** `Room`'s default `C` and `Thermostat`'s gain `k` both read `roomHeatCapacity`. A `Room` variant with another heat capacity changes the controller gain with no change in `Thermostat`. Threatens R-2 and QG-2 (QS-2). See [ADR 0003](../adr/0003-blocks-read-shared-room-heat-capacity-constant.md).\n- **Check coverage:** `tests/check.mos` checks only `System`. A broken `Room` or `Thermostat` is not caught by the script. Threatens R-3 and QG-3 (QS-3).\n- **No temperature output:** \"show its temperature\" is met only by the `.mat` file that `simulate` writes. Threatens R-1.\n\n## 12. Glossary\n\n`GLOSSARY.md` is created with the first resolved term.\n"
}
```

### tool_result

```
The file /tmp/sa-eval-yzarbn9i/project/docs/architecture/arc42.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### tool_use Bash

```json
{
 "command": "git status --short --untracked-files=all && ls docs/adr && grep -o '\\.\\./adr/[^)]*' docs/architecture/arc42.md | sort -u | while read p; do test -f \"docs/architecture/$p\" && echo \"ok $p\" || echo \"MISSING $p\"; done",
 "description": "Confirm only docs/ changed and ADR links resolve"
}
```

### tool_result

```
?? docs/adr/0001-record-architecture-decisions.md
?? docs/adr/0002-blocks-connect-only-through-interfaces.md
?? docs/adr/0003-blocks-read-shared-room-heat-capacity-constant.md
?? docs/adr/0004-units-si-temperatures-in-kelvin.md
?? docs/architecture/arc42.md
0001-record-architecture-decisions.md
0002-blocks-connect-only-through-interfaces.md
0003-blocks-read-shared-room-heat-capacity-constant.md
0004-units-si-temperatures-in-kelvin.md
ok ../adr/0001-record-architecture-decisions.md
ok ../adr/0003-blocks-read-shared-room-heat-capacity-constant.md
ok ../adr/0004-units-si-temperatures-in-kelvin.md
MISSING ../adr/` (that is, `docs/adr/`
```

### assistant

Recovery is done. ADR 0001 is accepted as written, dated 2026-11-21, and only its Status line changed. Nothing outside `docs/` changed, and all `docs/` changes are new files.

## What was written

- **`docs/architecture/arc42.md`:** sections 2–8 and 11 are filled from the code, each starting with *As found, unconfirmed.* Sections 1, 9, 10 and 12 carry no marker. Section 5 holds the block table: `Interfaces`, `Room`, `Thermostat`, `System`, and the package constant `roomHeatCapacity`.
- **`docs/adr/0002-blocks-connect-only-through-interfaces.md`:** status `proposed`. The code connects blocks only through the four connectors in `Interfaces`.
- **`docs/adr/0003-blocks-read-shared-room-heat-capacity-constant.md`:** status `proposed`. `Room` and `Thermostat` both read `roomHeatCapacity`. It strains R-2 and QG-2.
- **`docs/adr/0004-units-si-temperatures-in-kelvin.md`:** status `proposed`. The code uses SI units, with temperatures in K displayed as degC.

## Decisions on the approved list with no ADR

- **Result output format:** the code makes no project decision here. `simulate` writes a `.mat` file with its default name. Section 8 records this as found.
- **Third-party libraries:** none are used, and the code shows no decision about them. Section 2 records this as found.

## Open items for when you are back

- **Approve or reject each proposed ADR (0002–0004).** Each stays `proposed` until you approve its text.
- **QG-1 measure:** still open, pending your intended room temperature after 24 h. The offset is recorded as a risk in section 11.
- **Stakeholders:** still empty, since you did not answer that question.
- **Work waiting on the decisions:** removing the `roomHeatCapacity` coupling waits for ADR 0003. Making `check.mos` cover every model, which is QS-3, is not blocked by any ADR and can go ahead.

### result (success)
