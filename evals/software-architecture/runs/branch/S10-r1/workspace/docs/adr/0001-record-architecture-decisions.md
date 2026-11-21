# 1. Record architecture decisions

## Status

accepted 2026-11-21

## Context

The architect decides the architecture; contributors and agents build it. HeatingLib must keep its blocks swappable without touching the rest (R-2, QG-2) and every model must check in OpenModelica (R-3, QG-3), so the decisions that cross block boundaries are made centrally. The product itself is the simulation of a heated room over a day (R-1).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Connector types and the dependency rule between blocks: blocks are connected only through the connectors in `Interfaces`, and no block reads another block's internals.
- Shared parameters and constants: whether blocks may read package constants such as `roomHeatCapacity`. Today `Room` and `Thermostat` both do, which is the coupling against R-2.
- Units: SI, with Kelvin internally and degC for display only.
- Result output format: the `.mat` file that `simulate` writes.
- Third-party libraries: none in use yet; adding one is central.

Left to the building blocks (no ADR):

- Equations inside `Room` and `Thermostat`.
- Parameter defaults.
- Test file layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. In particular, removing the constant coupling between `Room` and `Thermostat` waits for a decision on shared constants.
