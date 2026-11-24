# 6. The library is written in Modelica and checked with OpenModelica only

## Status

proposed

## Context

Found in the code: all sources are Modelica (`HeatingLib/*.mo`); `README.md` and `tests/check.mos`
run them with `omc`, the OpenModelica compiler. No external Modelica library is used. Decision on
the accepted list: "Third-party dependencies: OpenModelica as the only tool". It serves R-3
(QG-3): every model is checked with this one tool.

## Decision

We write the library in Modelica and check and simulate it with OpenModelica only.

## Consequences

Checks and simulations depend on the OpenModelica version installed. Using another Modelica
library or tool would need its own ADR.
