# 3. Blocks read the room heat capacity from a package constant

## Status

proposed

## Context

Found in the code, not decided by the architect: `HeatingLib/package.mo` defines
`roomHeatCapacity = 5e5` J/K. `Room` uses it as the default of its parameter `C`, and
`Thermostat` uses it in its gain `k = roomHeatCapacity / tau`, as its own comment says. Serves
R-2 and QG-1, and conflicts with them: a `Room` variant with a different `C` silently changes the
controller's gain.

## Decision

We read the room heat capacity from the package constant `HeatingLib.roomHeatCapacity` in `Room`
and in `Thermostat`.

## Consequences

Conflicts with QG-1 (R-2): swapping `Room` for a variant with another heat capacity changes
`Thermostat` without any change to `Thermostat`'s own files. Choosing another way to share the
value is an architect's decision; `Thermostat`'s reading changes only after that decision is
accepted (ADR 0001).
