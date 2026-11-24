# 0001. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. HeatingLib needs
the line drawn so that a room or controller variant can be swapped without touching the rest
(R-2, QG-1) and so that every model is checked in OpenModelica (R-3, QG-2). A controller that
reads another block's constant would break that swap silently, which is why the dependency
rule is on the list.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Interfaces between blocks: the connectors and signal types in `HeatingLib.Interfaces` are the
  contract every room and controller shares.
- Dependency rule: a block does not read another block's package constant; shared values pass
  through connectors or a parameter.
- Variant mechanism: how `System` takes a room or controller variant (`replaceable` components,
  or one composition per variant).
- Units: SI throughout (K, W, J/K, s); temperatures displayed in °C.
- Result format: the OpenModelica result file is the export format of a simulation.
- Third-party dependencies: OpenModelica is the required tool; no Modelica Standard Library is
  used yet.

Left to the building blocks (no ADR):

- parameter defaults inside a block;
- the layout of `tests/`.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. In particular,
the variant mechanism decides how QS-1 is met, so changes to `System` for variants wait for
that decision.
