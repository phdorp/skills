# 1. Store books in one JSON file

## Status

Accepted

## Context

A personal catalog is small, and the project must run on the Python standard library alone.
Requirement 2 says the catalog must survive a crash mid-write.

## Decision

We keep the whole catalog in one JSON file (`$SHELF_FILE`, default `~/.shelf.json`). Each save
writes the full list to a temporary file and renames it over the catalog with `os.replace`.

## Consequences

- Every change rewrites the whole file. This is acceptable at personal-catalog size.
- A crash before the rename leaves the previous catalog intact. This covers process crashes only:
  the save does not fsync, so a power loss can still damage the file (see
  [architecture gaps](../architecture.md#known-gaps)).
- There is no locking, so concurrent writers can lose updates.
- A corrupt file is not repaired; `load` raises.
