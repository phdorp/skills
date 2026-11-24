# 4. System composes the concrete blocks Room and Thermostat

## Status

proposed

## Context

Found in the code: `HeatingLib/System.mo` declares `Room room;` and `Thermostat thermostat;` as
concrete types, with no `replaceable` or `partial` declarations. Decision on the accepted list:
"Replaceability: which blocks are swappable, and the interface a variant must meet". This is found
in the code and works against R-2 (QG-2): R-2 requires that the room or the controller can be
swapped without touching the rest, which these fixed types do not allow.

## Decision

We compose `System` from the concrete types `Room` and `Thermostat`; no block is replaceable.

## Consequences

Swapping a variant means editing `System`. R-2 is not met while this decision stands. Meeting R-2
needs a superseding ADR that makes the blocks replaceable, which this ADR stays `proposed` until
the architect decides on it.
