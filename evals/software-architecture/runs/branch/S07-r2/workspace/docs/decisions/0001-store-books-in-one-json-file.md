# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

Serves R-2 (a crash mid-write leaves the catalog readable) and R-3 (only the standard library).
A personal catalog is small, and the standard library reads and writes JSON.

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Every read and write handles the whole catalog, which is acceptable for a personal catalog and
gives no partial writes on a crash. Scaling to large catalogs would need a new decision.
