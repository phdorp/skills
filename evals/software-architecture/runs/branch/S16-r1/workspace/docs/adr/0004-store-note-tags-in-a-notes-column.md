# 4. Store note tags as a comma-separated column on notes

## Status

proposed

## Context

Users want to label notes and list notes by label. This is a new need: no R-n in arc42 section 1
names tagging yet (see the ledger's "New requirement" line for the architect). It changes the
on-disk format (the `notes` table gains a column) and the `Note` value, so it crosses the
storage boundary (ADR-0001, ADR-0002: "the storage engine and the on-disk format" are decided
centrally). Existing stores must keep opening (QS-1: stores stay readable; R-2). The
standard library only (R-3). Only `notes/store.py` touches the database (ADR-0003, QS-3).

Options the plan implies:

- **A. A `tags` text column, comma-separated, default empty.** Migrated with `ALTER TABLE` on
  open. Simple; `list --tag` needs a match that does not hit substrings (`work` vs `homework`).
- **B. A `tags` table keyed by note id** (one row per tag). Exact tag matching and indexing;
  a second table to migrate and keep consistent with `notes` under crash safety (QS-1).

## Decision

We will use option A: add a `tags` column (comma-separated text, default empty) to the `notes`
table, migrate an existing table with `ALTER TABLE`, and match tags exactly in `Store`.

## Consequences

- `Note` gains a `tags` field; `Store.add` and `Store.all`/`search` read and write it; the
  CLI gains `--tag` on `add` and `list` (no new command names, so ADR-0002's CLI list is not
  changed).
- Tag values may not contain commas; the store must reject them. Exact tag matching must not
  match substrings.
- Switching to option B later is a schema migration; it stays inside `notes/store.py` (ADR-0003).
- Accepting this ADR unblocks Task 2 of `docs/plans/2026-11-22-search-and-tags.md`. Task 1
  (newest-first search) is independent and already committed.
