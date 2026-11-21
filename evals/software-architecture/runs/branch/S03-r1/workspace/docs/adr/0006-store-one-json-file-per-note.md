# 6. Store each note as one JSON file

## Status

proposed

## Context

This ADR replaces ADR-0001 (use SQLite for storage). SQLite files are binary: they are hard to
diff and cannot be repaired by hand. Notes must still survive crashes (R-2, QG-1, QS-1), and the
program may use only the Python standard library (R-3, QG-2). Storage stays behind the store
module (QG-3, QS-3; ADR-0003). Crash safety for each file follows ADR-0004 (accepted).

## Decision

We will store each note as one JSON file in a notes directory, named by the note's ID. Every
write goes through the atomic write rule of ADR-0004: temporary file, `os.fsync`, `os.replace`.
No other storage engine is used.

## Consequences

Notes can be diffed, read and repaired with a text editor. A crash during `add` leaves either
the old set of files or the new one (QS-1). Listing and searching read every file, which is
slower than a query on a database; accepted for the current note counts (ADR-0005 is rejected,
so no faster engine is planned).

Effects on other ADRs: ADR-0003 still holds (only `notes/store.py` touches files), but its
wording names `sqlite3` and the database file; it needs a new ADR if the architect wants it
restated. ADR-0004 applies to every note file.

Work that follows once this is accepted: replace the SQLite code in `notes/store.py`, change
the default location from `~/.notes.db` to a notes directory, and update QS-3's test scope.
