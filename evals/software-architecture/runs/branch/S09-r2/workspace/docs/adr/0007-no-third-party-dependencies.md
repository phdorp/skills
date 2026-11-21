# 7. No third-party dependencies

## Status

proposed

## Context

Found in the code, unconfirmed: all imports in `pantry/` (`argparse`, `json`, `os`, `re`, `dataclasses`, `datetime`, `pathlib`, `sys`). No requirements or packaging file exists. Serves R-3 (QG-3).

## Decision

We will use only the Python standard library. We will add no third-party package, dependency file, or packaging dependency without a new ADR.

## Consequences

The tool installs and runs with no package manager step. Features that a library would supply must be written in the project.

Question for the architect: keep the standard-library-only rule as the third-party decision?
