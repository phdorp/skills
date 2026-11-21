# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

The catalog must survive a crash mid-write (R-2, QG-1), and the tool must run on the standard
library alone (R-3, QG-3).

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Each command reads the whole file, and each save rewrites the whole file.
