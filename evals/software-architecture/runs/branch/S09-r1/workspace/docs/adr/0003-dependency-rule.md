# 3. Dependency rule between building blocks

## Status

proposed

## Context

Found in the code, not decided by anyone yet: the imports in `pantry/cli.py`, `pantry/store.py`, `pantry/model.py` and `pantry/dates.py`. It is a decision on the list in ADR 0001 (interfaces between building blocks). It serves the requirement that a new command touches only `cli.py` and at most one new module (R-4, QG-3).

## Decision

We will keep the dependencies between building blocks as they are: `cli` may use `store`, `model` and `dates`; `store` may use `model`; `model` and `dates` use no other pantry module; `model` does no I/O.

## Consequences

A new command fits the rule when its logic lives in `cli.py` or one new module. A command that needs a new stored query changes `store.py` as well, which R-4 does not allow; that case needs the architect's decision. Changing the rule needs a superseding ADR.
