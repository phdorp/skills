# 5. A new command touches cli.py and one new module

## Context

Each new command should be cheap to add. The file format and the storage rules are shared, so
they must not be spread across command code.

## Decision

- `cli.py` owns argument parsing and dispatch: one subparser and one branch per command.
- A command's logic goes in one new module under `shelf/`. That module may use the public
  `catalog.load` and `catalog.save`. Storage stays in `catalog.py`.
- No other module changes when a command is added.

## Consequences

- If a command needs a storage operation that `catalog` does not offer, the new module can build
  it from `load` and `save`. If several commands need the same operation, move it into `catalog`
  in a separate change.
- Dispatch in `cli.main` is an `if`/`else` chain. It stays readable at the current size. Past
  about five commands, switching to a table of command handlers is the next step.
- The existing `add`, `list` and `find` logic is still in `cli.py`, so they are not examples of
  the one-new-module pattern.
