# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. The catalog must
survive crashes (R-2, QG-2) and run with only the standard library (R-3, QG-4), and a wrong
ISBN must never be stored (R-4, QG-3). Those three forces decide which choices are central.

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk format, including a format version field in the catalog file (none exists yet);
- the dependency rule: `cli` calls `catalog` and `isbn`, never the file directly;
- versioning of the CLI commands;
- crosscutting conventions: error reporting (stderr and exit codes, as in `cli.py` today);
- third-party dependencies (standard library only, per R-3).

Left to the building blocks (no ADR):

- internal helpers and the structure inside one block;
- the test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
