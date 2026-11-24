# 3. SI units in Interfaces types, and fixed public class names

## Status

proposed

## Context

Found in the code (`Interfaces.mo`, `Room.mo`, `Thermostat.mo`, `System.mo`), not decided by
the architect. The signal types declare `final quantity` and `final unit` (K, W) and
`displayUnit = "degC"` for temperatures. The public classes are `System`, `Room` and
`Thermostat`. This serves R-2 (QG-2) and the units and naming decision of ADR-0001.

## Decision

Quantities are SI, declared once in the types of `Interfaces.mo`. The public classes are
`System`, `Room` and `Thermostat`.

## Consequences

A variant that replaces a block must use the same types and the same class name for its role
(R-2). Changing a unit or a class name touches every block that uses it.
