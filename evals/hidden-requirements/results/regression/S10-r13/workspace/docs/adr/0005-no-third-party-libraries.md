# 5. No third-party Modelica libraries

## Status

proposed

## Context

Found in the code (no `uses` clause and no library imports in `HeatingLib/`), not decided by the architect. The checks must pass with OpenModelica (R-3, QG-2), and tooling is restricted to open-source tools (arc42 section 2).

## Decision

We will depend on no third-party Modelica library: the library uses only its own package, `HeatingLib`, and the Modelica language. The only tool is OpenModelica (`omc`).

## Consequences

The library stays self-contained and checks with OpenModelica alone. Using a library such as the Modelica Standard Library would be a decision for a new ADR.
