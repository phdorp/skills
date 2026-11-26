# 5. Block dependency rule

## Status

proposed

## Context

Found in the code (the imports of `pantry/`), not decided by the architect. The interfaces between building blocks and the dependency rule between them are on the list of decisions made centrally (ADR-0001). It serves R-4 (a new command touches only `cli.py` and at most one new module; QG-3 modifiability).

## Decision

As found: `__main__` uses `cli`. `cli` uses `store`, `dates` and `model`. `store` uses `model`. `model` and `dates` use nothing else in the package.

## Consequences

A new command changes `cli.py` and at most one new module, as R-4 requires. A change to the pantry file format touches `store` and `model`, which ADR-0002 governs.
