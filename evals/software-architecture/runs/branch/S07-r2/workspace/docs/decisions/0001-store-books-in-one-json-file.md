# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

The catalog must survive a crash mid-write (R-2), and the program must run with only the Python
standard library (R-3). The Context was added when this ADR was upgraded at setup; the decision
predates it.

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Every change rewrites the whole file. The temporary file is renamed into place without being
flushed to disk first, so a power failure can still lose the write.
