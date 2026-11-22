# 3. The room heat capacity is one shared package constant

## Status

proposed

## Context

Found in the code, not decided: `package.mo` defines the constant `HeatingLib.roomHeatCapacity`
(5e5 J/K). `Room.mo` uses it as the default of `C`, and `Thermostat.mo` uses it for the gain
`k = roomHeatCapacity / tau`. Serves R-2, QG-2.

## Decision

The room heat capacity is the package constant `HeatingLib.roomHeatCapacity`, read by `Room` and
by `Thermostat`.

## Consequences

A room variant with another heat capacity changes the controller gain unless `Thermostat` stops
reading the constant. That is the failure QS-1 measures. Whether blocks may read shared constants
is the question ADR 0001 leaves open.
