# 4. Units are SI, with temperatures in kelvin

## Status

proposed

## Context

Found in the code, unconfirmed. `Interfaces.mo` types temperatures as `Real` in K
(`unit = "K"`, `min = 0`, with `displayUnit = "degC"` for display), power as `Real` in W, and
`Room.mo` and `Thermostat.mo` carry units on their parameters (J/K, W/K, s). Serves R-1 and
R-2, since blocks must agree on units to be swapped. Units are a crosscutting convention on
the central list (`ADR-0001`).

## Decision

We will use SI units everywhere: temperatures in kelvin, power in watts, heat capacity in
J/K, conductance in W/K, time in seconds.

## Consequences

Any block added or swapped follows this convention. Display in degrees Celsius is allowed
only through `displayUnit`.
