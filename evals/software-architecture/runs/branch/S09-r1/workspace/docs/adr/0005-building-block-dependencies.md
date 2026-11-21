# 0005. Building-block dependencies

## Status

proposed

## Context

Found in the imports of `pantry/`. Serves R-4 (a new command touches only `cli.py` and at most
one new module) and QG-4.

## Decision

We will keep these dependencies between building blocks:

- `cli` may use `dates`, `store` and `model`.
- `store` may use `model`.
- `dates` and `model` use no other pantry module.
- `__main__` uses only `cli`.

A new command adds at most one module.

## Consequences

Adding a command changes `cli.py` and at most one new module. `cli` imports `model` to build
`Item` objects. The text of ADR-0001 names only `dates` and `store` for `cli`. ADR-0001 is
accepted as written and is not changed here; whether `cli` may use `model` is the architect's
decision, and a change to it needs a new ADR.
