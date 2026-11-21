# 4. Replace SQLite with text-editable storage

## Status

proposed

## Context

ADR-0001 chose SQLite for storage, so that notes survive crashes (R-2, QG-1, QS-1) with only
the standard library (R-3, QG-2). The architect has since added R-7: notes can be read and
edited with any text editor. A binary SQLite file cannot be edited with a text editor, so
ADR-0001 is replaced. ADR-0001 stays `accepted` until this ADR is accepted.

R-8 (notes encrypted at rest) also bears on the storage format. It is not decided here. R-8
conflicts with R-7, since a file an editor can read is plaintext unless the editor can open an
encrypted file, and encryption needs a cipher the standard library does not provide (R-3).

## Decision

Notes are stored in a format that a text editor can read and edit (R-7). The concrete format,
its crash-safety mechanism (QS-1), and how R-8 is met are open questions for the architect and
are not decided by this draft.

## Consequences

- The storage engine and on-disk format are decided centrally (ADR-0002), so storage work
  waits until this ADR is accepted.
- ADR-0003 is unaffected: `store` remains the only block that touches the storage.
- QS-1 (crash safety) must be re-measured for the new format; the SQLite transaction argument
  of ADR-0001 no longer applies.
- Any new third-party dependency needed for R-8 is a central decision (ADR-0002) and conflicts
  with R-3 unless the architect accepts that trade-off.
