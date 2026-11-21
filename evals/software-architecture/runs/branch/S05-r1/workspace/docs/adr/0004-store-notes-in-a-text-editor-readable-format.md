# 4. Store notes in a text-editor-readable format

## Status

proposed

## Context

Users want to read and edit their notes with any text editor (R-7). This replaces the SQLite
storage chosen in ADR-0001, which is binary and cannot be edited as text. The notes must still
survive crashes (R-2, QG-1, QS-1) and the program may use only the Python standard library
(R-3, QG-2). Encryption at rest (R-8) is also requested; it is not decided here, and it pulls
against R-7 because encrypted content cannot be edited as plain text.

## Decision

We will store notes in a plain-text format that any text editor can read and edit. This
replaces ADR-0001. The file layout and the write-safety mechanism are not decided here.

## Consequences

ADR-0001 stays `accepted` until this ADR is accepted, then becomes `superseded by ADR-0004`.
Until then, no code changes for this decision.

The format must still meet R-2 and QS-1: a crash during a write must leave every note either
stored or absent, and a hand edit must not make the store unopenable. How it does so is open.

ADR-0003 names `sqlite3` in its Decision. It stays `accepted`; its wording needs revising once
this ADR is accepted. Its rule (only the store touches the storage) still holds.

Encryption at rest (R-8) needs its own decision, since it adds a third-party dependency or a
hand-written cipher and conflicts with R-7. It waits for the architect and is not part of this
ADR.

Sync (R-4) is deferred and out of scope here.
