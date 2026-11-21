# 4. Units: SI, temperatures in Kelvin internally

## Status

proposed

## Context

Found in the code, not yet confirmed by the architect: `Interfaces.Temperature` is a Real with unit K and display unit degC; `HeatFlowRate` is in W; parameters carry SI units (J/K, W/K, s). This serves R-1 (the temperature is shown) and R-2 (variants with the same connectors agree on units).

## Decision

We will use SI units throughout: temperatures in K (displayed in degC), heat flow in W, time in s, heat capacity in J/K, conductance in W/K.

## Consequences

Blocks with the same connectors agree on units by construction. The degC display is presentation only. Changing the unit system would affect every block.
