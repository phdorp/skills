# 4. Store notes as plain text that any editor can read

## Status

proposed

## Context

Users want to read and edit their notes with any text editor (R-7). This replaces the SQLite
storage of ADR-0001, the ADR this one replaces; ADR-0001 stays `accepted` until this ADR is
accepted. ADR-0001 gave crash safety through SQLite transactions (R-2, QG-1, QS-1); plain text
needs another mechanism. The standard-library-only constraint (R-3, QG-2) still holds.
Notes encrypted at rest (R-8) conflict with R-7: encrypted notes cannot be edited in a plain
text editor. That conflict is open and waits for the architect.

## Decision

We will store notes as plain text files that any text editor can read and edit, in place of the
SQLite database of ADR-0001 (R-7).

## Consequences

- Crash safety (R-2, QS-1) must be re-established without SQLite transactions. The mechanism is
  not chosen yet.
- The file layout (one file per note, or one file) is not decided.
- ADR-0003 still holds: only `notes/store.py` touches the note files. Its text names `sqlite3`
  and the database file, so its wording is stale once this ADR is accepted; its rule stays.
- If R-8 is confirmed over R-7, this decision changes and needs a new ADR.
- Storage work (`notes/store.py`, and the `~/.notes.db` default in the README) waits until this
  ADR is accepted.
