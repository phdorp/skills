# 4. Export notes as JSON Lines through an `export` command

## Status

proposed

## Context

Users ask to export their notes to back them up and to move them to other tools. The export
must keep every note (R-2, QG-1), use only the standard library (R-3, QG-2), and must not
break the rule that only `notes/store.py` touches storage (ADR-0003, QG-3). ADR-0002 lists
import and export formats and CLI command names as decisions made centrally, so this ADR
decides both. No requirement ID exists for export yet; it is named in words here.

The format has to round-trip without loss: note text may contain newlines, quotes, and
non-ASCII characters, and the creation time must survive unchanged.

## Decision

We will export all notes as JSON Lines: UTF-8 text, one JSON object per note, one note per
line, in ascending `id` order. Each object has exactly the keys `id` (integer), `text`
(string), and `created` (the ISO 8601 UTC string the store already holds). Example line:

    {"id": 1, "text": "Buy milk", "created": "2026-10-02T08:14:00+00:00"}

We will add the command `python3 -m notes export`. Without options it writes to standard
output. With `-o PATH` (or `--output PATH`) it writes to a new file at `PATH`. We will write
the file to a temporary file in the same directory and rename it into place, so an
interrupted export never leaves a partial file at `PATH`. If `PATH` already exists, the
command refuses to overwrite it and exits with code 1. An empty store produces empty output
and exit code 0. Errors go to stderr as `notes: <message>`, exit code 1 (arc42 section 8).

The command reads notes only through `Store.all()`. The JSON Lines serialisation lives in
`notes/cli.py` next to the existing output code, using the standard `json` module.

## Consequences

JSON Lines keeps newlines, quotes, and non-ASCII text exact, keeps `id` typed as an integer,
and can be read line by line by most tools. A plain CSV export was rejected as the only
format because multi-line text and typed fields are fragile in it; a CSV or Markdown export
can be added later as its own decision.

The three keys and their meaning become a compatibility promise for backups. Adding,
renaming, or retyping a key needs a new ADR that supersedes this one.

Import is not decided here and needs its own ADR. The command name `export` and the
refuse-to-overwrite rule are fixed by this ADR; changing either needs a new ADR.

No new building block is added, so the dependency rule in ADR-0002 is unchanged. The export
follows ADR-0003 because it uses `Store.all()` and never imports `sqlite3`.

Work that follows once this ADR is accepted: a requirement for export in arc42 section 1
(architect's call), the command in `notes/cli.py`, tests for round-trip and refusal to
overwrite, and README usage.
