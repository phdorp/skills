# 4. Store notes as plain text

## Status

proposed

## Context

Notes must be readable and editable with any text editor (R-7). This replaces the SQLite storage
of ADR-0001, which stays `accepted` until this ADR is accepted. Notes must still survive crashes
(R-2, QG-1, QS-1), and the program still uses only the Python standard library (R-3, QG-2).

## Decision

We will store notes as plain UTF-8 text files that any text editor can read and edit, in place of
the SQLite database. Only `notes/store.py` touches these files (ADR-0003). The file layout and the
atomic-write method are not yet decided and must be settled in this ADR before it is accepted.

## Consequences

- Hand-edited files must still open. QS-1's "the store still opens" needs a measure that covers
  them; this is an open question for the architect.
- Crash safety moves from SQLite transactions to atomic file writes. The consequence in ADR-0001
  about the binary file no longer applies.
- ADR-0003 holds unchanged: only `notes/store.py` touches storage.
- Encryption at rest (R-8) is not decided here. It conflicts with R-7 and R-3 and needs its own
  decision once the architect has ranked them.
- Storage work waits until this ADR is accepted.
