# 3. One-way module dependencies

## Status

proposed

## Context

Found in the code, not decided by the architect: `pantry/__main__.py` uses `cli`; `cli` uses `dates`, `store` and `model`; `store` uses `model`; `model` and `dates` use no pantry module. There are no cycles. This serves R-3 (QG-3) and is an interface and dependency rule under ADR-0001.

## Decision

We keep the module dependencies one-way, as found: `__main__` → `cli` → `dates`, `store`, `model`; `store` → `model`; `model` and `dates` use no pantry module. A new command is added in `cli`. A new module may be added once, as R-3 allows.

## Consequences

A command that only reads items needs no change outside `cli`. A command that needs a storage operation `store` does not yet have needs a change to `store`, which R-3 does not allow, so it needs its own ADR first.
