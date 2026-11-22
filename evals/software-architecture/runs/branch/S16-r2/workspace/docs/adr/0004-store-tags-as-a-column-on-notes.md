# 4. Store tags as a column on the notes table

## Status

proposed

## Context

Users want to label notes and list them by label. The change alters the on-disk format
defined by ADR-0001 (one SQLite file, one `notes` table), and it adds `--tag` options to the
`add` and `list` commands, which ADR-0002 lists among the centrally decided CLI surface.
Existing stores must keep opening and must not lose notes when migrated (QG-1, QS-1, ADR-0001).
The change must stay inside `notes/store.py` for the database and be exposed through the
`Store` class (ADR-0003, QG-3, QS-3). No requirement in arc42 section 1 names tags yet; this
ADR serves a need that is named in words here (see the report). This ADR does not replace
any accepted ADR.

Options:

- **A. Column (proposed by the plan).** A `tags` text column on `notes`, comma-separated,
  default empty, added to existing tables with `ALTER TABLE`.
- **B. Join table.** A `tags(note_id, name)` table with one row per tag.

## Decision

We will add a `tags` text column to the `notes` table, holding the note's tags comma-separated,
default empty, and migrate existing stores with `ALTER TABLE`. `add` accepts `--tag` repeatable,
and `list` accepts `--tag` to filter.

## Consequences

- Easier: one table and one migration step; the `Note` value gains a single field.
- Harder: a tag may not contain a comma (the store must reject or escape it, a rule to decide
  when implementing); filtering by tag needs matching on whole tags, not substrings.
- The on-disk format changes; a store written by the new version may not be readable by the
  old one. This is the first change to the format under ADR-0001.
- Option B would avoid the comma rule and make tag filtering exact, at the cost of a second
  table and a join; choosing B later means a second migration.
- Blocks the plan's Task 2 until accepted; Task 1 (search ordering) is unaffected.
