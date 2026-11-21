# 3. Room and Thermostat read the shared constant roomHeatCapacity

## Status

proposed

## Context

Found in the code, not yet confirmed by the architect: `HeatingLib.roomHeatCapacity` (5e5 J/K) is read by `Room` (default for `C`) and by `Thermostat` (controller gain `k = roomHeatCapacity / tau`). This strains R-2 and QG-2: see QS-2.

## Decision

We will keep `roomHeatCapacity` as a package constant that `Room` and `Thermostat` both read.

## Consequences

A `Room` variant with a different heat capacity changes the controller gain without any change to `Thermostat`, so R-2 and QS-2 are not met for that case. Changing this is a decision for the architect: a different shape is recorded in a new ADR that supersedes this one. Work that removes the coupling waits for that decision.
