# 1. Record architecture decisions

## Status

accepted 2026-11-24

## Context

The architect decides the architecture; contributors and agents build it. The tool must
keep every item it has acknowledged through a crash (R-2, QG-1), run with only the Python
standard library (R-3, QG-2), and let each new command change only `cli.py` and at most one
new module (R-4, QG-3), with the core job of adding and listing expiring items first (R-1).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage engine and on-disk format: the append-only JSON Lines file at `PANTRY_FILE`
  (default `~/.pantry.jsonl`), in which each acknowledged write is durable (R-2, QG-1).
- The record format: `add` and `remove` operations, item names as strings, expiry dates as
  ISO 8601 calendar dates. Treated as a file format: files written today stay readable.
- The CLI interface: command names, arguments and exit codes 0, 1 and 2.
- The dependency rule: `cli` uses `dates`, `store` and `model`; `store` uses `model`; `dates`
  and `model` use no other block (R-4, QG-3).
- Third-party dependencies: none; the standard library only (R-3, QG-2).
- Date conventions: local calendar dates without a time; the input forms users type
  (`YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`, `+Nw`).

Left to the building blocks (no ADR):

- Internal helper functions, argparse wiring, the date pattern, the output sort order, and
  the test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. That includes
any change to how `store` writes or repairs the file (R-2), and recovering the architecture
from the code (`setup-architecture`, section 4).
