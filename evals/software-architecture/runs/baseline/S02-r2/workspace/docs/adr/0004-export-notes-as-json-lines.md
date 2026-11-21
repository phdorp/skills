# 4. Export notes as JSON Lines through a `notes export` command

## Status

proposed 2026-11-21

Work on the export waits until the architect accepts this ADR (ADR-0002).

## Context

Users want to back up their notes and move them to other tools. This is a new requirement
(proposed as R-6 in arc42 section 1; not yet added there). Export only reads notes, so it must
not reach storage except through `Store` (ADR-0003). The format and the CLI command and exit
codes are decided centrally (ADR-0002). The program stays on the standard library (R-3, QG-2).
A backup file must never be left half-written, in the spirit of QS-1.

## Decision

**Format.** The export is JSON Lines: UTF-8 text, one JSON object per note, one object per line,
each line ending in `\n`, notes ordered by `id`. Each object has exactly these keys:

- `id`: integer, as stored;
- `text`: string, the note text;
- `created`: string, the timestamp as stored (ISO 8601, UTC).

Example:

```
{"id": 1, "text": "Buy milk", "created": "2026-11-21T08:00:00+00:00"}
```

Records are written with `json.dumps(..., ensure_ascii=True)`. Every record is then pure ASCII
and contains no raw line separators. This matters because `str.splitlines()` also splits on
characters such as U+2028, which a note may contain. An empty store exports an empty file.

**Command.** `notes export [-o PATH]`:

- without `-o`, the export goes to stdout, so `notes export > notes.jsonl` works;
- with `-o PATH`, the export goes to a file. If `PATH` already exists the command fails with
  exit code 1 and does not overwrite it. There is no overwrite flag in this decision. The export
  is written to a temporary file in the same directory and then renamed to `PATH`, so a failed
  export never leaves a partial file at `PATH`.

Exit codes follow the existing convention: 0 on success; 1 for runtime errors (store cannot be
opened, path exists, write fails), reported as `notes: <message>` on stderr; 2 for usage errors
(argparse default). `add`, `list` and `search` are unchanged.

**Structure.** The export reads notes through `Store.all()`. The record encoding is a helper in
`notes/cli.py` that depends only on `Note`. No new building block and no new dependency are
added.

**Not decided here.** Import and restore are not part of this ADR. They need their own ADR
before the project claims that an export can be restored.

## Alternatives considered

- **CSV.** It is the most widely imported format, but multi-line note text needs quoting rules
  that tools handle differently, and CSV has no types. A CSV converter can be added later on top
  of the JSON Lines file.
- **One Markdown file per note.** Readable, but it either drops `id` and `created` or needs an
  invented front-matter convention, and it spreads a backup over many files.
- **A JSON array.** It must be built and held in memory as a whole and cannot be appended or
  streamed. JSON Lines avoids both problems.
- **Copying the SQLite file.** It is an exact copy, but it is a backup of the storage engine,
  not an export, and it ties users to ADR-0001. Users can still copy `~/.notes.db` directly as a
  raw backup; this ADR does not change that.

## Consequences

- `id`, `text` and `created` survive an export unchanged, including newlines and non-ASCII text.
- Any change to the fields of `Note` changes this format. Such a change needs a superseding ADR.
- Users can make backups, but `notes` cannot restore one until an import ADR is accepted.
- Tests for the implementation should cover: the record shape; notes with newlines, quotes and
  U+2028; the empty store; refusal to overwrite; and that a failed write leaves no file at `PATH`.
