# 4. Store tags as a column on the notes table

## Status

proposed

## Context

Users need to tag notes and filter `list` by tag (a need no R-n in arc42 section 1 names yet). This changes the on-disk format of the SQLite file decided in ADR-0001 and listed in ADR-0002 as decided centrally. Existing stores must keep opening and keep all their notes (R-2, QS-1), and only `notes/store.py` may touch the schema (ADR-0003, QS-3).

Options:

- **A. A `tags` column on `notes`:** comma-separated text, default empty, added with `ALTER TABLE` on existing stores. One column, no new table. Filtering matches whole tags; tags may not contain commas.
- **B. A `note_tags` table:** rows of `(note_id, tag)`, joined on list. Exact tag matching without string tricks; more schema, and a second migration path.

Recommended, awaiting the architect: **A**, because it is the smallest change to the file and the tag filter can match whole tags in SQL.

## Decision

Recommended, awaiting the architect. We will add a `tags` column to the `notes` table (option A), migrate existing stores with `ALTER TABLE`, and keep all schema access inside `notes/store.py`.

## Consequences

- The file gains one column; stores written before the change still open, with empty tags.
- Tags are limited: no commas inside a tag. Filtering matches whole tags, not substrings.
- Option B would replace this with a table and a join; it can be chosen later with a migration, at the cost of a second schema change.
- No other accepted ADR changes. ADR-0001 (SQLite) and ADR-0003 (store-only access) hold under either option.
