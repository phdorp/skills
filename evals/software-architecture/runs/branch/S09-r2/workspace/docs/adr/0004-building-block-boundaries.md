# 4. Building-block boundaries and dependency rule

## Status

proposed

## Context

Found in the code, unconfirmed: the imports of `pantry/cli.py`, `store.py`, `model.py`, `dates.py`. Serves R-4 (QG-4). `cli` imports `dates`, `store` and `model`. `store` imports `model`. `model` and `dates` import only the standard library.

## Decision

We will keep the blocks in this dependency order: `cli` may use `dates`, `store` and `model`; `store` may use `model`; `model` and `dates` use no other block. Only `store` reads or writes the pantry file.

## Consequences

A new command changes `cli.py` and, if it needs new storage, `store.py`; a new block must fit this order. The rule is what makes R-4 hold, so breaking it needs a new ADR.

Question for the architect: keep this dependency rule?
