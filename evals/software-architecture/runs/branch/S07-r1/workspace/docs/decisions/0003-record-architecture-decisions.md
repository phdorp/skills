# 3. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. The catalog must
survive crashes (R-2, QG-1), and the tool must run with only the standard library (R-3, QG-3),
so the central decisions must be recorded where builders will find them before they change the
code.

## Decision

We record architecture decisions as ADRs in `docs/decisions/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage format: one JSON file (ADR 0001). Its versioning is open: the file has no version field.
- Interfaces and the dependency rule: cli calls catalog and isbn; only catalog touches the file.
- Versioning of the file format and of the CLI commands.
- Canonical ISBN form, hyphens kept or stripped: open. `find` currently compares the raw strings.
- Error handling: messages go to stderr, with exit code 1, as cli.py does now.
- Third-party dependencies: none (R-3).

Left to the building blocks (no ADR):

- Internal helpers, the argparse structure, and the test layout.

## Consequences

Work that depends on a decision on this list waits until its ADR is accepted. ADRs 0001 and 0002
are legacy-accepted and their decisions are unchanged. Changing the ISBN form and the file-format
versioning both wait for the architect's decision.
