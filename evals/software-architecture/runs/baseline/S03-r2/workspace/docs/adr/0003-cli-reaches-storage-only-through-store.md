# 3. CLI reaches storage only through the store module

## Status

accepted 2026-10-01

## Context

Contributors should be able to swap the storage engine by changing one module (QG-3, QS-3).

## Decision

Only `notes/store.py` reads or writes the storage (the note files of [ADR-0006](0006-store-one-json-file-per-note.md)).
`notes/cli.py` uses the `Store` class and the `Note` value.

## Consequences

Any new command that reads or writes notes goes through `Store`.
