# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | Purpose of the library; shapes the simulation model. |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 2 | active | Most architecture-shaping: fixes the connectors and what each block may depend on. |
| R-3 | Every model checks in OpenModelica without errors. | 3 | active | A gate every model must pass; a convention for all blocks. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: modifiability | R-2 | QS-1 |
| QG-2 | Maintainability: testability | R-3 | QS-2 |

Open, without a measure yet: Functional suitability: functional completeness (from R-1).
Open question: what would show R-1 is met (which temperature accuracy or range counts as
correct, and what "show" means).

### Stakeholders

- Modellers: the users of the library, a handful of people, who run OpenModelica.
- Maintainer: one person who knows Modelica and OpenModelica and builds and maintains the library.

## 2. Constraints

- Open-source tooling only; no commercial tools or licences.
- Runs wherever OpenModelica runs.

*As found, unconfirmed.*

- The library is Modelica source in one package, `HeatingLib`, with no third-party library (ADR-0005).
- The check is `omc tests/check.mos`, run from the project root. The script loads the package and checks `HeatingLib.System`.

## 3. Context and scope

- First version: one room, one thermostat, a one-day simulation, and a plot of the temperature.
- No external systems in the first version: no FMU export, no data files, no exchange with other tools.
- Out of scope (non-goals): real-time and hardware-in-the-loop use; a custom GUI beyond what OpenModelica provides.

*As found, unconfirmed.*

- The boundary is the room. The outdoor temperature is a fixed parameter, `T_amb` = 273.15 K (0 °C), not an input.
- No signal crosses the boundary: `System` has no connectors. The simulation outputs the room temperature and the heat flow.

## 4. Solution strategy

*As found, unconfirmed.*

- Lumped heat balance: the room is one state, the temperature `T`, with `C · dT/dt = Q_heat − G · (T − T_amb)`.
- Proportional control: `Q = min(Q_max, max(0, k · (T_set − T)))` with `k = C / tau`, so the controller closes the gap to the set point with time constant `tau` (1800 s).
- Composition: `System` connects the two blocks and sets the one-day experiment (`StopTime` = 86400 s). This traces to R-1 (QG-1 is open for R-1).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | in | out | may use |
|---|---|---|---|---|
| Room | lumped room air: stores heat, loses it through the walls | `Q_heat` (HeatFlowInput) | `T` (TemperatureOutput) | Interfaces; `HeatingLib.roomHeatCapacity` |
| Thermostat | proportional heating controller with a set point | `T` (TemperatureInput) | `Q` (HeatFlowOutput) | Interfaces; `HeatingLib.roomHeatCapacity` |
| System | connects Room and Thermostat; sets the one-day experiment | none | none | Room, Thermostat |
| Interfaces | connectors and units shared by all blocks | none | none | none |
| HeatingLib (package) | package constant `roomHeatCapacity` = 5e5 J/K | none | none | none |

`HeatingLib.roomHeatCapacity` is a shared constant, not a connector: `Room` and `Thermostat` both read it (see section 11).

## 6. Runtime view

*As found, unconfirmed.*

- The simulation starts at `T_start` = 288.15 K (15 °C) and runs for 86400 s.
- The controller heats at about 1390 W at the start, below `Q_max`. The room reaches 286.14 K (12.99 °C) by about 4 hours and stays there to the end of the day (simulated on a copy of the project).

## 7. Deployment view

*As found, unconfirmed.*

- No deployment: the library is Modelica source, run by OpenModelica on the developer's machine. The repository holds no build or runtime artefacts.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- Units: SI in models (K, W, J/K, W/K, s); `degC` only for display (`Interfaces.Temperature`), as ADR-0003 records.
- Naming: CamelCase for models and blocks (`Room`, `Thermostat`); connectors named by direction; parameter and signal names as in the code (`T_set`, `T_amb`, `Q_max`, `Q_heat`), as ADR-0004 records.
- Package layout: one file per model or block; `package.order` gives the load order; `package.mo` holds the package constant.
- Error handling: none in the code; the check script prints the error string (`getErrorString()`).

## 9. Architecture decisions

ADRs live in `docs/adr/`. The "Record architecture decisions" ADR is [ADR-0001](../adr/0001-record-architecture-decisions.md), accepted 2026-11-24.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a new room or controller variant is added | the library as it is today | only the new variant's file is added; no existing block is changed | 0 existing files edited |
| QS-2 | QG-2 | any model in the library is changed | normal development | every model is checked with OpenModelica | 0 errors |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Shared constant:** `Room` (`C`) and `Thermostat` (`k`) both read `HeatingLib.roomHeatCapacity`. A room variant with another heat capacity silently changes the controller gain. Threatens QG-1 (R-2) and the rule ADR-0001 lists.
- **Hard-wired blocks:** `System` declares `Room` and `Thermostat` by type, so swapping a variant means editing `System.mo`. Threatens QG-1 (R-2); QS-1 measures this.
- **Steady-state offset:** the proportional controller settles the room at 286.14 K (12.99 °C), 7 K below the 20 °C set point, and stays there for the day. Threatens R-1 (the temperature shown is wrong against the set point) and the open R-1 goal.
- **Partial check:** `tests/check.mos` checks only `HeatingLib.System`. `Room` and `Thermostat` pass when checked alone (checked by hand), but nothing runs that check. Threatens QG-2 (R-3); QS-2 measures this.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
