# 0003. Only the Python standard library is used

## Status

proposed

## Context

As found in the code, not yet decided by the architect: every module in `pantry/` imports only from the standard library (argparse, dataclasses, datetime, json, os, pathlib, re, sys), and `tests/` uses `unittest`. This serves R-3 (runs with only the Python standard library). It is a central decision under ADR-0001.

## Decision

We use no third-party packages in the program or its tests.

## Consequences

Storage, durability and parsing rely on the standard library (`os.fsync`, `json`, `datetime`). Adding any third-party package needs a new ADR that supersedes this one.
