# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Pantry items must survive a crash mid-write (R-2, QG-1), a new command must touch only `cli.py` and at most one new module (R-3, QG-3), and the product must run with only the Python standard library (arc42 section 2). Correct expiry listing from the command line (R-1, QG-2) depends on the same date and file decisions.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage engine and on-disk data format: the append-only JSON Lines file `~/.pantry.jsonl`, its add and remove records, and how a write stays crash-safe (R-2);
- interfaces between `cli`, `store`, `model` and `dates`, and the dependency rule between them (R-3);
- versioning of the file format and of the CLI: command names and exit codes 0, 1 and 2;
- error handling: user errors exit 1, bad usage exits 2, messages go to stderr;
- date formats: what users type and what the file stores;
- third-party dependencies: none (arc42 section 2).

Left to the building blocks (no ADR):

- parsing internals in `dates.py`;
- helper names and structure inside one module;
- test layout;
- argparse details.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. That includes any change to how items are written to the file, such as a fix for a torn last line.
