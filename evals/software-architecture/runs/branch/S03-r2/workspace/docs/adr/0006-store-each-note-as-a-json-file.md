# 6. Store each note as one JSON file

## Status

proposed

## Context

SQLite files are hard to diff and repair by hand, so the architect wants notes in a
plain-text form. Notes must survive crashes (R-2, QG-1, QS-1) and the program may use only the
Python standard library (R-3, QG-2). This ADR replaces ADR-0001 (use SQLite for storage); ADR-0001
stays `accepted` until this ADR is accepted.

## Decision

We will store each note as its own JSON file in a notes directory, by default `~/.notes/`, and
the store will write each note file with the rule of ADR-0004. We will not use SQLite or any other
database engine. The `json` module of the standard library reads and writes the files.

## Consequences

- Notes can be read, diffed and repaired with a text editor. A damaged note affects only its own file.
- A crash during `add` leaves either the note file or no note file (QS-1), provided ADR-0004's rule
  holds for every note file.
- ADR-0004 does not yet require syncing the directory after a rename. Without that, a new note file
  may be lost on a crash even though its contents were synced; this needs settling in ADR-0004 or here.
- `list` and `search` read every file in the directory, so search gets slower as the number of notes
  grows (R-1).
- The default location changes from `~/.notes.db` to a directory, so the `NOTES_DB` variable and any
  existing database need a migration path. This ADR does not decide that path.
- Only `notes/store.py` changes, as ADR-0003 requires; the on-disk format is a central decision
  (ADR-0002), so this ADR is the record for it.
- ADR-0001 is superseded by this ADR once this ADR is accepted.
- ADR-0004 applies to the note files written here; its Context already covers files besides the database.
