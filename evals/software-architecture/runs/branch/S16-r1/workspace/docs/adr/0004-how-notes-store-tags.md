# 4. How notes store tags

## Status

proposed

## Context

Users want to tag notes and filter `list` by tag. Tagging is not yet a numbered requirement in
arc42 section 1; it is named in words here and needs the architect's confirmation. The tag design
changes the on-disk format of the SQLite file, which ADR-0002 decides centrally, and existing stores
must keep opening (QS-1, QG-1, R-2). Only `notes/store.py` may touch the database (ADR-0003, QS-3),
so either option below keeps all storage code in that one module. R-1 (command-line use), QG-3
(modifiability), QS-3 (swap storage by changing one module).

## Decision

Pending the architect's choice between two options:

- **A (from the plan):** add a `tags` text column to the `notes` table holding comma-separated
  tags, added to existing stores with `ALTER TABLE`. Simple, one table. Filtering by tag needs
  delimiter-aware matching: a plain substring match would make `--tag work` also match a note
  tagged `homework`. A tag containing a comma cannot be stored.
- **B:** add a `tags` table with one row per (note id, tag), created with `CREATE TABLE IF NOT
  EXISTS`, so existing stores need no `ALTER TABLE`. Exact tag matching and no comma limit. Two
  tables to keep consistent when a note is written.

## Consequences

Either option keeps storage inside `notes/store.py` (ADR-0003). The choice fixes the on-disk
format, which is costly to change once users have tagged notes, so it waits for the architect.
The search ordering change (newest first) is independent of this choice.
