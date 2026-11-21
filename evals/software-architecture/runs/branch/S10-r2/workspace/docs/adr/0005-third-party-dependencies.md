# 5. Third-party dependencies

## Status

proposed

## Context

Found in the code, not decided by the architect: `README.md` and `tests/check.mos` use
OpenModelica (`omc`) as the only tool. No file imports another library, and the Modelica
Standard Library is not used. This is on the accepted list ("Third-party dependencies"). It
serves R-3 and QG-3.

## Decision

We check and simulate HeatingLib with OpenModelica (`omc`), and we depend on no other library.

## Consequences

Any other Modelica tool would need the checks to be ported. Adding a library, such as the
Modelica Standard Library, waits for this ADR's acceptance.
