# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Shelf must keep its catalog intact (R-2, QG-1), run with only the standard library (R-3), and let a new command touch only `cli.py` and one new module (R-5, QG-3).

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage format and write rule: one JSON file, written to a temporary file and renamed into place (ADR-0001; R-2).
- Dependency rule: `cli` calls `catalog` and `isbn`; only `catalog` reads or writes the file (R-5).
- CLI commands, options and exit codes, which users depend on (R-1).
- Error handling: validation messages go to stderr, exit code 1 (ADR-0002; R-4).
- Third-party dependencies: none (R-3).

Left to the building blocks (no ADR):

- Helper names inside a module, the `tests/` layout, the argparse structure inside `cli.py`.

## Consequences

Work that depends on a decision on the list waits until this ADR is accepted.
