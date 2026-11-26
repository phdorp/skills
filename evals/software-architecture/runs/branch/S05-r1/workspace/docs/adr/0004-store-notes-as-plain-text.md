# 4. Store notes as plain text, replacing SQLite

## Status

proposed 2026-11-22

## Context

Notes can be read and edited with any text editor (R-7). This is a system-level requirement
from this week's user interviews, confirmed by the architect. It replaces the SQLite decision in
[ADR-0001](0001-use-sqlite-for-storage.md), which stays `accepted` until this ADR is accepted.

ADR-0001 gets crash safety (R-2, QG-1, QS-1) from SQLite transactions. The replacement must keep
that guarantee by other means. Notes are also to be encrypted at rest (R-8), which the architect
has confirmed as system-level; its interaction with R-7 is open (see Consequences). The program
may use only the Python standard library (R-3, QG-2).

## Decision

Replace the SQLite store with plain-text storage: notes are kept as text that any text editor can
read and edit.

Not yet decided, and to be settled in this ADR before it is accepted:

- the file layout (one file, or one file per note);
- the method that keeps a crash during `add` from losing or corrupting a note (QS-1).

## Consequences

- Once accepted, [ADR-0001](0001-use-sqlite-for-storage.md) becomes `superseded by ADR-0004`.
- R-7 and R-8 conflict for the same file: text that any editor can read cannot also be encrypted at
  rest. This must be resolved before acceptance. Open question for the architect: if only one of
  R-7 and R-8 can be fully met, which?
- Encryption (R-8) needs a cipher that the standard library does not provide. That conflicts with
  R-3 and with the rule in [ADR-0002](0002-record-architecture-decisions.md) that third-party
  dependencies are decided centrally.
- [ADR-0003](0003-cli-reaches-storage-only-through-store.md) names `sqlite3` in its Decision. Its
  rule, that only the store module touches storage, still holds under this ADR; its wording is
  left for the architect to update.
- No storage code changes until this ADR is accepted.
- Quality measure QS-1 (SIGKILL during `add`) still applies to the new storage.
