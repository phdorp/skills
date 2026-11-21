# 2. Blocks connect only through the connectors in Interfaces

## Status

proposed

## Context

Found in the code, not yet confirmed by the architect: `Interfaces.mo` defines the four connectors; `System.mo` connects `room.T` to `thermostat.T` and `thermostat.Q` to `room.Q_heat`; neither `Room` nor `Thermostat` refers to the other. This serves R-2 (a variant replaces a block without touching the rest) and QG-2.

## Decision

We will connect blocks only through the connectors in `Interfaces` (`TemperatureInput`, `TemperatureOutput`, `HeatFlowInput`, `HeatFlowOutput`), and no block will refer to another block's internals.

## Consequences

A variant that keeps these connectors can replace a block without changes elsewhere (R-2). Shared constants are outside this rule; see ADR 0003. New connectors are a central decision under ADR 0001.
