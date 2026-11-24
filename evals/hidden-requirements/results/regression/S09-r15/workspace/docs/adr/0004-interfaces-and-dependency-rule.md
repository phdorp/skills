# 4. Interfaces and dependency rule between building blocks

## Status

proposed

## Context

A new command touches only cli.py and at most one new module (R-3, QG-3, QS-3), and interfaces between building blocks are decided centrally (ADR 0001). Found from the imports in `pantry/`.

## Decision

The blocks depend on each other as follows. `__main__` uses `cli`. `cli` uses `dates`, `store` and `model`. `store` uses `model`. `dates` and `model` use no project module. Blocks talk through plain function calls, the `Item` value, and record dictionaries. No block imports `cli`.

## Consequences

A new command that reuses existing store and model calls changes only `cli.py`. A new storage operation changes `store.py` and `model.py` as well, which bears on R-3 (QG-3). The dependency rule is not enforced by any test.
