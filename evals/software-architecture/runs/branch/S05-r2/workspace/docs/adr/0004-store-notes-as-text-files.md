# 4. Store notes as text files

## Status

proposed

## Context

Notes must be readable and editable with any text editor (R-7). The binary SQLite file of
ADR-0001 cannot offer that, so this ADR replaces [ADR-0001](0001-use-sqlite-for-storage.md),
which stays `accepted` until this one is accepted.

Notes must still survive crashes (R-2, QG-1, QS-1), which SQLite transactions gave us; plain
files need another mechanism. The program stays on the standard library only (R-3, QG-2).
Encryption at rest (R-8) conflicts with plain text (R-7) and is not yet decided.

## Decision

We will store notes as plain text files. Each write goes to a temporary file that is then
renamed into place, so a crash leaves each note either whole or absent.

## Consequences

Crash safety moves from SQLite transactions to write-then-rename; QS-1 (SIGKILL during `add`)
is the check. Users can edit notes with any editor, so the store must cope with hand-edited
files that no longer parse. Only `notes/store.py` changes, as ADR-0003 requires.

R-7 and R-8 cannot both be met as written: a text editor cannot read encrypted notes. This ADR
cannot be accepted until the architect settles that conflict. Storage work waits for this
ADR's approval.
