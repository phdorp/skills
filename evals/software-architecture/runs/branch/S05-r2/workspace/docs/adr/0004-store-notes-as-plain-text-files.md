# 4. Store notes as plain text files

## Status

proposed

## Context

Users want to read and edit their notes with any text editor (R-7). This replaces the storage
decision in ADR-0001 (SQLite). ADR-0001 stays `accepted` until this ADR is accepted. Storage is
centrally decided (ADR-0002), so this change needs this record first.

ADR-0001 gave crash safety (R-2, QG-1, QS-1) through SQLite transactions. A text format does not
have that, so the new store must provide crash safety in another way. Stdlib-only (R-3, QG-2)
still holds for plain text files.

## Decision

Notes are kept as plain text files that any text editor can read and edit.

Open, for the architect to settle before acceptance: one file for all notes, or one file per
note (proposed default: one UTF-8 text file per note, in a notes directory replacing
`~/.notes.db`).

## Consequences

- Crash safety must be re-established: writes go through a method that leaves either the old or
  the new content (for example, write to a temporary file, then rename). QS-1 is then measured
  against the new store. This is an open question for goal impact, not yet a changed measure.
- ADR-0003 (only `notes/store.py` touches the storage) stays accepted and still applies; "database
  file" in it reads as "note files".
- R-8 (encryption at rest) conflicts with plain text any editor can read. The architect must
  decide R-7 versus R-8 before this ADR is accepted.
- The default path `~/.notes.db` and `NOTES_DB` in the README change with this decision. Existing
  SQLite stores are not migrated by this ADR.
