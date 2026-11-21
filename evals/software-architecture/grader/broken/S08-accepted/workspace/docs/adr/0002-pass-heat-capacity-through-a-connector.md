# 2. Pass the room's heat capacity to the thermostat through a connector

## Status

accepted 2026-11-21

## Context

`Thermostat` reads `HeatingLib.roomHeatCapacity`, the constant `Room` uses, so replacing the
room changes the controller's gain behind its ports (R-2, QG-2, QS-2).

## Decision

`Room` publishes its heat capacity on an output connector; `Thermostat` reads it from an input
connector. The package constant is removed.

## Consequences

A room variant works with the unchanged thermostat. `Interfaces` gains one connector.
