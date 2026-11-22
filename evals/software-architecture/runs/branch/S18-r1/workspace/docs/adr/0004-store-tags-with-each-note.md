# 4. Store tags with each note

## Status

proposed

## Context

Notes need tags that `list` can filter on. Tags change the on-disk format and add CLI options,
both decided centrally (ADR-0002). Serves R-1; keeps QS-3.

## Decision

Add a `tags` text column (comma-separated, default empty) to the `notes` table, migrated with
`ALTER TABLE`; `add` and `list` take `--tag`.

## Consequences

Every store migrates on first open. A tag cannot contain a comma.
