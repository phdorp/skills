# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. The catalog must
survive a crash mid-write (R-2, QG-1) and a book's ISBN must be checked before it is stored
(R-4, QG-2), with only the Python standard library (R-3).

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the catalog's on-disk format (ADR 0001) and whether it gets a version field;
- the file location and the `SHELF_FILE` override;
- the CLI surface: command names, flags, and the output line format;
- the dependency rule: `cli` calls `catalog` and `isbn`; nothing calls the file directly;
- where ISBN validation is enforced;
- ISBN normalisation: stored as typed, or hyphens removed;
- error handling: messages to stderr, exit code 1;
- third-party dependencies: none (R-3).

Left to the building blocks (no ADR):

- helper functions inside a block, the test layout, the argparse structure.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
