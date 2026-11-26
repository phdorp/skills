# 5. Encryption at rest

## Status

proposed 2026-11-21. Not accepted: the architect must choose an option below.

## Context

Users want notes encrypted at rest, so that a stolen laptop exposes nothing (requirement
R-7). This cannot be met together with the other requirements as they stand:

- R-6 (read and edit with any text editor) means the note files are readable by any program
  that opens them. Application-level encryption would make them unreadable in an editor.
- R-3 (standard library only) means the program has no authenticated cipher. Writing one by
  hand is not acceptable. A real cipher needs a third-party package such as `cryptography`,
  which breaks R-3. Third-party dependencies are an architect decision (ADR-0002).

## Options

1. **Full-disk encryption by the operating system** (FileVault on macOS, LUKS or similar on
   Linux). The notes directory is encrypted at rest without any change to the program. R-3
   and R-6 still hold. Protects against a stolen laptop when the disk is locked. Does not
   protect a running, unlocked machine or a copy of the notes taken from it. Recommended.
2. **Application-level encryption with `cryptography`.** Protects the files everywhere. Breaks
   R-3 and R-6. Requires a new ADR that accepts both costs.
3. **Drop R-7.** Keep plain files and tell users to rely on option 1.

## Decision

Pending. Option 1 is recommended; it needs no code change, only documentation in the README.
