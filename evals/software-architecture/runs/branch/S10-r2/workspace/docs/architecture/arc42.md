# HeatingLib: architecture

Structured after the arc42 template (https://arc42.org). Empty sections are filled when needed.

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Simulate a heated room over a day and show its temperature. | 1 | active | — |
| R-2 | Swap the room or the controller for another variant without touching the rest. | 3 | active | — |
| R-3 | Every model checks in OpenModelica without errors. | 2 | active | — |

Gap check (confirmed by the architect): no further characteristics are missing.

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-2 | Flexibility: replaceability | R-2 | QS-1 |
| QG-3 | Maintainability: testability | R-3 | QS-2 |

### Stakeholders

## 2. Constraints

*As found, unconfirmed.*

- The model is written in Modelica and simulated and checked with OpenModelica (`omc`); the check script and the README both use it.
- The simulation runs for one day: `System` sets `StopTime = 86400` s.

## 3. Context and scope

*As found, unconfirmed.*

The system is the `HeatingLib` package. It has no runtime connections to other systems. Around it:

- OpenModelica (`omc`) runs the check script `tests/check.mos` and the simulation.
- The outdoor temperature `Room.T_amb` is a parameter, not a live input.

## 4. Solution strategy

*As found, unconfirmed.*

- The room is one lumped heat store: heat capacity `C`, loss to outdoors through conductance `G`.
- Heating is proportional control: `Thermostat` demands `k · (T_set − T)`, clamped to 0 … `Q_max`, with `k = C / tau`. The gain uses the room's heat capacity, which is why the constant is shared (see section 5).
- Blocks exchange signals only through the typed connectors in `Interfaces`; `System` wires them with `connect`.

## 5. Building block view

*As found, unconfirmed.*

| block | responsibility | in | out | may use |
|---|---|---|---|---|
| `Interfaces` (package) | connectors and the unit types shared by all blocks | — | — | — |
| `Room` (model) | stores heat and loses it through the walls | `Q_heat` | `T` | `Interfaces`, `HeatingLib.roomHeatCapacity` (default for `C`) |
| `Thermostat` (block) | proportional heating control with a set point | `T` | `Q` | `Interfaces`, `HeatingLib.roomHeatCapacity` (gain `k`) |
| `System` (model) | connects one room and one thermostat in a closed loop | — | — | `Room`, `Thermostat`, `Interfaces` |
| `HeatingLib` (package) | holds the shared constant `roomHeatCapacity` (5e5 J/K) | — | — | — |
| `tests/check.mos` (script) | checks `HeatingLib.System` with `omc` | — | — | `HeatingLib` package |

`Room` and `Thermostat` both read `HeatingLib.roomHeatCapacity`. That is a dependency between two blocks through a shared constant, not through a connector. See the risk in section 11.

## 6. Runtime view

*As found, unconfirmed.*

`System` is simulated for 86400 s. The room starts at `T_start` (288.15 K). At each step the thermostat turns the measured `T` into a heating demand `Q`, and the room integrates `C · dT/dt = Q − G · (T − T_amb)`. The code produces no output beyond the default simulation result; it has no step that shows the temperature.

## 7. Deployment view

*As found, unconfirmed.*

Nothing is deployed. The library is run locally with `omc`, as the README describes.

## 8. Crosscutting concepts

*As found, unconfirmed.*

- Units: SI. Temperatures are in K (with `displayUnit = "degC"` in `Interfaces`), power in W, heat capacity in J/K. Each parameter carries its unit.
- Naming: blocks and packages are capitalised; parameters use short physics symbols (`C`, `G`, `T_set`, `Q_max`).
- Errors: the code has no error handling. The check script prints errors through `getErrorString()` and does not exit non-zero when there are any.

## 9. Architecture decisions

ADRs live in `../adr/`. The list of decisions made centrally is [ADR-0001: Record architecture decisions](../adr/0001-record-architecture-decisions.md) (status accepted 2026-11-21).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-2 | a replacement `Room` or `Thermostat` variant is substituted in `System` | the rest of the library unchanged | `System` and the other block are unchanged | 0 changed lines outside the replaced block |
| QS-2 | QG-3 | the check script runs over all models in `HeatingLib` | normal project state | each model is reported, and the script exits non-zero on any error | 0 models with errors |

## 11. Risks and technical debt

*As found, unconfirmed.*

- **Hidden coupling through `roomHeatCapacity`.** `Thermostat` takes its gain from the package constant, not from the room it controls. A room variant with a different heat capacity leaves the controller's gain wrong, and the swap needs edits outside the swapped block. Threatens R-2, QG-2.
- **`System` names concrete types.** `System` declares `Room room` and `Thermostat thermostat`, so swapping either one means editing `System`. Threatens R-2, QG-2.
- **The check script covers one model and cannot fail.** `tests/check.mos` runs `checkModel` on `HeatingLib.System` only; `Room`, `Thermostat` and `Interfaces` are not checked. It prints errors but exits 0 either way. Threatens R-3, QG-3.
- **No step shows the temperature.** Nothing in the code produces or plots the simulated temperature; the `StopTime` is the only part of R-1 in place. Threatens R-1.

## 12. Glossary

`GLOSSARY.md` is created with the first resolved term.
