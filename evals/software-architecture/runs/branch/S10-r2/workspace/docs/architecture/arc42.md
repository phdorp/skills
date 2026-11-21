# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over 24 h and output its temperature trajectory. | 1 | active | Fixes the model structure and the simulation output; `System.mo` already does this. |
| R-2 | A room or a controller can be replaced by another variant with the same connectors, without editing `System` or the other block. | 2 | active | Sets the interfaces and the dependency rule. The current `Thermostat.mo` reads `HeatingLib.roomHeatCapacity` directly, which breaks this. |
| R-3 | Every model in HeatingLib passes OpenModelica `checkModel` with no errors. | 3 | active | Sets the testability bar. Room, Thermostat and System pass today; `tests/check.mos` checks only System. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-2 | Flexibility: replaceability | R-2 | QS-1 |
| QG-3 | Maintainability: testability | R-3 | QS-2 |

QG-1 (Functional suitability: functional correctness, from R-1) is open: no measure yet. The
architect has to name the tolerance against the expected temperature curve.

### Stakeholders

### Gap check

Asked about time behaviour, interoperability and safety. The architect left nothing out; no
new requirement came from it.

## 2. Constraints

*As found, unconfirmed.*

- The model is written in Modelica and checked with OpenModelica (`omc`) (`README.md`,
  `tests/check.mos`).

## 3. Context and scope

*As found, unconfirmed.*

The system is one room with a heater and a thermostat, simulated for one day (86400 s). The
outdoor temperature `T_amb` is a constant parameter. Nothing outside the model is connected:
the output is the simulation result, which the user reads.

## 4. Solution strategy

*As found, unconfirmed.*

- A lumped room: one heat capacity, with heat loss through the walls to a constant outdoor
  temperature.
- A proportional controller with a set point and a heater power limit.
- Blocks connected through typed connectors (`HeatingLib/Interfaces.mo`).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | may use |
|---|---|---|
| `HeatingLib` (package) | holds the shared constant `roomHeatCapacity` (5e5 J/K) | none |
| `Interfaces` | connectors and unit types for temperature and heat flow | none |
| `Room` | lumped room air: stores heat, loses it through the walls | `Interfaces`; the package constant `roomHeatCapacity` |
| `Thermostat` | proportional controller with set point and power limit | `Interfaces`; the package constant `roomHeatCapacity` |
| `System` | connects `Room` and `Thermostat`; sets the one-day stop time | `Room`, `Thermostat` |
| `tests/check.mos` | checks the package and `System` with `omc` | `HeatingLib` |

## 6. Runtime view

*As found, unconfirmed.*

`System` runs for 86400 s. The room starts at 288.15 K (15 °C). At each step the thermostat
reads the room temperature `T` and gives `Q = min(Q_max, max(0, k * (T_set - T)))`, where
`k = roomHeatCapacity / tau`. The room integrates `C * der(T) = Q_heat - G * (T - T_amb)`.

Simulated once with `omc` at the default parameters: the room starts at 15 °C and falls to
286.14 K (about 13 °C) by the end of the day; the heater runs at 1948 W at the end, below its
3000 W limit. The set point (20 °C) is never reached (see section 11).

## 7. Deployment view

## 8. Crosscutting concepts

*As found, unconfirmed.*

- Units: SI. Temperature in K internally with `displayUnit = "degC"`; heat flow in W; time
  in s (`HeatingLib/Interfaces.mo`, unit annotations on parameters).
- Naming: the `HeatingLib` package, one class per file, each file starts with `within HeatingLib;`
  (`package.order` for load order).
- Error handling and logging: none in the code.

## 9. Architecture decisions

The architecture decisions are recorded as ADRs in [`../adr/`](../adr/). The ADR
[Record architecture decisions](../adr/0001-record-architecture-decisions.md) is accepted
2026-11-21.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a room variant with a different heat capacity is swapped in | normal development | only the swapped block changes; `System` and the controller are untouched | 0 edits to `System` and to the controller |
| QS-2 | QG-3 | `checkModel` runs on every model in the package | normal development, OpenModelica | no errors reported for any model | 0 models with errors |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Hidden coupling through a shared constant:** `Room` and `Thermostat` both read
  `roomHeatCapacity`. Swapping the room changes the controller gain, so QS-1 (QG-2) is not met.
- **Steady-state offset:** the proportional controller settles at about 13 °C, below the 20 °C
  set point. Simulated: the room falls from 15 °C to 286.14 K (about 13 °C), and the heater
  stays under its limit. This may be intended behaviour, but nothing in the code says so. It
  touches QG-1, which has no measure yet.
- **Partial checks:** `tests/check.mos` checks only `System`. QS-2 (QG-3), which asks for every
  model, is not enforced; `Room` and `Thermostat` pass when checked by hand.
- **No behaviour test:** nothing compares a simulated trajectory with an expected value, so QG-1
  has no test behind it.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
