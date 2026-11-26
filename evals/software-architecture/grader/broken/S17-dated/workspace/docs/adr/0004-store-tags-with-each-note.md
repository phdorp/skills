# 4. Store tags with each note

## Status

proposed 2026-11-22

## Context

The plan's Task 2 adds tags, which changes the on-disk format and adds CLI options; both are
decided centrally (ADR-0002). Serves R-1; keeps QS-3.

## Decision

Add a `tags` text column to the `notes` table; `add` and `list` take `--tag`.

## Consequences

Existing stores migrate with `ALTER TABLE`.
