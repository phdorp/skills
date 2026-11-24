# 3. Dependency rule between building blocks

## Status

proposed

## Context

Found in the code, in the imports of `pantry/*.py` (arc42 section 5). It serves R-4 (a new command touches only `cli.py` and at most one new module, QG-4), because the command logic sits in `cli` and the layers below it do not depend on it.

## Decision

We will let building blocks use only the blocks below:

- `__main__` may use `cli`.
- `cli` may use `dates`, `store` and `model`.
- `store` may use `model`.
- `dates` and `model` use nothing internal.
- `tests` may use any block.

## Consequences

A new command needs changes in `cli` only, unless it needs new storage behaviour (then `store`) or a new block. A block that imports `cli` would break this rule. Adding a block or a dependency edge needs a new ADR.
