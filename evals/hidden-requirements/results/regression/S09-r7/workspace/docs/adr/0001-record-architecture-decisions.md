# 1. Record architecture decisions

## Status

accepted 2026-11-24

## Context

The architect decides the architecture; contributors and agents build it. The product must
not lose an item when the machine crashes mid-write (R-2), must run with only the Python
standard library (R-3, QG-3), and must let a new command touch only `cli.py` and at most one
new module (R-4, QG-4). A goal for crash recovery (R-2) is still open, named here in words.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage format: an append-only JSON Lines file, replayed on read, at `PANTRY_FILE` or
  `~/.pantry.jsonl`;
- crash handling of the store (R-2): what a torn write is, and what a later append does after
  one;
- the record shape (`op`, `name`, `expires`) and the date formats accepted on input
  (`YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`, `+Nw`);
- the dependency rule: `cli` → `store` → `model`, with `dates` used by `cli`; a new command
  lives in `cli.py` plus at most one new module (R-4);
- error handling: exit code 0 on success, 1 on a user error, 2 on bad usage;
- versioning of the command line and of the file format: none yet;
- third-party dependencies: none (R-3).

Left to the building blocks (no ADR):

- internal helpers and the layout of the argument parser;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The recovery of
the architecture from the code waits for the approval of this ADR's text. The crash behaviour
of the current code (a torn last line, after which a later append is lost) is an open case
under R-2 until the crash-handling decision is accepted.
