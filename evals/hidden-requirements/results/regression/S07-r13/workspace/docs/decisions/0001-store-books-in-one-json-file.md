# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

Serves R-2 (the catalog survives a crash mid-write) and R-3 (runs with only the standard library).
The record predates the requirements list; it is upgraded, not reopened.

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Each change rewrites the whole file. The temporary-file-then-rename write covers a crash of the
process; whether a power cut is covered is open (R-2).
