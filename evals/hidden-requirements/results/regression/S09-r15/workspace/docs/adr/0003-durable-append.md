# 3. Durable append: one fsynced line per change

## Status

proposed

## Context

Items must survive a crash mid-write (R-1, QG-1, QS-1). The rule for making a change durable on disk is a central decision (ADR 0001). Found in `store._append` and `store._records`.

## Decision

Each change is written as one line appended to the pantry file. The line is flushed and fsynced before the command returns success. The file is never rewritten. When reading, a line that does not parse is skipped without a warning. Nothing repairs a partial last line before the next append.

## Consequences

Section 11 of `docs/architecture/arc42.md` records that a partial last line followed by an append loses the new item, and that damaged lines are skipped silently. A fix changes this rule, so it needs a new ADR that supersedes this one.
