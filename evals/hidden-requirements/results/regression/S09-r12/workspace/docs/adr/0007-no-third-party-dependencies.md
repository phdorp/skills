# 7. No third-party dependencies

## Status

proposed

## Context

*As found, unconfirmed.* Found in the imports of `pantry/` and `tests/`, and in the absence of any packaging or requirements file. Serves R-3 (QG-2): the program runs with nothing installed.

## Decision

We will use only the Python standard library, in the program and in its tests. We will not add a requirements file or a package dependency.

## Consequences

Any feature that a library would make simpler is written with the standard library instead. Adding a third-party package is a new decision that replaces this one, and needs its own ADR.
