# 7. Standard library only

## Status

proposed

## Context

Found in the code: every module imports only the Python standard library (`argparse`, `dataclasses`,
`datetime`, `json`, `os`, `pathlib`, `re`, `sys`; the tests add `unittest`). It serves R-3.

## Decision

pantry uses only the Python standard library, at run time and in its tests. There is no third-party
dependency, no requirements file and no packaging metadata.

## Consequences

Installation is not needed: any Python 3 can run the program from the source tree. The minimum
Python version is not declared; the code needs at least Python 3.7 (by reading: dataclasses, f-strings
and `date.fromisoformat`).
