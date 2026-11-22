# 5. Library names of blocks, connectors and parameters

## Status

proposed

## Context

Found in the code, not decided by the architect: the blocks are `Room`, `Thermostat` and
`System`; the connectors are in `Interfaces`; the parameters are `C`, `G`, `T_amb`, `T_start`
(`Room`) and `T_set`, `tau`, `Q_max` (`Thermostat`). The code has no version number or
deprecation policy. Serves R-2 and QG-1: a block is swapped by its name and parameters.

## Decision

We name blocks, connectors and parameters as the code does: the blocks `Room`, `Thermostat` and
`System`, the connectors in `HeatingLib.Interfaces`, and the parameters listed above.

## Consequences

Renaming a block, connector or parameter breaks every user of the library; the code gives no
versioning policy for this (open question for the architect).
