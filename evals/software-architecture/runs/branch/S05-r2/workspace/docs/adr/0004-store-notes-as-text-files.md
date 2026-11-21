# 4. Store notes as text files

## Status

proposed

## Context

Notes must survive crashes (R-2, QG-1, QS-1) and the program may use only the Python standard
library (R-3, QG-2). SQLite (ADR-0001) meets both, but its file is binary, so a user cannot read
or edit notes with a text editor. R-7 requires that access. This ADR replaces ADR-0001; that
ADR stays `accepted` until this one is accepted. The on-disk format is decided centrally
(ADR-0002).

R-8 (notes encrypted at rest) is not decided here. Its conflicts with R-7 and R-3 are listed in
Consequences.

## Decision

We will store each note as its own UTF-8 plain-text file in one notes directory. We will write
each file atomically: write a temporary file, flush it to disk, then replace the note's file
with `os.replace`. Only `notes/store.py` reads or writes these files (ADR-0003).

## Consequences

- Crash safety moves from SQLite transactions to atomic replacement. QS-1 (SIGKILL during `add`)
  must be re-measured on this design before acceptance.
- Notes become readable and editable with any text editor (R-7). The file is no longer binary.
- Open: the notes directory's default location. Today it is `~/.notes.db` (README, `NOTES_DB`).
- R-8 conflicts with this decision. Encrypted files cannot be read in a text editor (R-7), and
  the standard library has no symmetric cipher, so encryption at rest needs a third-party
  dependency, which breaks R-3 and is decided centrally (ADR-0002). This decision holds only if
  R-7 is ranked above R-8, or R-8 is resolved by a later ADR.
- ADR-0003 still holds: only `notes/store.py` touches the files.
- Storage work waits until this ADR is accepted. ADR-0001 stays in force until then.
