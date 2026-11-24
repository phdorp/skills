# 6. Standard library only

## Status

proposed

## Context

Found in the code, not decided by the architect: every module imports only the Python standard library (`argparse`, `dataclasses`, `datetime`, `json`, `os`, `pathlib`, `re`, `sys`; `unittest` in the tests). The constraint is confirmed in arc42 section 2 and serves no R-ID directly. Third-party dependencies are on the approved ADR-0001 list.

## Decision

We use only the Python standard library. No third-party package is added to the product.

## Consequences

Installing pantry needs no package manager. Adding any library needs a superseding ADR.
