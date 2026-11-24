# 3. Blocks read the shared package constant roomHeatCapacity

## Status

proposed

## Context

Found in the code: `HeatingLib/Room.mo` sets `C` from `HeatingLib.roomHeatCapacity`, and `HeatingLib/Thermostat.mo` derives its gain `k` from the same constant. Reading a shared constant couples the blocks outside their connectors. This touches R-2 and QG-2, and section 11 of arc42 records it as a risk.

## Decision

We read the heat capacity from the shared package constant `HeatingLib.roomHeatCapacity` in every block that needs it.

## Consequences

Changing the constant changes every block that reads it. A variant `Room` with another `C` does not change the controller's gain. A rule that forbids shared constants would change `Thermostat`; work that depends on the rule waits until the architect decides it.

Question for the architect: keep the shared constant as the rule, or forbid it?
