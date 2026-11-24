# 3. Units: SI in models, degC for display

## Status

proposed

## Context

Found in the code (`HeatingLib/Interfaces.mo`, `Room.mo`, `Thermostat.mo`), not decided by the architect. The simulation shows its temperature (R-1), and ADR-0001 lists units as decided centrally.

## Decision

We will keep every quantity in SI units in the models: temperatures in kelvin (`Interfaces.Temperature`, unit `K`), power in watts (`HeatFlowRate`, unit `W`), heat capacity in J/K, conductance in W/K, time constants in s. Only the display of a temperature may use `degC` (`displayUnit = "degC"`).

## Consequences

Parameters and equations are written in kelvin, so the default set point 293.15 K is 20 °C. Plots show degrees Celsius without changing the model. Any new block follows the same rule, and its unit attributes must match.
