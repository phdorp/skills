# 4. Store note tags as a comma-separated column

## Status

proposed

## Context

Users want to sort notes with tags and filter `list` by a tag (R-1). Tags change the on-disk
format of the `notes` table, which ADR-0002 keeps central, and the store must keep opening
existing databases without losing notes (R-2, QS-1). The change stays inside `notes/store.py`
(QG-3, QS-3, ADR-0003). ADR-0001 (SQLite) is unchanged.

Options:

- **A. One `tags` text column, comma-separated, default empty.** An existing table is migrated
  with `ALTER TABLE`. `list --tag` matches whole tags. *Recommended, awaiting the architect.*
- **B. A separate `note_tags(note_id, tag)` table.** Exact matching and no separator rules, but
  a second table, a join in every read, and a second migration path.

## Decision

Recommended, awaiting the architect: We will use option A. A note's tags live in a `tags` column
of the `notes` table, stored as comma-separated text with the default empty string. Tags may not
contain a comma, and `add` rejects one with an error. An existing table gains the column through
`ALTER TABLE`, run in one transaction. The CLI gains a repeatable `--tag` option on `add` and
`list` (a CLI surface change under ADR-0002).

## Consequences

- Simple to read and migrate; one table, no joins.
- Tag rules (no commas) are enforced in `Store`; a tag cannot hold a comma.
- The file format stays a single SQLite file (ADR-0001). The change is additive: the existing
  columns keep their names and types.
- Option B would replace this column later through a new ADR, which would supersede this one.
- Does not affect ADR-0003: the CLI still reaches storage only through `Store`.
