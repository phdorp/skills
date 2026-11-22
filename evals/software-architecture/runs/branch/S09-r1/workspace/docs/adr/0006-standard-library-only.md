# 6. Standard library only

## Status

proposed

## Context

Found in the code, not decided by anyone yet: every import in `pantry/` and `tests/` is from the Python standard library, and there is no package manifest. It is a decision on the list in ADR 0001 (third-party dependencies). It serves the requirement that the program runs with only the Python standard library (R-3).

## Decision

We will use only the Python standard library, at runtime and in the tests.

## Consequences

No install step is needed to run the tool. The minimum Python version is not yet measured (QG-3 is open), so the floor the code needs (Python 3.7 or later, from `dataclasses` and `date.fromisoformat`) is not a commitment. Adding a third-party package needs a superseding ADR.
