# 2. Blocks exchange signals through the connectors in HeatingLib.Interfaces

## Status

proposed

## Context

Found in the code: `HeatingLib/Interfaces.mo` defines the connectors `TemperatureInput`,
`TemperatureOutput`, `HeatFlowInput` and `HeatFlowOutput`; `Room.mo`, `Thermostat.mo` and
`System.mo` use them for every signal. Decision on the accepted list: "Interfaces between
blocks". It serves R-2 (QG-2, modularity): swapping a block depends on this boundary.

## Decision

We exchange signals between blocks only through the connectors defined in `HeatingLib.Interfaces`.

## Consequences

The connectors are the boundary a replacement block must meet. Changing a connector type
affects every block that uses it.
