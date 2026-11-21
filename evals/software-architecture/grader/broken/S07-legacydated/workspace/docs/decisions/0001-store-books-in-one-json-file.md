# 1. Store books in one JSON file

## Status

accepted 2026-11-21

## Context

A personal catalog is small and must survive a crash mid-write (R-2, QG-1); the standard library reads and writes JSON (R-3).

## Decision

We keep the whole catalog in one JSON file, written to a temporary file and renamed into place.

## Consequences

The whole file is rewritten on every change.
