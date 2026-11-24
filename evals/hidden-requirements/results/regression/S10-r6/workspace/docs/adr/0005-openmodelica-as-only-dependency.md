# 5. Depend on OpenModelica only, with no third-party Modelica library

## Status

proposed

## Context

Found in the code and the README: the only tool used is OpenModelica (`omc`), run by `tests/check.mos` and by the README. No model imports a third-party library, for example the Modelica Standard Library. This serves R-3 and QG-3: the checks run on OpenModelica alone.

## Decision

We depend on OpenModelica as the only tool, and on no third-party Modelica library.

## Consequences

Using any library needs its own ADR. The work of adopting a library waits until that ADR is accepted.

Question for the architect: keep OpenModelica as the only dependency?
