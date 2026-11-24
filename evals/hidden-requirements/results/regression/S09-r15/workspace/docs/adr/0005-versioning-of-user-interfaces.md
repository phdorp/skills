# 5. Versioning of user-facing interfaces: none

## Status

proposed

## Context

The commands and their flags are what users type (R-2, QG-2), and the storage format is what users' files contain (ADR 0002). Versioning of what users depend on is a central decision (ADR 0001). Found in `pantry/cli.py`, `pantry/store.py` and the README.

## Decision

The code makes no versioning promise. The commands `add`, `list --soon` and `remove`, the `PANTRY_FILE` variable and the file format are unversioned: no command carries a version, no record carries a version field, and no migration step exists.

## Consequences

A change to a command or to the file format reaches existing users without a migration. Any versioning scheme is a new ADR that supersedes this one.
