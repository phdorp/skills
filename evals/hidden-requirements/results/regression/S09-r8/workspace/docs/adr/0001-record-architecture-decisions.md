# 1. Record architecture decisions

## Status

accepted 2026-11-24

## Context

The architect decides the architecture; contributors and agents build it. pantry must not lose an item when the machine crashes (R-1, QG-1), and it must run with only the Python standard library (R-3, QG-3), so the storage format and the dependency rule are decided centrally.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- the storage format: the append-only JSON-lines file at `PANTRY_FILE` (default `~/.pantry.jsonl`) and its record schema (`add`, `remove`)
- the dependency rule: `cli` may use `store`, `dates` and `model`; `store` may use `model`; `model` and `dates` use nothing internal
- the error-handling convention: exit codes 0, 1 and 2, with messages on stderr
- the versioning of the file format: open; the records carry no version field today
- third-party dependencies: none

Left to the building blocks (no ADR):

- the argparse structure inside `cli`
- the date regex in `dates`
- the dataclass in `model`
- the test layout

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted. In particular, the fix for the lost-item bug (a record appended after a torn line is lost, against R-1) may change how records are written, so it waits for this ADR.
