# 3. Dependency rule between the building blocks

## Status

proposed

## Context

Found in the code: `pantry/cli.py:6-7` imports `dates`, `store` and `model`; `pantry/store.py:6`
imports `model`; `pantry/__main__.py:3` imports `cli`; `dates` and `model` import nothing from
pantry. Serves R-4 (a new command touches only cli.py and at most one new module) and QG-1.

## Decision

We will let `__main__` use `cli`; `cli` use `store`, `dates` and `model`; and `store` use `model`.
`dates` and `model` use nothing else in pantry.

## Consequences

The approved central list (ADR 0001) says `cli` uses `store` and `dates`, with no other edges. The
code also has `cli` → `model`, which that list does not name. The architect must decide whether the
edge stays, which changes this ADR or the central list. Until then, a new command may use `model`
from `cli`.
