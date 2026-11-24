# 3. Dependency rule between the pantry modules

## Status

proposed

## Context

Found in the code, not decided: the imports in `pantry/`. R-4 (QG-3, QS-3) requires a new
command to touch only `cli.py` and at most one new module.

## Decision

We will keep the dependencies the code has: `cli` may use `dates`, `store` and `model`; `store`
may use `model`; `dates` and `model` use no other module of the package; `__main__` may use
`cli` only.

## Consequences

`__main__` → `cli` is an edge that ADR 0001's list ("no other edges between modules") does not
name; this ADR names it, and the architect decides whether it stays. A new command that needs a
change to `store.py` or `model.py` breaks R-4: the tension noted at setup.
