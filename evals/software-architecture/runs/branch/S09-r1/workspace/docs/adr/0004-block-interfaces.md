# 4. Interfaces between the building blocks

## Status

proposed

## Context

Found in the code: `pantry/store.py:33-42` defines `add(item)`, `remove(name)` and `items()`;
`pantry/model.py:6-16` defines the `Item(name, expires)` record with `to_record()` and the
`removal(name)` record; `pantry/model.py:19` defines `replay(records)`; `pantry/dates.py:8` defines
`parse(text, today=None)`. Serves R-4 (a new command touches only cli.py and at most one new module)
and QG-1.

## Decision

We will expose the store to other blocks only through `add`, `remove` and `items`, and pass items
between blocks as `Item` records. We will expose `dates.parse` as the only date-text entry point.

## Consequences

A change to the `Item` record or to the record shape in `model.py` reaches `store.py` and every
caller of `items()`. A new command that needs only these functions stays inside cli.py.
