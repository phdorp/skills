# 4. Store notes as plain text, replacing SQLite

## Status

proposed

## Context

Supersedes ADR-0001 (Use SQLite for storage, accepted 2026-10-01). The architect's new
requirement R-7 says notes can be read and edited with any text editor, which the SQLite file
of ADR-0001 rules out.

The forces that stay: notes must survive crashes (R-2, QG-1, QS-1), and the program may use
only the Python standard library (R-3, QG-2). R-8 (notes encrypted at rest) is confirmed as
system-level but is not yet reconciled with R-7; see Consequences.

## Decision

We will store notes as plain UTF-8 text, readable and editable with any text editor, replacing
the single SQLite database file of ADR-0001. The file layout is not yet decided.

## Consequences

- Crash safety moves from SQLite transactions to the store itself. The store must write each
  change atomically (for example, write a temporary file, flush it to disk, then rename it over
  the old one) so that QS-1 still holds.
- R-7 and R-8 conflict: text that any editor can read is not encrypted at rest. This ADR cannot
  be accepted until the architect decides how R-7 and R-8 are reconciled.
- Standard library suffices (`open`, `os.replace`, `os.fsync`), so R-3 and the dependency rule
  in ADR-0002 are unaffected.
- ADR-0003 still holds: only `notes/store.py` touches the files, so swapping storage stays
  confined to one module (QS-3).
- Work that depends on the storage change waits until this ADR is accepted.
