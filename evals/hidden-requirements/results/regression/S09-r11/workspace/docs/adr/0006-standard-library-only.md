# 6. Standard library only

## Status

proposed

## Context

*As found, unconfirmed.* Found in the imports of every module and test: only `argparse`, `json`,
`os`, `re`, `sys`, `dataclasses`, `datetime`, `pathlib`, `io`, `contextlib`, `tempfile` and
`unittest` are used. Serves R-3 (QG-3).

## Decision

We will use only the Python standard library, and support Python 3.9 or later.

## Consequences

The 3.9 floor is the architect's confirmed constraint; no test checks it. Adding any
third-party package is a new ADR.
