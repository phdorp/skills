# 4. Naming and package layout

## Status

proposed

## Context

Found in the code (`HeatingLib/package.mo`, `package.order`, the file layout), not decided by the architect. Naming keeps variants swappable (R-2, QG-1), so the names must say which block is which.

## Decision

We will keep one model or block per file in the `HeatingLib` package. `package.order` gives the load order and `package.mo` holds the package constant. Models and blocks are named in CamelCase (`Room`, `Thermostat`, `System`). Connectors are named by their direction (`TemperatureInput`, `HeatFlowOutput`). Parameters and signals use the names from the code (`T_set`, `T_amb`, `Q_max`, `Q_heat`).

## Consequences

A new block is a new file, added to `package.order`. Names follow the existing pattern, so a variant is found by its name.
