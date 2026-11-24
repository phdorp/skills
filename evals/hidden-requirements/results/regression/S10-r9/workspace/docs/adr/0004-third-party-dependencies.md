# 4. Third-party dependencies: OpenModelica only

## Status

proposed

## Context

Found in the code, not decided by the architect: no model or `package.mo` uses an external
library (no `uses` annotation, no import), and `README.md` names OpenModelica (`omc`) as the
only tool (`omc tests/check.mos`). It serves R-3 and QG-2: every model is checked with that
tool. This is the "Third-party dependencies" item of ADR-0001.

## Decision

We will depend on OpenModelica as the only required tool, and use no external Modelica library.

## Consequences

Models cannot use the Modelica Standard Library. A block that needs one waits for a new ADR.
