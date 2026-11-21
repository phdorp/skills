# 2. Blocks connect only through the connectors in Interfaces

## Status

proposed

## Context

Found in the code, unconfirmed. `System.mo` wires `Room` and `Thermostat` with `connect` on
the typed connectors of `Interfaces.mo`; `Room` and `Thermostat` use no other block's
connectors. Serves R-2 and QG-2 (swap a block without touching the rest). The dependency rule
is on the central list (`ADR-0001`). One deviation is found: `Thermostat` reads a package
constant, which the rule forbids; see ADR-0003.

## Decision

We will connect blocks only through the connectors in `Interfaces`, and no block will read
another block's parameters or constants.

## Consequences

`Thermostat`'s read of `HeatingLib.roomHeatCapacity` breaks this rule. Fixing it waits for
the architect's decision on ADR-0003. `System` names its components by concrete type; whether
that changes is a separate question for R-2.
