# 6. Use only the Python standard library

## Status

proposed

## Context

Found in the code: every import in `pantry/` is from the standard library (`argparse`,
`dataclasses`, `datetime`, `json`, `os`, `pathlib`, `re`, `sys`); the tests use only `unittest` and
the standard library. There is no packaging file for third-party dependencies. Serves R-3 (runs with
only the Python standard library).

## Decision

We will use no third-party packages. We will run on the Python standard library alone.

## Consequences

Adding any package requires a new ADR that supersedes this one. The minimum Python version is not
recorded anywhere in the code (see arc42 section 2).
