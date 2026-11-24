# 4. Dependency rule between blocks

## Status

proposed

## Context

*As found, unconfirmed.* Found in the imports of `pantry/`: `cli` imports `dates`, `store` and
`model`; `store` imports `model`; `dates` and `model` import no other pantry block. Serves R-4
(QG-2).

## Decision

We will let `cli` use `dates`, `store` and `model`; `store` use `model`; and `dates` and `model`
use no other pantry block. A new command uses the existing store API.

## Consequences

A new command changes `cli.py` and at most one new module, as R-4 requires. A change to the
dependency rule is a new ADR, because it changes which modules a command may touch.
