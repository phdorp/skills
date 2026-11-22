# 4. Store tags and expose them as a --tag option

## Status

proposed

## Context

Users want to group notes by topic and list one group (a requirement in words: "tag notes and
list by tag"; not yet an arc42 requirement ID). The change serves R-1 (add, list, search from
the command line) and QG-3 (modifiability, QS-3: only `notes/store.py` and its tests change for
a storage change). It changes two things ADR-0002 decides centrally: the on-disk format of the
SQLite file (ADR-0001) and the CLI surface (`add` and `list` gain a `--tag` option).
Existing stores must still open (R-2, QS-1: the store still opens after the change).

The plan proposes one option: a `tags` text column holding comma-separated tags, added to the
`notes` table with `ALTER TABLE` on open. Other options that fit the same constraints are a
separate `tags` table keyed by note id, or a `--tag` option on `add` only, with `list` filtering
later. This ADR does not choose among them.

## Decision

Proposed: We will add tags to notes in the SQLite file, and `add` and `list` will accept a
repeatable `--tag` option. The storage shape (column versus table, separator, migration) and
the CLI surface (which commands take `--tag`) are for the architect to decide.

## Consequences

- The on-disk format changes; existing stores are migrated on open, and only `notes/store.py`
  and its tests change for that (QS-3).
- The CLI gains an option on two commands, which is a change to the CLI surface ADR-0002 decides
  centrally. The CLI keeps reaching storage only through `Store` (ADR-0003).
- ADR-0001 (SQLite storage) is not changed. The atomic-transaction guarantee holds for the
  migration only if `ALTER TABLE` runs inside the same transaction discipline; this is to be
  checked when the option is chosen.
- Work that depends on this decision: Task 2 of `docs/plans/2026-11-22-search-and-tags.md`.
  Task 1 (newest-first search) does not depend on it and is complete.
