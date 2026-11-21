# 0004. Use only the Python standard library

## Status

proposed

## Context

Found in the imports of every module: `argparse`, `dataclasses`, `datetime`, `json`, `os`,
`pathlib`, `re`, `sys`. The tests use `unittest`. Serves R-3 and QG-3.

## Decision

We will use only the Python standard library, in the package and in its tests. No third-party
dependency is declared or installed.

## Consequences

Installation needs no pip step (QG-3). Richer date parsing, if ever needed, is written by hand.
The minimum Python version is an open question in section 2; the code needs Python 3.7 or later.
