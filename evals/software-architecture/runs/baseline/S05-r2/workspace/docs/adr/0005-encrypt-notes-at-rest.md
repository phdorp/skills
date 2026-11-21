# 5. Encrypt notes at rest

## Status

proposed 2026-11-21. Not accepted; no encryption is implemented. Work that depends on it waits
until this ADR is accepted (ADR-0002).

## Context

Interviews asked that a stolen laptop expose no notes (R-9). This is an on-disk format decision,
so it is central (ADR-0002). It conflicts with two accepted requirements:

- R-7: notes can be read and edited with any text editor. Ciphertext cannot be edited directly,
  so application-level encryption ends R-7 unless the user decrypts first.
- R-3: the program uses only the Python standard library. The standard library has no
  authenticated cipher. Third-party libraries are excluded for the same reason as the rejected
  `rich` request (R-6).

## Options

1. **Operating-system full-disk encryption** (FileVault on macOS, LUKS or BitLocker elsewhere).
   Keeps R-7 and R-3 unchanged. The application does not enforce it, so the guarantee holds only
   where the user enables it.
2. **Application-level encryption** with a passphrase, using an external `openssl` binary through
   `subprocess`. Keeps R-3 but ends R-7 for encrypted notes, needs a passphrase on every command,
   and relies on an external binary.
3. **Application-level encryption with a third-party library.** Breaks R-3.

## Decision

Pending. The architect chooses an option and accepts this ADR, or relaxes R-7 or R-3.

## Consequences

Until this ADR is accepted, notes are plain text on disk ([ADR-0004](0004-store-notes-as-plain-text-files.md)).
