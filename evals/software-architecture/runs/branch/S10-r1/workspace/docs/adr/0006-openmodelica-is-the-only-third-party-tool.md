# 6. OpenModelica is the only third-party tool

## Status

proposed

## Context

Found in the code, not decided by the architect: `README.md` and `tests/check.mos` check the
library with `omc` (OpenModelica). No file imports the Modelica Standard Library. Serves R-3 and
QG-2: every model is checked with this tool.

## Decision

We check and simulate the library with OpenModelica, and the library uses no third-party
Modelica library.

## Consequences

R-3 depends on OpenModelica's checks. Adding the Modelica Standard Library later is a new
decision, recorded in its own ADR.
