# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Crash-safe storage of pantry items (R-2, QG-1) and a runtime that needs only the Python standard library (R-3) set the storage format and the dependency rule.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage format: an append-only JSON Lines file at `~/.pantry.jsonl` (override with `PANTRY_FILE`), with `add` and `remove` records.
- Dependency rule: `cli` → `store` → `model`; `dates` is used by `cli`; `model` does no I/O.
- CLI versioning: command names, flags, date forms (ISO, `today`, `tomorrow`, `+Nd`, `+Nw`), and exit codes 0, 1 and 2.
- Error handling: user errors go to stderr with exit 1.
- Third-party dependencies: none (R-3).

Left to the building blocks (no ADR):

- Internal helpers, sort order, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. A change to the storage format or the CLI's command, flag or exit-code contract needs a new ADR that supersedes this one's entry.
