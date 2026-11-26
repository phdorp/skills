# 4. Plain-text note files, device sync and encryption at rest

## Status

proposed 2026-11-21 — supersedes ADR-0001 if accepted; needs the architect's acceptance before
any implementation

## Context

Three user requirements from this week's interviews:

1. Notes sync between a user's laptop and desktop (R-4, currently deferred: "needs a server").
2. Notes can be read and edited with any text editor.
3. Notes are encrypted at rest, so a stolen laptop exposes nothing.

These conflict with the accepted decisions:

- ADR-0001 stores notes in one binary SQLite file, which a text editor cannot read or repair.
  The same file cannot be synced by a file-sync tool while it is open on two machines without
  risk of corruption.
- Requirement 2 needs plaintext on disk; requirement 3 needs ciphertext on disk. Both cannot
  hold for the same file unless the CLI decrypts and re-encrypts on every edit.
- Encryption needs a cipher. The standard library has none (R-3, QG-2 forbid third-party
  packages without a decision; see ADR-0005).

## Options

A. **One Markdown file per note in a notes directory.** Plain text, editable with any editor,
   and it syncs with any folder-sync tool. Crash safety by writing to a temporary file and
   `os.replace`. Stays within the standard library. Sync conflicts on the same note appear as
   sync-tool conflict copies.

B. **Keep SQLite; add an export/import to text.** Editing a text export does not change the
   note the CLI reads, so requirement 2 is not met.

For encryption at rest, the options are:

- **E1. Full-disk encryption (FileVault, LUKS, BitLocker) and no app-level encryption.** A stolen
  laptop exposes nothing, and the editor and sync work on plaintext. Requirement 3 is met by the
  OS, not by the app. The notes directory must sit on an encrypted volume.
- **E2. App-level encryption with a third-party cipher and a passphrase key.** Requirement 3 is
  met inside the app, but the notes are no longer readable by a plain text editor (requirement 2
  fails unless the user edits through the CLI). It also needs a key-management decision.

## Recommendation

Option A with E1. It meets requirements 1 and 2 and keeps R-3. Requirement 3 is met by the
platform, and the app documents that the notes directory must be on an encrypted volume. If the
architect insists on app-level encryption, E2 must be accepted together with a relaxed
requirement 2 and an ADR-0005 exception for the cipher library.

Sync (requirement 1) is in scope only through a folder-sync tool the user runs (e.g. Syncthing).
A notes server stays out of scope, consistent with R-4 being deferred.

## Decision

Pending: architect to choose A or B, and E1 or E2.

## Consequences

If A and E1 are accepted:

- `notes/store.py` changes its storage; QS-1 (crash safety) is re-verified for atomic file
  writes; QS-3 holds (only `store.py` changes).
- ADR-0001 is marked superseded.
- The arc42 requirements table: R-4 moves from deferred to active.
