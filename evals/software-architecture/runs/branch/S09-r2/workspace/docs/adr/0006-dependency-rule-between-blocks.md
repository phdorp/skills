# 6. Dependency rule between blocks

## Status

proposed

## Context

Found in the code, not decided: the imports in `pantry/`. `cli` imports `dates`, `store` and `model`. `store` imports `model`. `model` and `dates` import only the standard library. Serves R-4 (QG-2).

## Decision

We will let `cli` use `dates`, `store` and `model`; `store` use `model`; `model` and `dates` use no other block; and `__main__` use only `cli`.

## Consequences

A new command touches `cli.py` and at most one new module, as R-4 requires. A change that needs a new store operation touches `store.py`, which R-4 forbids unless the store API stays generic. This is the tension named in the proposal.

Question for the architect: keep this dependency rule?
