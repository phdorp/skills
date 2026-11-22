# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | A 24 h simulation of the heated room yields the room temperature over time, in a form a user can plot. | 1 | active | The purpose of the library; the rest serves it. |
| R-2 | A room or thermostat variant replaces another with the same connectors, and only that block and its instance declaration change. | 2 | active | Sets the block boundaries and the dependency rule; violated today by `Thermostat` reading `roomHeatCapacity`. |
| R-3 | `checkModel` reports no error for every model class in HeatingLib, run by `omc tests/check.mos`. | 3 | active | Already largely met; cheap to enforce for every model. |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-2 | Maintainability: modularity | R-2 | QS-1 |
| QG-3 | Maintainability: testability | R-3 | QS-2 |

QG-1 (Functional suitability: functional correctness, from R-1) is open: no measure is confirmed yet.

### Stakeholders

### Gap review

Asked at setup whether anything is missing for performance efficiency (time behaviour),
compatibility (interoperability) and safety (fail safe). The architect answered no to each;
no requirement was added.

## 2. Constraints

*As found, unconfirmed.*

- The library is run and checked with OpenModelica (`omc`); the check is `omc tests/check.mos` from
  the project root (`README.md`, `tests/check.mos`).
- No source file imports another Modelica library (ADR 0006).

## 3. Context and scope

*As found, unconfirmed.*

HeatingLib is a Modelica library. Its boundary is the `HeatingLib` package. Outside it stands
OpenModelica (`omc`), which loads, checks and simulates it. No external signal enters the model:
the outdoor temperature `T_amb` is a parameter (`Room.mo`).

## 4. Solution strategy

*As found, unconfirmed.*

- The room is one lumped heat store with one state, its temperature, and heat loss through the
  walls (`Room.mo`).
- Heating is a proportional controller with a set point; its gain is the room's heat capacity
  divided by a time constant (`Thermostat.mo`).
- The blocks are wired in `System` through connectors (`System.mo`, ADR 0002), with one shared
  constant for the heat capacity (`package.mo`, ADR 0003).

The goals these serve are not traced yet: QG-1 is open.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | in | out | may use |
|---|---|---|---|---|
| `Room` | lumped room air: stores heat and loses it through the walls | `Q_heat` (heating power) | `T` (room temperature) | `Interfaces`; `HeatingLib.roomHeatCapacity` (default of `C`) |
| `Thermostat` | proportional heating controller with set point and power limit | `T` (room temperature) | `Q` (heating power) | `Interfaces`; `HeatingLib.roomHeatCapacity` (gain `k`) |
| `System` | connects a room to a thermostat | none | none | `Room`, `Thermostat` |
| `Interfaces` | connector and unit types shared by all blocks | none | none | none |

`HeatingLib.roomHeatCapacity` is one package constant (ADR 0003), read by `Room` and by
`Thermostat`. `Thermostat` reads it although ADR 0001's dependency rule forbids blocks from reading
other blocks' constants (see section 11).

## 6. Runtime view

*As found, unconfirmed.*

`System` runs for 86400 s (`System.mo`, `experiment`) from `T_start` = 288.15 K. A scratch run in
OpenModelica, outside the repo, gave 286.14 K at 86400 s with default parameters, while the heating
power there is 1948 W, below `Q_max`. The room settles about 6 K below the set point (section 11).

## 7. Deployment view

*As found, unconfirmed.*

The code has no deployment. OpenModelica loads and runs the library from the project root.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- **Units:** SI; temperatures in K, shown in degC; parameters carry `unit` attributes (ADR 0004).
- **Names:** the package is `HeatingLib`; connectors and types live in `Interfaces`; signals are
  `T` and `Q`, and the heating input is `Q_heat` (ADR 0005).
- **Error handling:** none in the code. `tests/check.mos` reports OpenModelica's errors through
  `getErrorString()`.
- **Simulation output:** the code sets no output format; OpenModelica's default result file is used.

## 9. Architecture decisions

Architecture decisions are recorded as ADRs in [`docs/adr/`](../adr/). The rule for which decisions
need one is in [0001 Record architecture decisions](../adr/0001-record-architecture-decisions.md).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a developer replaces `Room` with a variant of another heat capacity | the current library | only the variant and its declaration in `System` change; `Thermostat` is unchanged | 0 edited lines in `Thermostat.mo` and `Interfaces.mo` |
| QS-2 | QG-3 | a developer runs `omc tests/check.mos` after a change | the current library; OpenModelica version open | every model class checks without error and the run exits 0 | 0 check errors across the model classes (3 today: `Room`, `Thermostat`, `System`) |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **`Thermostat` reads `roomHeatCapacity`.** A room variant with another heat capacity changes the
  controller gain, and swapping the room needs a change in `Thermostat`. Threatens R-2 and QG-2.
  Fixing it waits for ADRs 0002 and 0003 to be accepted.
- **The check script covers only `System`.** `tests/check.mos` calls `checkModel` on
  `HeatingLib.System` alone. `Room` and `Thermostat` pass when checked alone (scratch run), but
  nothing in the repo checks them. Threatens R-3 and QG-3.
- **Controller offset.** The room settles about 6 K below the set point. The code is a proportional
  controller with no integral term (`Thermostat.mo`); whether the offset is intended is not
  confirmed. Threatens R-1 and QG-1.
- **`package.order` lists `roomHeatCapacity`,** a constant, not a class. Its effect is not verified.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
