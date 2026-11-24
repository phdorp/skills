# 5. Dependency rule between modules

## Status

proposed

## Context

Found in the code, unconfirmed: `pantry/cli.py` imports `dates`, `store` and `model`;
`pantry/store.py` imports `model`; `model` and `dates` import nothing from the package;
`pantry/__main__.py` imports `cli`. Requirement R-4 (a new command touches only `cli.py` and at
most one new module) and goal QG-4 are the reasons this rule matters.

## Decision

We will keep the import graph as found: `cli` may use `dates`, `store` and `model`; `store`
may use `model`; `model` and `dates` use no other module of the package.

## Consequences

`cli` reads `model` directly as well as through `store`, which the shorter rule
`cli` → `store` → `model` in ADR-0001's list does not show. The `remove` command edits both
`cli.py` and `store.py`, so the code does not meet R-4's bound for that command. The architect
decides whether to keep the graph, tighten it, or accept the difference.
