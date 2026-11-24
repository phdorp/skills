# 6. Dependency rule between building blocks

## Status

proposed

## Context

*As found, unconfirmed.* Found in the imports of every module under `pantry/`. Serves R-4 (QG-3): a change to one block has a bounded reach, so a new command touches only `cli.py` and at most one new module.

## Decision

We will allow these uses: `__main__` uses `cli`; `cli` uses `dates`, `store` and `model`; `store` uses `model`. `model` and `dates` use only the standard library. No block imports `cli`, and `model` and `dates` do not import `store`.

## Consequences

`store.py`, `model.py` and `dates.py` stay unchanged when a command is added (QS-3). A command that needs a new storage operation must still change `store.py`, which conflicts with R-4 when that happens; that case is open and needs its own decision.
