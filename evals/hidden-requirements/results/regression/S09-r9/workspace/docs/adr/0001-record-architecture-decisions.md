# 0001. Record architecture decisions

## Status

accepted 2026-11-24

## Context

The architect decides the architecture; contributors and agents build it. The pantry must keep stored items through a crash mid-write (R-2), run with only the Python standard library (R-3), and keep a new command inside `cli.py` and at most one new module (R-4, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the on-disk format of the pantry file (JSON Lines, one record per line, append-only) and the write and recovery rule that keeps items through a crash (R-2);
- third-party dependencies: none; the standard library only (R-3);
- interfaces and the dependency rule between building blocks: `cli` may use `dates`, `store` and `model`; `store` may use `model`; no other block crosses (R-4, QG-3);
- the command-line contract: command names, arguments, and exit codes 0 (success), 1 (user error), 2 (bad usage);
- the date input formats the CLI accepts (`YYYY-MM-DD`, `today`, `tomorrow`, `+Nd`, `+Nw`) and the ISO 8601 dates stored in the file.

Left to the building blocks (no ADR):

- helpers and structure inside one module;
- test layout;
- parser internals.

## Consequences

Work that depends on a decision on this list waits until its ADR is accepted.
