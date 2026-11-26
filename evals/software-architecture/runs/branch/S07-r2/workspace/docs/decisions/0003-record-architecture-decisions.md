# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Storage and its
crash safety must hold (R-2, QG-1), the program must run with only the Python standard library
(R-3, QG-2), ISBNs must be checked before storage (R-4, QG-3), and adding a command must stay
within `cli.py` and one new module (R-5, QG-5).

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk format: the JSON catalog file and its record shape (ADR 0001)
- import and export formats: none yet
- interfaces between blocks and the dependency rule: `cli` calls `catalog` and `isbn` and never
  touches the file; `catalog` and `isbn` do not import `cli`
- versioning of the CLI commands and of the catalog file format
- crosscutting conventions: error handling (messages to stderr, exit codes)
- third-party dependencies: none; standard library only (R-3)

Left to the building blocks (no ADR):

- helper functions inside a block
- argument parsing inside `cli`
- the internals of the ISBN check-digit algorithm
- test layout

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. ADR 0001 and ADR 0002
are accepted (legacy) and are on this list as the storage and ISBN decisions.
