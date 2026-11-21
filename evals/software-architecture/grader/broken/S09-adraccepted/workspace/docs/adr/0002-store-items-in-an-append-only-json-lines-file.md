# 2. Store items in an append-only JSON Lines file

## Status

accepted 2026-11-21

## Context

Found in the code (R-2).

## Decision

Every change is appended as one JSON line and synced with fsync.

## Consequences

See the decision.
