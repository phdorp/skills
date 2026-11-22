# 6. Store each note as one JSON file

## Status

proposed

## Context

ADR-0001 stores all notes in one SQLite file. The architect wants to move off SQLite, because
SQLite files are hard to diff and repair by hand. The program may use only the standard library
(R-3, QG-2), which includes the `json` module. Notes must still survive crashes (R-2, QG-1,
QS-1), which ADR-0004 provides per file. The storage engine and on-disk format are decided
centrally (ADR-0002). This ADR replaces ADR-0001.

## Decision

We will store each note as its own JSON file, `<id>.json`, in one notes directory, by default
`~/.notes/`. Every note file is written as ADR-0004 requires. Only `notes/store.py` reads or
writes these files (ADR-0003).

## Consequences

- A note file can be read, diffed, and repaired with a text editor.
- A crash during `add` leaves the old or new note file, never a partial one. No multi-note
  transaction is needed, because each add changes one note.
- `list` and `search` read every note file, so search gets slower as the number of notes grows
  (R-1). This trade-off is accepted here; it does not reopen ADR-0005.
- ADR-0003 and QS-3 are unchanged: the change stays inside `notes/store.py` and its tests.
- ADR-0001 becomes `superseded by ADR-0006` when this ADR is accepted.
- Work on the storage module waits until this ADR is accepted (ADR-0002).
- The code, tests, and README (which names `~/.notes.db`) still describe SQLite. They change
  when this ADR is implemented; this ADR does not change them.
