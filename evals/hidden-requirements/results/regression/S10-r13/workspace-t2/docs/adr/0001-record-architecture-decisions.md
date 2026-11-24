# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. A room or controller variant must be swappable without touching the rest (R-2, QG-1), and every model must check in OpenModelica without errors (R-3, QG-2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the interfaces between blocks: the connectors in the `Interfaces` package, and the dependency rule between blocks;
- blocks depend only on connectors and on parameters that `System` passes in; no block reads a package constant that another block also reads;
- units: SI in models (Kelvin); `degC` only for display (`Interfaces.Temperature`);
- naming and the library's package layout (`package.order`);
- third-party dependencies: none so far; only open-source tooling (see arc42 section 2).

Left to the building blocks (no ADR):

- parameter values and equations inside one model;
- test layout beyond the OpenModelica check script.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. Changing the coupling between `Room` and `Thermostat` (today both read `HeatingLib.roomHeatCapacity`) is such work.
