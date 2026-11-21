# 4. Replace SQLite storage with a text-editable format

## Status

proposed

## Context

Users want to read and edit their notes with any text editor (R-7). ADR-0001 chose SQLite,
whose binary file cannot be read or edited with a text editor, so this ADR replaces it. Crash
safety must hold as before (R-2, QG-1, QS-1), and the program must still use only the Python
standard library (R-3, QG-2).

R-8 (notes encrypted at rest) conflicts with R-7: plain text that any editor opens is not
encrypted at rest. The on-disk layout cannot be settled until the architect decides between
R-7 and R-8. ADR-0001 stays `accepted` until this ADR is accepted.

## Decision

We will replace the SQLite database with a store that a text editor can read and edit (R-7).
The concrete on-disk layout is not chosen yet; it is set when the architect resolves the
R-7/R-8 conflict.

## Consequences

Crash safety moves from SQLite transactions to the store's own write method, which must still
meet QS-1. Changing the storage is contained in `notes/store.py` (QS-3); ADR-0003 still holds,
but its mention of `sqlite3` no longer applies once this ADR is accepted.

Encryption at rest (R-8) needs its own ADR for the on-disk format and key handling, because
both are decided centrally (ADR-0002). A third-party cryptography library would also need an
ADR under ADR-0002 and would conflict with R-3.

Storage work waits until the architect accepts this ADR. When it is accepted, ADR-0001 becomes
`superseded by ADR-0004`.
