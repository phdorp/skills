# 5. Quantities use SI units; temperatures are in K and displayed in °C

## Status

proposed

## Context

Found in the code: `HeatingLib/Interfaces.mo` declares `Temperature` in K with
`displayUnit = "degC"`, and `HeatFlowRate` in W. Parameters in `Room.mo` and `Thermostat.mo` carry
SI units (J/K, W/K, s, W). Decision on the accepted list: "Units". It serves R-1 (QG-1), since the
simulated temperature is shown, and it is a crosscutting convention for every block.

## Decision

We express quantities in SI units inside the library, temperatures in K, and show temperatures
in °C only for display.

## Consequences

Every block that takes or returns a temperature uses K. A new block that uses °C internally would
break this convention.
