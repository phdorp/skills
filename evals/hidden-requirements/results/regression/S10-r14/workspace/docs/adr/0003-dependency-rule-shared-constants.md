# 3. Blocks may read the shared package constant HeatingLib.roomHeatCapacity

## Status

proposed

## Context

Found in the code: `HeatingLib/package.mo` defines `roomHeatCapacity = 5e5` J/K. `Room.mo` reads it
as the default of `C`, and `Thermostat.mo` reads it to compute the gain `k = roomHeatCapacity / tau`.
Decision on the accepted list: "Dependency rule: which blocks may read another block's constants or
parameters". It serves R-2 (QG-2, modularity), and it bears on the same goal as the connectors in
ADR-0002.

## Decision

We allow blocks to read package-level constants, as `Room` and `Thermostat` read
`HeatingLib.roomHeatCapacity`.

## Consequences

Two blocks now depend on a value neither owns. A room variant with a different heat capacity
also changes the controller's gain, unless the variant is also given its own value. Revisit this
ADR when a superseding decision on R-2 is accepted.
