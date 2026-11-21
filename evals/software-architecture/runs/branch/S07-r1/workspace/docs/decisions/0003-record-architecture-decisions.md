# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. The product needs the
line drawn here so that the catalog survives crashes (R-2, QG-1), ISBNs are checked before storing
(R-4, QG-2), the program runs on the standard library alone (R-3, QG-3), and a new command changes
only cli.py and one new module (R-5, QG-4).

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format: one JSON file (ADR 0001);
- interfaces and the dependency rule: `cli` calls `catalog` and `isbn`; only `catalog` touches the
  file; a command module is wired in by `cli.py` only;
- third-party dependencies: none; standard library only (R-3);
- versioning of the CLI and the catalog file (the JSON has no version field today);
- crosscutting conventions: error output to stderr, exit code 1 on invalid input.

Left to the building blocks (no ADR):

- internal helpers and the structure inside one block;
- parsing internals and test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
