# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Pantry must not lose an item when the machine crashes mid-write (R-2, QG-1), must run with only the Python standard library (R-3, QG-3), and must keep a new command within `cli.py` plus at most one new module (R-4, QG-2). Storage and the CLI interface are shared by all of these, so they need one decision each (R-1, QG-4).

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage: a per-user JSON Lines file, `~/.pantry.jsonl` (overridable with `PANTRY_FILE`), holding append-only add and remove records that are replayed on read.
- Record format: `{"op", "name", "expires"}`, with `expires` as an ISO date.
- Date input: ISO dates, `today`, `tomorrow`, `+Nd`, `+Nw`.
- CLI interface: commands `add`, `list --soon DAYS`, `remove`; exit codes 0 for success, 1 for a user error, 2 for bad usage.
- Dependency rule: `cli` may use `store`, `model` and `dates`; `store` may use `model`; `model` and `dates` use no other block.
- Crash safety: each append is flushed and fsynced; a line that does not parse is skipped on read.
- Error handling: user errors are reported on stderr with a message naming the input.
- Third-party dependencies: none; standard library only.

Left to the building blocks (no ADR):

- Test layout and helper functions inside a module.

## Consequences

Work that depends on a decision on the list waits until this ADR is accepted. A change to storage, the record format or the CLI interface is a new ADR.

Because a line that does not parse is skipped without a warning, a corrupt record in the middle of the file loses its item silently. Changing that is a new ADR.
