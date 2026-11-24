# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | The system simulates one room heated by a thermostat for 24 h and gives the room temperature over that time. | 1 | active | the function the library exists for |
| R-2 | A room model or a controller model can be replaced by another variant with the same connectors; only the wiring in `System` changes. | 3 | active | a design property; it can follow R-1 and R-3 |
| R-3 | Every model in `HeatingLib` passes an OpenModelica check with no errors. | 2 | active | the check every other requirement is verified against |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Maintainability: modifiability | R-2 | QS-1 |
| QG-2 | Maintainability: testability | R-3 | QS-2 |

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- The models run on OpenModelica (`omc`); `README.md` names it as the tool (`omc tests/check.mos`).
- The package uses no external library: no `uses` annotation and no import in `HeatingLib/package.mo` or the models.

## 3. Context and scope

*As found, unconfirmed.*

- Inside the boundary: the `HeatingLib` package (`Interfaces`, `Room`, `Thermostat`, `System`, and the constant `roomHeatCapacity`).
- Outside: OpenModelica (`omc`), which loads the package, checks the models and simulates `System`; and the person who runs `tests/check.mos`, the only script in the repository.

## 4. Solution strategy

*As found, unconfirmed.*

- The room is one lumped heat-capacity model: one temperature state, and heat loss to the outdoor temperature through one conductance (`Room`). It yields a room temperature over a day (R-1).
- The heating is a proportional controller with a power limit (`Thermostat`), closed around the room through connectors and wired only in `System`. A variant is a different block with the same connectors (R-2).

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | in | out | may use |
|---|---|---|---|---|
| `HeatingLib.Interfaces` | connector and signal types: `Temperature`, `HeatFlowRate`, `TemperatureInput/Output`, `HeatFlowInput/Output` | none | the types | none |
| `Room` | lumped room air: stores heat and loses it through the walls | `Q_heat` (HeatFlowInput) | `T` (TemperatureOutput) | `Interfaces`; `roomHeatCapacity` (default for `C`) |
| `Thermostat` | proportional heating controller with a set point and a power limit | `T` (TemperatureInput) | `Q` (HeatFlowOutput) | `Interfaces`; `roomHeatCapacity` (controller gain) |
| `System` | composes the room and the thermostat and connects them into the closed loop | none | none | `Room`, `Thermostat`, `Interfaces` |
| `HeatingLib` (constant `roomHeatCapacity`) | shared heat capacity, 5e5 J/K | none | the value | none |

`roomHeatCapacity` is read by `Room` and `Thermostat`: a value shared across blocks, not passed
through a connector. A `Room` variant with another heat capacity leaves the controller gain
unchanged (see section 11).

## 6. Runtime view

*As found, unconfirmed.*

- A simulation of `System` runs to a stop time of 86 400 s (`annotation(experiment)`). The room starts at `T_start` (288.15 K, 15 °C). `Room` integrates `C·dT/dt = Q_heat − G·(T − T_amb)`, and `Thermostat` sets `Q` from `T` at each step.
- In one run of the simulation, the room is at 14.04 °C at 1800 s, 13.08 °C at 3600 s, and 12.99 °C from about 7200 s on. Heater power settles at 1948 W, below the 3000 W limit. The set point is 20 °C (293.15 K).

## 7. Deployment view

*As found, unconfirmed.*

- A developer's machine: the package is loaded and checked with `omc tests/check.mos` from the project root (`README.md`). The repository holds no other deployment.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- Units: SI, in K, W, J/K, W/K and s, declared with unit attributes. Temperatures carry `displayUnit = "degC"` (`Interfaces.mo`).
- Naming: connector types end in `Input` or `Output`; parameters are named after their physical role (`C`, `G`, `T_amb`, `T_start`, `T_set`, `tau`, `Q_max`).
- Errors and logging: none in the models. The check script prints `getErrorString()` after each step and nothing else.

## 9. Architecture decisions

The ADRs are kept in [`docs/adr/`](../adr/). The "Record architecture decisions" ADR is
[ADR-0001](../adr/0001-record-architecture-decisions.md), status `accepted 2026-11-24`.

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | a developer adds a room variant with the same connectors as `Room` | normal development | only the variant file and the wiring in `System` change | 0 lines changed in `Thermostat` and `Interfaces` |
| QS-2 | QG-2 | a check runs over every model in `HeatingLib` | normal development | each model reports no error | 0 failing models out of every model in the package |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Hidden coupling through `roomHeatCapacity`.** `Room` and `Thermostat` both read the package constant. A `Room` variant with another heat capacity leaves the gain in `Thermostat` tuned for the old value, and nothing reports it. Threatens R-2 and QG-1. The code breaks the dependency rule on ADR-0001's list, which has no ADR of its own yet.
- **Set point not reached.** The controller is proportional only, with no integral action. The room settles at 12.99 °C against a 20 °C set point. Threatens R-1; the functional-correctness goal is still open.
- **No variant mechanism.** `System` declares `Room` and `Thermostat` directly, with no `replaceable`, so swapping a block edits `System`. Threatens R-2 and the measure of QS-1.
- **Partial check script.** `tests/check.mos` checks only `HeatingLib.System`. `Room` and `Thermostat` pass when checked by hand, but no file in the repository checks them. Threatens R-3 and QS-2.
- **`package.order` lists `roomHeatCapacity`,** which is a constant, not a class file. Unverified whether the tooling reads it; it may confuse the load order. Threatens maintainability.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
