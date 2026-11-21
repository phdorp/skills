# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | The library simulates one room heated by a thermostat over 24 h (86400 s) and makes the room temperature trace available as a result. | 1 | active | Shapes `System`, `Room` and `Thermostat` and the run length. |
| R-2 | Every class in HeatingLib passes `checkModel` in OpenModelica with no errors. | 2 | active | A library-wide quality bar on every change. |
| R-3 | A room or a controller can be replaced by another model with the same connectors, and only the `System` declaration that names it changes. | 3 | active | Extensibility the code only partly supports today: `Thermostat` reads `HeatingLib.roomHeatCapacity` directly. |

Gap check at setup: time behaviour, interoperability of the output format, and functional
completeness were asked about. The architect named no further requirement.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: testability | R-2 | QS-1 |
| QG-2 | Flexibility: replaceability | R-3 | QS-2 |

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- The models are Modelica and are simulated and checked with OpenModelica (`omc`), as `README.md` and `tests/check.mos` show.
- All quantities use SI units (see section 8).

## 3. Context and scope

*As found, unconfirmed.*

- Inside the system: the HeatingLib package, its four classes (`Interfaces`, `Room`, `Thermostat`, `System`) and the package constant `roomHeatCapacity`.
- Outside the system: the outdoor temperature (`Room.T_amb`, default 273.15 K) and the set point (`Thermostat.T_set`, default 293.15 K), both parameters; the OpenModelica tool that runs the models. No external system is connected at run time.

## 4. Solution strategy

*As found, unconfirmed.*

- The room is a lumped model: one heat capacity for the room air (C = 5e5 J/K) and one loss conductance to the outdoors (G = 150 W/K).
- The controller is proportional only, with gain k = C / τ, so that without wall losses the gap to the set point closes with time constant τ = 1800 s. It has no integral term.
- The heater power is limited to the interval [0, Q_max] with Q_max = 3000 W.
- The blocks are connected through typed connectors defined in `Interfaces`.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `Interfaces` | connector and unit types shared by all blocks | none |
| `Room` | lumped room air: stores heat, loses it through the walls to `T_amb`; outputs its temperature `T`, takes heating power `Q_heat` | `Interfaces`; the package constant `roomHeatCapacity` (default of `C`) |
| `Thermostat` | proportional controller: takes the measured temperature `T`, outputs the heating power `Q` with the set point `T_set` | `Interfaces`; the package constant `roomHeatCapacity` (for the gain `k`) |
| `System` | composition of one `Room` and one `Thermostat`, connected in a loop | `Room`, `Thermostat` |
| `HeatingLib` (package) | the constant `roomHeatCapacity` = 5e5 J/K | none |

## 6. Runtime view

*As found, unconfirmed.*

The simulation of `System` runs for 86400 s. The initial equation sets the room to `T_start`
(288.15 K). At each step `Thermostat` computes `Q = min(Q_max, max(0, k · (T_set − T)))` from
the measured `T`, and `Room` integrates `C · dT/dt = Q − G · (T − T_amb)`.

A scratch run with OpenModelica's default solver (dassl, tolerance 1e-6) gave:

| time | room temperature |
|---|---|
| 0 s | 288.15 K (15.0 °C) |
| 1800 s | 286.57 K (13.4 °C) |
| 7200 s | 286.14 K (13.0 °C) |
| 86400 s | 286.14 K (13.0 °C), heater power 1948 W |

The room settles at 13.0 °C against a set point of 20 °C (see section 11).

## 7. Deployment view

*As found, unconfirmed.*

The code says nothing about deployment beyond the command in `README.md`: `omc tests/check.mos`, run from the project root on the developer's machine.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Units:** SI throughout. Temperatures are stored in K and displayed in °C (`Interfaces.Temperature`, `displayUnit = "degC"`). Every other quantity carries a `unit` attribute (J/K, W/K, s, W).
- **Naming:** `T` for a temperature, `Q` for a heat power, parameters with an underscore (`T_set`, `T_amb`, `T_start`, `Q_max`, `Q_heat`); the physical symbols `C`, `G`, `k` and `tau` follow textbook usage.
- **Error handling and logging:** none found. The library has no assertions; errors surface through `checkModel` and `getErrorString()`.
- **Shared values:** the package constant `roomHeatCapacity` is read by two blocks (see section 11).

## 9. Architecture decisions

ADRs live in `docs/adr/`. The [Record architecture decisions](../adr/0001-record-architecture-decisions.md)
ADR (`0001`, status `accepted 2026-11-21`) lists the decisions made centrally.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a change to any class is submitted | normal development, before merge | every class in HeatingLib is checked with `checkModel`; a class that fails is reported | 100% of the library's classes pass `checkModel` with no errors |
| QS-2 | QG-2 | a room variant with a different heat capacity replaces `Room` | normal development | only `System.mo` changes; the controller gain follows the replaced room's capacity | 0 lines changed outside `System.mo`; controller gain equals the replaced room's C / tau |

## 11. Risks and technical debt

*As found, unconfirmed.*

1. **Hidden coupling through a package constant.** `Room` (default of `C`) and `Thermostat` (gain `k`) both read `HeatingLib.roomHeatCapacity`. This contradicts the second item of the accepted ADR 0001 and makes QS-2 fail: a room with another capacity leaves the controller gain unchanged.
2. **Steady-state offset.** With proportional control only, the room settles at 286.1 K (13.0 °C) against a 20 °C set point. This bears on R-1; the measure for its functional correctness is still open.
3. **Incomplete checks.** `tests/check.mos` checks `HeatingLib.System` only. `Room` and `Thermostat` pass `checkModel` when checked alone, but no script checks them, and the `Interfaces` package is never checked. QS-1 is not met as the scripts stand.
4. **No output format.** Nothing in the code defines how the temperature trace is made available; OpenModelica writes its default `.mat` result file. R-1 depends on this, and the output format is an open item of ADR 0001.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
