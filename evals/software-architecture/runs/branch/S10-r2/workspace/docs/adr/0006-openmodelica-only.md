# 6. OpenModelica is the only tool; the library uses no external library

## Status

proposed

## Context

Found in the code, not decided: `README.md` and `tests/check.mos` run the library with
OpenModelica (`omc`); no source file imports a Modelica library. Serves R-3, QG-3.

## Decision

OpenModelica is the tool for checking and simulating HeatingLib. The library uses no external
Modelica library.

## Consequences

Code that needs another library waits for a new ADR. Checks depend on OpenModelica's behaviour
(see QS-2, where the version is open).
