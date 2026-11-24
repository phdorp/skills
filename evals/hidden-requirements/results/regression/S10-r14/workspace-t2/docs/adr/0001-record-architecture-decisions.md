# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Replacing the room
or the controller without touching the rest (R-2, QG-2) and checking every model in OpenModelica
without errors (R-3, QG-3) depend on the interfaces, the dependency rule and the conventions
fixed here.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Interfaces between blocks: the connector and type definitions in `HeatingLib.Interfaces`, and
  the dependency rule: which blocks may read another block's constants or parameters.
- Replaceability: which blocks are swappable, and the interface a variant must meet.
- Units: SI inside the library, temperatures in K, °C for display only.
- Versioning: renaming or removing public classes (`Room`, `Thermostat`, `System`).
- Third-party dependencies: OpenModelica as the only tool.
- Output format: the simulation result format, if other tools will read it.

Left to the building blocks (no ADR):

- Equations inside one block, parameter names, and the layout of the test script.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
