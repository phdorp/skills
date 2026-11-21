# 0001. Record architecture decisions

## Status

accepted 2026-11-21

## Context

The architect decides the architecture; contributors and agents build it. Pantry must not lose
an item when the machine crashes mid-write (R-2, QG-1), must run with only the Python standard
library (R-3, QG-3), must keep each new command within `cli.py` and one new module (R-4, QG-4),
and must list expiring items correctly (R-1, QG-2).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage format: an append-only JSON Lines file, one record per line, replayed on read; the
  default path is `~/.pantry.jsonl`, overridable by `PANTRY_FILE` (R-2).
- Durability: each record is fsynced before a command reports success (R-2).
- Dependencies: the Python standard library only (R-3).
- Building-block interfaces and dependency rule: `cli` may use `dates` and `store`; `store` may
  use `model`; `model` uses nothing. Each new command adds at most one module (R-4).
- CLI interface: command names, arguments and exit codes (0 success, 1 user error, 2 bad usage)
  are versioned; changing them needs an ADR.
- Conventions: dates are ISO 8601 in the file and in output.

Left to the building blocks (no ADR):

- parsing internals in `dates.py`, helper names, test layout, output formatting details.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. Accepting this ADR
also unblocks recovering the as-is architecture from the code. Changes to the write path of the
storage format fall under the storage and durability items above.
