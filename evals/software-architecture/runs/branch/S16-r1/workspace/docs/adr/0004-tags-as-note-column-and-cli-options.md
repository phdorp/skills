# 4. Store tags as a notes column and filter list by --tag

## Status

proposed

## Context

Users need to group notes (R-1 quality of listing and finding notes, QG-3 modifiability).
Adding tags changes the on-disk format (ADR-0001, which the architect decides centrally) and
adds CLI options to `add` and `list` (the CLI command names and options are on the central list
in ADR-0002). Existing stores must keep opening and keep their notes (R-2, QS-1).
No requirement in arc42 section 1 names tags; see the report for the suggested `add-requirements`.

## Decision

Recommended, awaiting the architect: We will add a `tags` column to the `notes` table, holding
comma-separated text with an empty default. We will migrate an existing table with
`ALTER TABLE`. `add` accepts `--tag` (repeatable) and `list` accepts `--tag` to show only
notes carrying that tag. Only `notes/store.py` changes the schema (ADR-0003).

Alternative not recommended: a separate `tags` table with a join. It is more normalized but
adds a second table to migrate and query for a single-user CLI.

## Consequences

- The on-disk format changes; stores written before this ADR are migrated in place on open.
- `add` and `list` gain options; existing invocations keep working.
- Comma-separated values cannot contain commas inside a tag; tags containing commas must be
  rejected or escaped, a choice the implementation must make when this is accepted.
- Changes Task 2 of `docs/plans/2026-11-22-search-and-tags.md`, which waits for this ADR.
- Does not affect ADR-0003 (the store remains the only SQL module) or ADR-0001 (still SQLite).
