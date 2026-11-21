# 4. Export notes as JSON Lines via `notes export`

## Status

proposed

## Context

Users want to back up their notes and move them to other tools. This is not yet a requirement
ID in arc42 section 1; it is named here in words and awaits the architect's decision on whether
to add it as an R-n.

The export format and the CLI command name are on the central list in
[ADR-0002](0002-record-architecture-decisions.md). Constraints: standard library only (R-3);
export only reads, so it must not change the store (R-2); the database is reached only through
`Store` ([ADR-0003](0003-cli-reaches-storage-only-through-store.md)). The note fields (`id`,
`text`, `created`) are fixed by the `Note` value and the storage format in
[ADR-0001](0001-use-sqlite-for-storage.md).

## Decision

We will export notes as JSON Lines: UTF-8 text, one JSON object per line, one line per note, in
ascending `id` order. Each object has exactly these fields: `id` (integer), `text` (string),
`created` (string, ISO 8601 UTC, as stored).

We will add the command `notes export`. It writes the export to standard output, and the user
redirects it to a file (`python3 -m notes export > notes.jsonl`). It takes no other options. It
reads all notes through `Store.all()`. It exits 0 on success; on error it prints
`notes: <message>` to stderr and exits 1, as arc42 section 8 requires.

## Consequences

- Easier: JSON escapes newlines and quotes, so any note text round-trips exactly. The `json`
  module is in the standard library. One line per note works with line-based tools and diffs.
  Writing to stdout leaves file paths and overwrite rules to the user's shell.
- Harder: spreadsheets do not open JSON Lines directly. A CSV format is not part of this
  decision and would need its own decision.
- The export file is plain, unencrypted text of every note. Users must protect it themselves.
- A failed export can leave a partial file. The exit code 1 is the only signal, so backups must
  check it.
- Restoring from an export (import) is not decided here. Import formats are on the central list
  in ADR-0002, so restore needs its own ADR before it is built.
- No change to storage ([ADR-0001](0001-use-sqlite-for-storage.md),
  [ADR-0003](0003-cli-reaches-storage-only-through-store.md)) and no new `Store` method. arc42
  section 5 (building blocks) is unchanged. The new command is one more entry under the command
  names decided in ADR-0002.
