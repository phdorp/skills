# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

Serves R-2 (a crash during `add` or save leaves the catalog readable) and R-3 (standard library
only), that is QG-1 and QG-5. A personal catalog is small.

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Each save rewrites the whole file. The rename covers a process crash mid-write. Nothing is
fsynced, so a power loss during a write is not covered; this is an open question for the
architect (QG-1).
