# 4. Standard library only

## Status

proposed

## Context

Found in the code, not decided by the architect. Every module imports only from the standard library (argparse, dataclasses, datetime, json, os, pathlib, re, sys). The project has no packaging file. Third-party dependencies are on the list of decisions made centrally (ADR-0001). It serves R-3 (runs with only the Python standard library; QG-2 installability).

## Decision

As found: the program uses only the Python standard library, and its tests run with `python3 -m unittest`.

## Consequences

No install step is needed beyond a Python 3 interpreter. Any future third-party dependency needs a new ADR that supersedes this one.
