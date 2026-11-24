# 5. No third-party dependencies

## Status

proposed

## Context

Found in the code: every import in `pantry/` and `tests/` comes from the standard library. This serves R-3 (runs with only the Python standard library, QG-3) and is a constraint in arc42 section 2.

## Decision

We will use only the Python standard library, in the package and in its tests. The project has no requirements file and no packaging step that installs anything.

## Consequences

The tool runs on any Python 3 install with no `pip install` step. Libraries that would make some work easier (a date library, a CLI framework) are out. A third-party dependency needs a new ADR that supersedes this one.
