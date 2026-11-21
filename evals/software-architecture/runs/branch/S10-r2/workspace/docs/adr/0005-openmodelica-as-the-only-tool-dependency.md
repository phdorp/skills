# 5. OpenModelica is the only tool dependency

## Status

proposed

## Context

Found in the code, unconfirmed. `README.md` and `tests/check.mos` run the library with `omc`
(OpenModelica). The code imports no Modelica library; the Modelica Standard Library is not
used. Serves R-3 and QG-3 (every model checks in OpenModelica). Third-party dependencies are
on the central list (`ADR-0001`).

## Decision

We will simulate and check the library with OpenModelica, and add no Modelica library without
a new ADR.

## Consequences

Adding a library, or a second tool, needs its own ADR first. The check script is a building
block of its own (arc42 section 5) and is not decided here.
