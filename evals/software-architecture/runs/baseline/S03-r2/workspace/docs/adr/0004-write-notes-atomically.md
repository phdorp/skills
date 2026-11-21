# 4. Write notes atomically via a temporary file and rename

## Status

accepted 2026-11-21

## Context

QS-1 requires that a crash during `add` leaves the store readable (R-2, QG-1). Every note
file in the store, and any other file the store writes (for example an export), must meet the
same rule. Under [ADR-0006](0006-store-notes-as-json-files.md) each note is one file, so this
rule is what keeps a note from being half-written.

## Decision

Every file the store writes is written to a temporary file in the same directory, flushed with
`os.fsync`, and moved into place with `os.replace`.

## Consequences

A crash leaves either the old file or the new one, never a partial file. Writes cost one extra
`fsync`.
