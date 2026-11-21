# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Crashes must not lose
the catalog (R-2, QG-2) and the product must run with only Python's standard library (R-5, QG-5),
so the storage format, the dependency rule and the command interface must be decided centrally.

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage format and atomic-write rule (ADR 0001, legacy);
- dependency rule: `cli` calls `catalog`, never the file; where the ISBN check lives (R-3, R-4);
- third-party dependencies: none, standard library only (R-5);
- versioning of the on-disk catalog file and of the CLI command surface;
- crosscutting error handling: messages to stderr and exit codes;
- how command modules register with the CLI (R-4).

Left to the building blocks (no ADR):

- internal helpers inside `isbn.py`;
- test layout;
- the format of listing output.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. The catalog's
on-disk format has no version field today; a change to it needs an ADR first.
