# 4. Export notes as JSON Lines via `notes export`

## Status

proposed

## Context

Users keep notes for years (stakeholder "Users", R-2, QG-1) and want to back them up and move
them to other tools. No requirement ID covers export yet; the architect should confirm whether
to add one. The format must be readable by any tool, must hold every field of `Note` (id,
text, created) without loss, and must survive note text that contains newlines. The program
may use only the standard library (R-3, QG-2). Only `notes/store.py` touches the database
(ADR-0003), and the CLI reaches notes only through `Store` (ADR-0003).

## Decision

We will export notes as JSON Lines: UTF-8, one JSON object per line, with exactly the keys
`id` (integer), `text` (string), and `created` (ISO 8601 UTC string, as stored), in ascending
`id` order.

We will add the command `notes export [-o PATH]`:

- without `-o`, the export is written to standard output;
- with `-o PATH`, the export is written to a temporary file in the same directory and then
  renamed to `PATH`, so an interrupted export never leaves a partial file at `PATH`;
- if `PATH` already exists, the command refuses to overwrite it, prints
  `notes: <PATH> already exists` to stderr, and exits with code 1;
- errors follow arc42 section 8: `notes: <message>` on stderr, exit code 1; success is exit
  code 0.

The export reads notes with `Store.all()`. The serialization lives in `notes/cli.py`, which
imports only `store` and `model`, so the dependency rule is unchanged. Importing this format
back is out of scope and needs its own ADR if it changes the format.

## Consequences

Users can back up with `notes export -o backup.jsonl` or `notes export > backup.jsonl`, and any
tool that reads JSON Lines can consume the file. CSV and Markdown are not offered; they would
need a second format decision. The format is part of the public contract: changing a key or
its meaning requires a new ADR that supersedes this one. No change to `store.py` or
`model.py` is needed. The database file itself is not the export format, so ADR-0001's
binary-file note still applies.
