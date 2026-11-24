# 6. Dependency rule between the modules

## Status

proposed

## Context

Found in the imports of `pantry/`: `__main__` imports `cli`; `cli` imports `dates`, `store` and
`model`; `store` imports `model`; `dates` and `model` import no other pantry module. It serves R-4
(QG-2): a new command should touch `cli.py` and at most one new module.

## Decision

`__main__` may use `cli`. `cli` may use `store`, `dates` and `model`. `store` may use `model`.
`model` and `dates` do no file access, and `dates` depends on no other pantry module.

## Consequences

A new read-only command needs changes in `cli.py` only. A command that changes stored records
needs a new record kind in `model.py` and changes in `store.py` as well, which is two modules
beyond `cli.py`. That strains R-4 (arc42 section 11). The rule as found also lets `cli` use
`model` directly, which ADR 0001's list does not mention; the architect should confirm it.
