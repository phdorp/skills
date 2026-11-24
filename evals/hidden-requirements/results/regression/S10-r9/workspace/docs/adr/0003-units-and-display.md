# 3. Units: SI, temperatures shown in °C

## Status

proposed

## Context

Found in the code, not decided by the architect: `Interfaces.Temperature` is in K with
`displayUnit = "degC"`, `HeatFlowRate` is in W, and the parameters carry J/K (`C`), W/K (`G`,
`k`) and s (`tau`) (`Interfaces.mo`, `Room.mo`, `Thermostat.mo`). It serves R-1, which asks for
the room temperature over a day. This is the "Units" item of ADR-0001.

## Decision

We will use SI units throughout (K, W, J/K, W/K, s) and show temperatures in °C.

## Consequences

A new block takes these units. A block that needs other units waits for its own ADR.
