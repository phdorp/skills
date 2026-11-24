# 2. Interfaces between blocks and the dependency rule

## Status

proposed

## Context

Found in the code (`HeatingLib/Interfaces.mo`, `Room.mo`, `Thermostat.mo`, `System.mo`), not decided by the architect. A room or controller variant must be swappable without touching the rest (R-2, QG-1). ADR-0001 lists the interfaces and the dependency rule as decided centrally.

## Decision

We will connect the blocks only through the connectors of the `Interfaces` package: `Room` exposes `T` (TemperatureOutput) and takes `Q_heat` (HeatFlowInput); `Thermostat` takes `T` (TemperatureInput) and gives `Q` (HeatFlowOutput); `System` connects them with `connect`.

As found, `Room` and `Thermostat` also both read the package constant `HeatingLib.roomHeatCapacity`, outside the connectors. This departs from the rule in ADR-0001 and is recorded as a risk in arc42 section 11.

## Consequences

Swapping a block requires only its connectors to match. The shared constant couples `Room` and `Thermostat`: a room variant with another heat capacity changes the controller gain. Removing that coupling is work that waits until the architect accepts this ADR and decides the rule.
