# 2. Share the heat capacity through System, not a package constant

## Status

proposed

## Context

`Room` (`C`) and `Thermostat` (`k = C / tau`) both read the package constant
`HeatingLib.roomHeatCapacity`. That couples both blocks to a value outside their ports and
breaks the rule in arc42 §5 that `Room` and `Thermostat` may only use `Interfaces`.
The coupling works against QG-2 and QS-2: a two-zone room with a different heat capacity
would need a change to `Thermostat.mo`, which QS-2 forbids.

This is an arc42 §5 dependency rule and a library dependency, so it is decided centrally
(ADR-0001).

## Decision

We will remove the package constant `roomHeatCapacity`. `System` will declare the heat capacity
once and pass it to `Room` and `Thermostat` by modifier. `Thermostat` will take the capacity as a
parameter `C` and compute its gain `k = C / tau` itself. No block reads from the package root.

## Consequences

- `Room` and `Thermostat` depend only on `Interfaces`, as arc42 §5 states. QS-2 becomes
  measurable: a two-zone room can be wired with its own capacity without touching
  `Thermostat.mo`.
- `Thermostat` gains a parameter; `System` owns the shared value.
- ADR-0001's rule that blocks do not depend on each other is unchanged.
- Code changes wait until this ADR is accepted.
