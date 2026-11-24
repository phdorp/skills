# 4. Use only the Python standard library

## Status

proposed

## Context

Found in the code, not decided: every import in `pantry/` and `tests/` is from the standard
library. This serves R-3, which has no quality goal yet (arc42 section 1: open).

## Decision

We will use only the Python standard library, in the package and in its tests.

## Consequences

The tool needs no install step, and the tests run with `unittest`, as the README states. Adding a
third-party dependency needs a new ADR, because the central list makes it a central decision.
