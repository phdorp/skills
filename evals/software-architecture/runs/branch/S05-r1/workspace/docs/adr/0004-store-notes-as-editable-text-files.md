# 4. Store notes as editable text files

## Status

proposed

## Context

R-7 requires that notes can be read and edited with any text editor. ADR-0001 stores all notes
in one binary SQLite file, which no text editor can read or edit. This ADR proposes to replace
the storage decision of ADR-0001; ADR-0001 stays `accepted` until this ADR is accepted.

Constraints that still apply: notes must survive crashes (R-2, QG-1, QS-1), and the program may
use only the Python standard library (R-3, QG-2). R-8 (encryption at rest) is not yet decided
against this format; see Consequences.

## Decision

Store notes as plain text that any text editor can read and edit, replacing the SQLite database
of ADR-0001.

Open before this ADR is accepted (the architect decides):

- the file layout: one file per note, or one file for all notes;
- how a crash mid-write leaves each note either fully stored or absent (QS-1);
- how R-8 (encryption at rest) applies to plain text files.

## Consequences

- Replaces ADR-0001. Crash safety can no longer come from SQLite transactions; the write method
  must be chosen so that QS-1 still holds.
- R-7 and R-8 conflict as written: encrypted files cannot be read or edited with a plain text
  editor. The architect must resolve this before acceptance.
- R-8 needs a cipher. Python's standard library has none, so R-8 conflicts with R-3 and the
  section 2 constraint unless the cipher is provided outside the standard library.
- ADR-0003 (only `notes/store.py` touches storage) still applies to the new format. Its
  reference to `sqlite3` describes ADR-0001 and needs updating once this ADR is accepted.
- ADR-0002 lists the storage engine and on-disk format as decided centrally; this ADR is the
  record for that decision.
- Work that depends on the new format (storage code, its tests) waits until you accept
  ADR-0004.
