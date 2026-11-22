# 4. Store note tags as a comma-separated column on notes

## Status

proposed

## Context

Users want to group notes with tags and list one group with `notes list --tag` (R-1, QG-3).
The store is one SQLite table (ADR-0001), and the on-disk format is decided centrally
(ADR-0002). Existing stores must keep opening, since users keep notes for years (QG-1, QS-1).
Tags must stay within the standard library (R-3). The plan this comes from lists the options
as a comma-separated TEXT column; a separate `tags` table was not evaluated by the plan.

## Decision

Recommended, awaiting the architect.

We will add a `tags` column to the `notes` table: TEXT, NOT NULL, default empty, holding the
note's tags comma-separated. An existing table is migrated with `ALTER TABLE` when the store
opens. Only `notes/store.py` touches the column (ADR-0003).

## Consequences

- The on-disk format changes. Stores written before this change still open; their notes have
  no tags. This is the change ADR-0002 reserves for the architect.
- A tag cannot contain a comma. The CLI must reject such a tag, or the filter misreads it.
- Filtering by tag matches whole tags, not substrings of the stored text, so the store has
  to compare each tag on its own.
- A separate `tags` table would support tag listing and renaming without parsing text. It is
  the alternative if tag management grows beyond filtering; choosing it later means another
  format change and a new ADR.
- Affects no other accepted ADR. ADR-0003 is respected: `cli` still reaches storage only
  through `Store`.
