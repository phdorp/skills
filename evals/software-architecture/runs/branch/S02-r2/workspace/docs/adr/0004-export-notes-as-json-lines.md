# 4. Export notes as JSON Lines to standard output

## Status

proposed

## Context

Users want to back up their notes and move them to other tools (R-2: no note is lost; R-1: core
use). The export format and the way the CLI reaches it are on the list of decisions made centrally
(ADR-0002: import and export formats, CLI command names). The program may use only the standard
library (R-3), and all note access goes through `Store` (ADR-0003). Notes are short text that may
contain newlines, commas, and quotes, so the format must escape them losslessly. The export must
also be a plain text file that does not depend on the SQLite file (ADR-0001).

## Decision

We will export every note as JSON Lines: UTF-8, one JSON object per line, lines ended by `\n`, and
the objects in ascending `id` order. Each object has exactly these keys, with the values as stored:

```json
{"id": 1, "created": "2026-11-21T10:00:00+00:00", "text": "Buy milk"}
```

We will add the command `python3 -m notes export`. It writes the whole export to standard output
and takes no path argument; the user redirects it to a file (`python3 -m notes export >
notes-backup.jsonl`). It reads notes only through `Store.all()`. An empty store produces no output
and exit code 0. Errors follow arc42 section 8: stderr, exit code 1.

Import is not decided here; it needs its own ADR and must accept this format.

## Consequences

- Backups and other tools can parse the file with any JSON parser, line by line, and a line that
  is cut off by a crash is detectable on its own.
- No new `Store` method is needed, and the CLI reaches storage only through `Store` (ADR-0003).
- The command writes to standard output, so it cannot overwrite an existing file by accident, and it
  has no file-handling code to test. The cost is that a failed redirect is the user's to notice.
- The format is not spreadsheet-friendly. A CSV export would be a separate decision.
- The export is a snapshot. It is not sync (R-4 is deferred) and does not change the store.
- Changing the format or the command name later needs a new ADR that replaces this one.
- Requirement IDs: an export requirement is not in arc42 section 1. The architect should confirm
  whether to add one (for example R-6) before this ADR is accepted.
