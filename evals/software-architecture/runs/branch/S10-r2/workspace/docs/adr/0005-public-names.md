# 5. Public names of HeatingLib

## Status

proposed

## Context

Found in the code, not decided: the package is `HeatingLib`; its blocks are `System`, `Room` and
`Thermostat`; connectors and types live in `HeatingLib.Interfaces`; parameters are named `C`,
`G`, `T_amb`, `T_start`, `T_set`, `tau` and `Q_max`. Variants depend on these names (R-2, QG-2).

## Decision

The public names are `HeatingLib`, its blocks `System`, `Room` and `Thermostat`, the types and
connectors in `HeatingLib.Interfaces`, and the parameter names as in the sources.

## Consequences

Renaming any of these breaks variants and `tests/check.mos`. A rename needs a superseding ADR.
