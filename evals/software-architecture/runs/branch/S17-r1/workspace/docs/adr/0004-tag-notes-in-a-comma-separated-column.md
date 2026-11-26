# 4. Tag notes in a comma-separated column

## Status

proposed

## Context

Users need to sort notes by a label such as `work` and list only those notes (R-1). Tags change
the on-disk format of the `notes` table, which the storage decision places on the centrally
decided list (ADR-0001), and add a `--tag` option to `add` and `list`, which the CLI decision
also places on that list (ADR-0002). Stores created before this change must still open (QS-1
requires every store to open after a crash). No accepted ADR settles either point.

## Decision

We will add a `tags` column to the `notes` table: comma-separated text, default empty. An
existing table is migrated in place with `ALTER TABLE`. `Note` gains a `tags` field. `notes add`
takes `--tag` (repeatable), and `notes list` takes `--tag` to show only notes carrying that tag.

## Consequences

- Tags are simple to store and query, with no extra table and no join.
- A tag cannot contain a comma; `add` must reject or escape such a tag. Filtering on a tag must
  match whole tags, not substrings.
- Existing stores keep working after the `ALTER TABLE` migration; the file stays readable only
  through SQLite, as ADR-0001 already states.
- `cli` and `store` both change; `store` remains the only block that touches the database
  (ADR-0003).
- If tags later need to be shared, indexed, or carry metadata, this format must be replaced by
  a new ADR.
