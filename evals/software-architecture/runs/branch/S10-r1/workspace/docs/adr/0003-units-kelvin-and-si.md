# 3. Temperatures in kelvin, displayed in Celsius; other quantities in SI

## Status

proposed

## Context

Found in the code, not decided by the architect: `Interfaces.mo` defines `Temperature` with
`unit = "K"` and `displayUnit = "degC"`, and `Room.mo`, `Thermostat.mo` and `package.mo` give
every other quantity an SI unit attribute (J/K, W/K, s, W). This is a crosscutting convention of
the kind ADR 0001 lists as decided centrally. It serves the correctness of the temperature trace
(R-1).

## Decision

We store temperatures in K, display them in °C, and give every quantity an SI unit attribute.

## Consequences

Parameters such as `T_set` and `T_amb` are given in K; a user who thinks in °C converts first.
Any new block follows the same convention.
