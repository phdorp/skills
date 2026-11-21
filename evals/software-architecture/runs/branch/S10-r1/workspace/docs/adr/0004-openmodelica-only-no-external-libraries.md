# 4. OpenModelica is the only tool; no external Modelica library

## Status

proposed

## Context

Found in the code, not decided by the architect: `README.md` and `tests/check.mos` build and check
the models with `omc`, and `package.mo` has no `uses` annotation, so no external Modelica library
is imported. This is a third-party dependency of the kind ADR 0001 lists as decided centrally. It
serves the checks in OpenModelica (R-2, QG-1).

## Decision

We build and check the library with OpenModelica only, and use no external Modelica library.

## Consequences

Using another Modelica tool, or importing a library such as the Modelica Standard Library, changes
this decision and needs a new ADR.
