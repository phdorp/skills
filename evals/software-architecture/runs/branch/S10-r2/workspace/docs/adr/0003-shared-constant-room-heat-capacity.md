# 3. Shared constant roomHeatCapacity lives in the package and is read by Room and Thermostat

## Status

proposed

## Context

Found in the code, unconfirmed. `HeatingLib/package.mo` defines `roomHeatCapacity = 5e5` J/K.
`Room.mo` uses it as the default for `C`; `Thermostat.mo` uses it for the gain
`k = roomHeatCapacity / tau`, with a comment saying so. Serves R-2 and QG-2. The ownership of
the constant is on the central list (`ADR-0001`).

## Decision

We will keep `roomHeatCapacity` in the `HeatingLib` package, and only `Room` will read it.

## Consequences

This decision contradicts the code: `Thermostat` reads the constant too. Under this decision
`Thermostat` would get the heat capacity from its room (a connector or a parameter), not from
the package. That change waits for this ADR's acceptance and for ADR-0002.
