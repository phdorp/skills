# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Shelf needs this line
drawn so that crash-safe storage (R-2, QG-1) and standard-library-only (R-3, QG-5) hold for every
change.

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage format: one JSON file, written to a temporary file and renamed into place (ADR 0001).
- Interfaces and dependency rule: `cli` calls `catalog` and `isbn`; nothing else reads the file;
  `catalog` does not depend on `cli`.
- CLI interface: command names, flags and output of `add`, `list` and `find` (R-1).
- Error handling: exit codes and stderr messages of the CLI.
- Third-party dependencies: none; standard library only (R-3).
- Command registration: how a command module plugs into `cli` (R-5).

Left to the building blocks (no ADR):

- Internal helpers, names inside one module, test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
