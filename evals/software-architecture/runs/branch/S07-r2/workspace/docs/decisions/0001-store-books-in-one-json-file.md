# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

Serves R-2 (the catalog survives a crash mid-write) and R-3 (runs with only the Python
standard library).

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

The whole catalog is rewritten on every change.
