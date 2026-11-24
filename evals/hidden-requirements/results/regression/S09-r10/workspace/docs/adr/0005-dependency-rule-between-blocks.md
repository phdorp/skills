# 5. Dependency rule between the blocks

## Status

proposed

## Context

Found in the code, unconfirmed: the imports in `pantry/__main__.py`, `cli.py`, `store.py`, `model.py` and `dates.py`. This decision is on the accepted list in ADR 0001 (dependency rule). It serves R-4 and QG-3 (a new command touches only `cli.py` and at most one new module).

## Decision

We will let `__main__` use `cli`; `cli` use `dates`, `store` and `model`; and `store` use `model`. `dates` and `model` use no other block of the product.

## Consequences

A new command stays within `cli.py` and at most one new module, as R-4 requires. A command that needs a new kind of record also changes `model.py` and `store.py`, which R-4 does not allow; that conflict is open for the architect, as set out at setup. Changing a dependency in this list needs a new ADR.
