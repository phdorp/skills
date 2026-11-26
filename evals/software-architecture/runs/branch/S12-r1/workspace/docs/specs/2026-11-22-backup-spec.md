# Notes Backup Spec

Status: blocked (ADR-0004)
Source: the approved design for `notes backup`, given in conversation on 2026-11-22

## Problem Statement

A user's notes live in one store file on one disk. If that disk fails or is lost, every note is
gone, and the user has no copy to restore from. Users who keep notes for years (R-2) want a
second copy on another disk, but today the only way to make one is to copy the store file by
hand, which risks copying it while a command is writing to it.

## Solution

A user runs `notes backup PATH`. The command writes a complete, consistent copy of the store to
PATH, replacing any file already there, and prints how many notes it backed up. The user keeps
that file on another disk. To restore, the user copies the file back to the store's location.
There is no restore command yet.

## User Stories

1. As a user, I want to run `notes backup PATH`, so that I have a copy of my notes on another disk.
2. As a user, I want the command to print the number of notes backed up, so that I can confirm the copy holds what I expect.
3. As a user, I want the command to exit 0 when the backup succeeds, so that scripts can rely on it.
4. As a user, I want a backup to replace an older backup at the same PATH, so that I can reuse one file name for each backup.
5. As a user with no notes yet, I want a backup to succeed and report 0, so that an empty store is still backed up.
6. As a user, I want a backup taken while another `notes` command is writing to the store to be a consistent copy, so that the backup never contains half of a write.
7. As a user, I want a backup to be restorable by copying the file back over the store, so that I need no extra tool to restore.
8. As a user, I want a failed backup to leave any existing file at PATH unchanged, so that a failed run never destroys my previous backup.
9. As a user, I want a crash or kill during a backup to leave PATH holding either the old file or the complete new one, so that I never find a partial backup (QS-1).
10. As a user whose store cannot be read, I want the error on stderr and exit code 1, so that I know the backup did not happen.
11. As a user who gives a PATH whose directory does not exist, or that is not writable, or that is a directory, I want an error on stderr and exit code 1, so that I know where the problem is.
12. As a user who gives PATH equal to the store's own file, I want the command refused with an error and exit code 1, so that the store is never overwritten by its own copy.
13. As a user who runs `notes backup` without a PATH, I want the usual usage message, so that I learn the command needs a PATH.
14. As a user on a locked-down Linux or macOS machine, I want the command to work with only the Python standard library, so that I install nothing new (R-3, QS-2).
15. As a user whose backup target is on another disk, I want the backup to land there complete, so that the other disk can be unplugged afterwards.

## Implementation Decisions

- **Backup format.** The backup is a SQLite database file with the same schema as the store, so that copying it back over the store yields a working store. It is produced with SQLite's own backup facility, which copies a consistent snapshot even while another process writes. This is the store's existing on-disk format (ADR-0001); it is not a new format. See Further Notes, assumption A1.
- **Where the logic lives.** The store block performs the backup: it reads the store and writes the backup file. The CLI block parses the `backup` subcommand, calls the store, prints the count, and maps errors to stderr and exit code 1. The CLI block does not touch the database directly (ADR-0003).
- **Count.** The number printed is the number of notes in the snapshot the backup was taken from, as an integer on its own line on stdout.
- **Atomic write.** The backup file is written to a temporary file, flushed to disk, and moved onto PATH in one step, as ADR-0004 requires for every file the store writes. The temporary file is created in the same directory as PATH, not in the store's directory, so the final move works when PATH is on another disk. ADR-0004 is `proposed`; see Quality Requirements.
- **Store not created by backup.** Backup reads an existing store. If the store file does not exist, backup fails with an error. This differs from `list` and `add`, which create an empty store on first use. See A4.
- **Refusals.** Backup refuses, with an error and exit code 1, when PATH is the store's own file, when PATH is a directory, and when PATH's directory is missing or not writable. In each refusal, no file at PATH is created, changed, or removed.
- **Error reporting.** Every failure prints `notes: <message>` on stderr and exits 1, as arc42 section 8 requires. A missing `PATH` argument is a usage error and exits with the argument parser's usual code (2), as it does for every command today.
- **Permissions.** The backup file has owner-only read and write permission. See A7.
- **Interfaces that change.** The store gains one operation: back up to a given path, returning the note count. The CLI gains one subcommand, `backup`, taking one positional PATH. No existing command changes its output or exit codes.

## Testing Decisions

- **What makes a good test.** Test what a user or a restoring user can observe: the file at PATH, the printed count, the exit code, the stderr message, and whether the backup can be used as a store. Do not test which SQLite calls were made.
- **Seams.**
  - The highest seam is the existing CLI entry point, called with an argument list, with the store location set through the existing environment variable. It proves the command, output, exit codes, and error messages. It is the main seam.
  - The existing store seam (a `Store` opened on a temporary file) proves the backup operation itself and the count.
  - One failure-injection test at the store seam proves the atomic-write guarantee: a failure at the final move leaves the previous file at PATH unchanged. This test replaces the move step with a failing stand-in. It is the only test that reaches below the public behaviour, because a kill cannot be staged reliably in a unit test.
- **Modules tested.** The store block (backup operation, refusals, atomic write) and the CLI block (subcommand, printed count, exit codes, stderr messages).
- **Cases that must have a test:**
  - backup then restore by copying the file back: `list` on the restored store shows all notes;
  - the printed count equals the number of notes; exit code 0;
  - an existing file at PATH is replaced;
  - an empty store backs up with count 0 and exit code 0;
  - a missing store: stderr message, exit code 1, no file created at PATH;
  - PATH's directory missing: stderr message, exit code 1;
  - PATH is the store's own file: refused, exit code 1, store unchanged;
  - PATH is a directory: stderr message, exit code 1;
  - a failure at the final move: the previous file at PATH is byte-for-byte unchanged;
  - `backup` without PATH: exit code 2.
- **Prior art.** `tests/test_notes.py`: `StoreTest` (temporary-file store, `add`/`all`/`search`) and `CliTest.test_add_and_search` (environment-variable store location, `main` with an argument list, captured stdout). New tests follow these patterns in the same file or a sibling file.
- **Standard library only.** Tests use `unittest` and the standard library, as the rest of the suite does.

## Quality Requirements

- **Serves:** R-2 (no note is lost; a backup is the copy that survives a lost disk), R-3 (standard library only, Linux and macOS).
- **Keeps:** QS-1 (a crash during the backup leaves PATH either as it was or as a complete backup, and the store still opens; measure: 0 unreadable files in 100 trials), QS-2 (works on a fresh machine with no install steps), QS-3 (the backup logic sits in the store block; only the store block, the CLI block, and their tests change).
- **Builds on:** ADR-0001 (one SQLite file as the storage format), ADR-0003 (the CLI reaches storage only through the store).
- **Blocked by:** ADR-0004 (write notes atomically via a temporary file and rename). It is `proposed`. The atomic-write rule in this spec depends on it. Implementation waits until the architect accepts ADR-0004. Per ADR-0002, work that depends on a decision on the centrally decided list waits for its ADR.

## Out of Scope

- A restore command. Restore is copying the file back, as the design states. A restore command, if wanted, is a separate spec.
- Scheduled or automatic backups.
- Compression, encryption, or a backup format other than the SQLite file.
- Verifying a backup beyond the printed count (no checksum or integrity command).
- Backing up the PostgreSQL backend. ADR-0005 is `proposed` and no such backend exists.
- Incremental backups, backup rotation, or pruning old backups.

## Further Notes

Assumptions made because the author was not available to confirm them. Each one is for the architect to confirm or change before implementation.

- **A1. Format is the store's own format, so no new ADR.** ADR-0002 lists import and export formats as centrally decided. This spec treats a backup as a copy in the existing on-disk format (ADR-0001), not a new export format, so it needs no new ADR. If the architect sees a backup as an export format, a new ADR is needed before implementation.
- **A2. PATH equal to the store's file is refused.** The design does not say. Refusing keeps the store from being replaced by its own copy while another connection has it open.
- **A3. Failures are reported, not retried.** PATH's directory missing, not writable, or PATH being a directory each give an error and exit 1. No directory is created for the user.
- **A4. A missing store is an error for backup.** The design says only "if the store cannot be read". Backup does not create an empty store as a side effect, because that would write a store file the user did not ask for. Confirm this differs from `list`/`add` behaviour as intended.
- **A5. Output format.** The count is printed as a bare integer on its own line on stdout. The design says "prints the number of notes backed up" and does not fix a wording. The count is an integer, with no prefix text, so scripts can read it directly.
- **A6. Temporary file location.** The temporary file is in PATH's directory, so the final move stays on one disk. ADR-0004 says "in the same directory"; this spec reads that as the destination's directory.
- **A7. Permissions.** The backup holds all notes, so it is owner-only (0600), the default for a temporary file. The design does not say.
- **A8. Crash leftovers.** If the process is killed during a backup, a temporary file may remain in PATH's directory. PATH itself is never partial. Cleanup of such leftovers is not required; handled errors remove their temporary file.
- **A9. Concurrent writers.** A backup started while another process writes to the store gives a consistent snapshot of some point in time, not necessarily the latest note. The design does not say which point.
- **A10. The count** is the number of notes in that snapshot, so it matches what the backup file holds.

Open until the architect answers: A1 (whether a new ADR is needed) and the acceptance of ADR-0004. The rest can be changed at implementation review without reopening the design.
