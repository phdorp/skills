# 4. SI units, with temperatures in kelvin

## Status

proposed

## Context

Found in the code, not decided by the architect: `Interfaces.Temperature` is a `Real` in `K`
with `displayUnit = "degC"`; heat flow is in `W`; `tau` is in `s`; `C` is in `J/K`; `G` is in
`W/K`. Serves R-1: the temperature is simulated in kelvin and shown in °C.

## Decision

We use SI units throughout; temperatures are in kelvin and display in °C.

## Consequences

Every block states its units and uses kelvin for temperatures, with no conversions inside
equations. A variant must follow the same convention.
