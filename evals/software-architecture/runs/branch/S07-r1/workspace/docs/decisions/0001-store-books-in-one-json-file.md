# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

The catalog must survive a crash during a write (R-2) and run with only the Python standard
library (R-3). This record was written without a context section; the context is added at
upgrade.

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

The whole file is rewritten on every change, which is simple but suits only small catalogs. The
rename gives crash safety against a killed process, not against power loss: the file is not
synced before the rename (see QG-1).
