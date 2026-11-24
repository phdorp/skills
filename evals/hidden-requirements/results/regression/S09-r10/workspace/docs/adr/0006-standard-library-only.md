# 6. Use only the Python standard library

## Status

proposed

## Context

Found in the code, unconfirmed: every module imports only standard-library modules (`argparse`, `json`, `os`, `pathlib`, `dataclasses`, `datetime`, `re`, `sys`), and the repository has no requirements or packaging file. This decision is on the accepted list in ADR 0001 (third-party dependencies). It serves R-3 and QG-2 (installability).

## Decision

We will import only the Python standard library. We will not add a package manifest that lists third-party packages.

## Consequences

Any feature that needs a third-party package needs a new ADR, and R-3 would have to change first. Installation stays a matter of running `python3 -m pantry`.
