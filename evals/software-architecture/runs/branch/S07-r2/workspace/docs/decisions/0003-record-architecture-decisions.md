# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. The catalog must
survive crashes mid-write (R-2, QG-1) and run with only the Python standard library (R-3, QG-5),
which fixes the storage format and the dependency rule.

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk format: one JSON file (ADR 0001);
- import and export formats: none yet; any future format gets an ADR;
- interfaces between building blocks and the dependency rule: `cli` may use `catalog` and `isbn`;
  `catalog` may use `isbn`; `isbn` uses nothing in the project; no block imports `cli`;
- versioning of the CLI and of the catalog file format;
- crosscutting conventions: errors are printed to stderr and return exit code 1; naming;
- third-party dependencies: none; standard library only (R-3).

Left to the building blocks (no ADR):

- internal helpers and the structure inside one block;
- test layout;
- argument parsing details.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
