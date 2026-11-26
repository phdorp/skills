# 6. Store each note as a JSON file

## Status

proposed

## Context

ADR-0001 stores notes in SQLite. The architect wants files that can be diffed and repaired by
hand. Crash safety (R-2, QG-1) then comes from ADR-0004's temporary-file-and-rename writes.

## Decision

Store each note as `<id>.json` in a notes directory. Supersedes ADR-0001 once accepted.

## Consequences

Search reads every file. ADR-0001 becomes "superseded by ADR-0006" when this is accepted.
