# 1. Record architecture decisions

## Status

accepted 2026-11-24

## Context

The architect decides the architecture; contributors and agents build it. Pantry must keep every add or remove it acknowledged through a crash (R-2, QG-1) and run with only the Python standard library (R-3, QG-2), while a new command touches only `cli.py` and at most one new module (R-4, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the pantry file format: one JSON record per line, `add` and `remove` events replayed in order, at `PANTRY_FILE` or `~/.pantry.jsonl`;
- the write rule that makes R-2 hold, and how a torn last line is handled;
- the CLI interface: command names, arguments, exit codes 0, 1 and 2, and the output format of `list`;
- the accepted date forms: `2026-11-25`, `today`, `tomorrow`, `+3d`, `+2w`;
- the dependency rule: `cli` may use `store`, `model` and `dates`; the others do not import `cli`;
- third-party dependencies: none (R-3).

Left to the building blocks (no ADR):

- helper functions inside a module;
- the test layout;
- argparse wiring inside `cli.py`.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
