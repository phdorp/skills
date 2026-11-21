# 9. Standard library only

## Status

proposed

## Context

Found in the code, not decided: every module in `pantry/` and `tests/` imports only the standard library. Serves R-3 (QG-3).

## Decision

We will use only the Python standard library, with no third-party package and no install step.

## Consequences

Installation stays a copy of the source tree. A richer command-line parser or a TOML reader is unavailable without a new ADR.

Question for the architect: keep the standard-library-only rule?
