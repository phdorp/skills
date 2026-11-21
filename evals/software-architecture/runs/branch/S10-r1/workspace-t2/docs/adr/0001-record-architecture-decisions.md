# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. HeatingLib must
stay checkable on every change (R-2, QG-1) and let a room or a controller be replaced without
touching the rest (R-3, QG-2), so the choices that cross block boundaries need a central record.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Blocks connect only through the connector types in `Interfaces`; only `System` names concrete
  blocks.
- A block gets a value owned by another block through a connector or a parameter set in
  `System`, never by reading another block's package constant.
- Units: SI, with temperatures stored in K and displayed in °C.
- The output format of the temperature trace (R-1).
- Third-party dependencies: OpenModelica as the only tool.
- Versioning of public model and connector names, if other projects will use the library.

Left to the building blocks (no ADR):

- Equations inside a block, parameter defaults, the layout of `tests/`, and `package.order`.

## Consequences

Work that depends on a decision on the list above waits until its ADR is accepted. The
current coupling through `HeatingLib.roomHeatCapacity` contradicts the second item and must
change once that item is accepted.
