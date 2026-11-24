# 0004. Dependencies between building blocks point one way

## Status

proposed

## Context

As found in the code, not yet decided by the architect: `pantry/cli.py:6-7` imports `dates`, `store` and `model`; `pantry/store.py:6` imports `model`; `pantry/model.py` and `pantry/dates.py` import only the standard library; `pantry/__main__.py:3` imports `cli`. This serves R-4 (a new command touches only `cli.py` and at most one new module) and QG-3 (modularity). It is a central decision under ADR-0001.

## Decision

We allow these dependencies between blocks, and no others:

- `__main__` may use `cli`;
- `cli` may use `dates`, `store` and `model`;
- `store` may use `model`;
- `dates` and `model` use no block of the package.

## Consequences

A new command changes `cli.py` and at most one new module. A new module that reads the pantry file goes through `store`. A change to this rule needs a new ADR.
