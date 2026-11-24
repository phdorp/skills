# 7. Standard library only

## Status

proposed

## Context

Found in the code, unconfirmed: every module imports only the Python standard library
(`argparse`, `dataclasses`, `datetime`, `json`, `os`, `pathlib`, `re`, `sys`). It serves R-3
and goal QG-3 (installability).

## Decision

We will use only the Python standard library. No third-party package is imported or required.

## Consequences

The tests also use only the standard library (`unittest`). Any feature that would need a
package waits for a new ADR that supersedes this one.
