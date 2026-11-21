# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

R-2 (the catalog survives a crash mid-write) and R-5 (runs with only the Python standard library).

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Every write rewrites the whole file, so the cost of a write grows with the catalog. The rename
protects against a crash of the process; the temporary file is not flushed to disk before the
rename, so a power loss can still leave an unreadable file (see QS-2).
