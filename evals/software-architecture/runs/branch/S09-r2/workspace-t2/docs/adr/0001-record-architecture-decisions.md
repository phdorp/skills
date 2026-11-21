# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Pantry must not lose
an item to a crash (R-2, QG-2) and must run on the Python standard library alone (R-3, QG-3),
and a new command must stay within `cli.py` plus at most one module (R-4, QG-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage format: an append-only JSONL file with records `{op, name, expires}`, at `~/.pantry.jsonl` or the path in `PANTRY_FILE`;
- write durability: how a write becomes safe after a crash (R-2);
- building-block boundaries and the dependency rule: `cli` may use `store`, `model` and `dates`; `store` may use `model`; `model` and `dates` use no other block;
- CLI interface: commands, arguments and exit codes 0 (success), 1 (user error), 2 (bad usage);
- date input and convention: the ISO date and the relative forms `today`, `tomorrow`, `+Nd`, `+Nw`; calendar dates without time;
- third-party dependencies: none (R-3).

Left to the building blocks (no ADR):

- argparse usage and internal helpers inside a block;
- test layout and test helpers;
- error message wording.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
