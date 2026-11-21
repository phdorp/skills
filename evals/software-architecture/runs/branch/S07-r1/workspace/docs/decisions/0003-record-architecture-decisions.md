# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. The line between
the two must let the catalog survive crashes (R-2, QG-1) and work with only Python's standard
library (R-3, QG-3), and keep a new command to `cli.py` and one module (R-5, QG-4).

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage format and write rule of the catalog file (ADR 0001);
- the boundary between `cli` and `catalog`: `cli` calls `catalog` and never touches the file (README);
- where ISBNs are checked (ADR 0002);
- the CLI's command names and flags, as an interface other people's scripts may depend on;
- crosscutting conventions: error output and exit codes;
- third-party dependencies: none; standard library only (R-3).

Left to the building blocks (no ADR):

- internal helpers, the structure inside one module, and the test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
