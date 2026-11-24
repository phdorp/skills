# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. HeatingLib must
simulate a heated room over a day and show its temperature (R-1, QG-1), let a room or a
controller variant be swapped without touching the rest (R-2, QG-2), and keep every model
passing OpenModelica's checks (R-3, QG-3). A decision that crosses a block boundary, or fixes a
format, is expensive to change later, so it needs a record the architect has approved.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- The interfaces between blocks: the connectors in `Interfaces.mo` are the only way blocks
  connect. A block reads no constant of another block.
- Units and naming: SI types throughout, and the names of the public classes (`System`, `Room`,
  `Thermostat`) are fixed.
- The result format for R-1: a CSV result file, plus a PNG plot made from it.
- Third-party dependencies: the Modelica Standard Library only.

Left to the building blocks (no ADR):

- The equations inside one block.
- The parameter defaults of a block.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The current
`Room` and `Thermostat` read a package constant and so conflict with the interface decision
above; fixing that waits for this ADR's approval. QG-1 (the set-point offset) is a
building-block change inside `Thermostat` and is not on the list.
