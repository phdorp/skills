# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

Serves R-2 (the catalog survives a crash mid-write) and R-3 (only the Python standard library).

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Each save rewrites the whole file, which suits up to about 10,000 books. The rename guards
against a killed process; it does not fsync, so a power loss may lose the last write.
