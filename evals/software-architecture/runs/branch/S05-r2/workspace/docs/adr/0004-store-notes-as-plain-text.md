# 4. Store notes as plain text

## Status

proposed

## Context

Requirement R-7 says notes can be read and edited with any text editor. That replaces the
storage decision in ADR-0001 (SQLite), which the architect has named as replaced. ADR-0001
stays `accepted` until this ADR is accepted.

The forces: notes must survive crashes (R-2, QG-1, QS-1); the program may use only the Python
standard library (R-3, QG-2); and requirement R-8 says notes are encrypted at rest, which
conflicts with R-7 because encrypted notes cannot be read or edited in a plain text editor.

## Decision

We will store notes as plain text that any text editor can read and edit (R-7). The on-disk
file layout is not yet decided and must be settled before this ADR is accepted.

## Consequences

- Crash safety (R-2, QS-1) no longer comes from SQLite transactions. The plain-text store must
  provide it another way, for example by writing a new file and renaming it into place.
- R-7 and R-8 conflict. This ADR cannot be accepted until the architect answers which one wins
  when both cannot be met.
- ADR-0001 is superseded by this ADR once it is accepted. Its consequence "the file cannot be
  read with a text editor" no longer applies.
- ADR-0003 names `sqlite3` as the only module that touches storage. Its rule (only `store.py`
  touches the file) still holds; the module name in it changes when this ADR is accepted.
  ADR-0003 is not edited here.
