# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

The catalog must survive a crash mid-write (R-2, QG-1) and run with only the Python standard library (R-3).

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Every change rewrites the whole file, and every read loads it whole. The rename keeps a killed
process from leaving a half-written file. The file is not yet flushed to disk before the rename,
so a power cut is not covered by this decision.
