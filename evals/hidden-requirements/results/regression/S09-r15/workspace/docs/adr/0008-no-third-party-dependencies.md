# 8. No third-party dependencies

## Status

proposed

## Context

The program runs with only the Python standard library (section 2 of `docs/architecture/arc42.md`). Third-party dependencies are a central decision (ADR 0001), and portability is an open quality question (section 1). Found from the imports in `pantry/` and `tests/`.

## Decision

The program imports only the Python standard library and declares no dependencies. The repository has no requirements or packaging file.

## Consequences

Any third-party dependency needs its own ADR, which supersedes this one. Portability remains open until the architect gives its measure.
