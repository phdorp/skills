# 1. Store books in one JSON file

## Status

accepted (legacy)

## Context

A personal catalog is small, and the standard library reads and writes JSON (R-3). A crash
mid-write must not leave the catalog unreadable (R-2, QG-1).

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place,
because a personal catalog is small and the standard library reads and writes JSON.

## Consequences

Each write replaces the whole file, which is fine at personal scale. A process killed mid-write
leaves the previous catalog in place. Power-cut durability is not covered (QG-1 is open on it).
