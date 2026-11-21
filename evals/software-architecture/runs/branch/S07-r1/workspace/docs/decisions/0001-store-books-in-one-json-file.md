# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

The catalog must survive a crash mid-write (R-2, QG-1) and the program must run with only the
standard library (R-3, QG-3).

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Every save rewrites the whole file, so the cost grows with the catalog. The rename protects
against a crashed process; it does not call `fsync`, so a power cut is not covered (open
question for the architect, see the report).
