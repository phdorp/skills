# notes backup Spec

Status: draft, blocked until ADR-0004 is accepted and the `backup` command name has an accepted decision (see Quality Requirements)
Source: the approved design for a backup command, as given in the conversation of 2026-11-22

## Problem Statement

A user's notes live in one file on one disk: the store. If that disk fails, or the file is deleted, every note is lost (R-2). Today the only way to keep a copy elsewhere is to copy the file by hand. That means knowing where the store is, and a hand copy taken while the program is writing can be incomplete. Nothing tells the user whether the copy holds all their notes.

## Solution

A new command, `notes backup PATH`, writes a complete copy of the store to PATH. An existing file at PATH is replaced. On success the command prints the number of notes in the copy and exits 0. On failure it prints the reason on stderr, exits 1, and leaves whatever was at PATH unchanged. The user keeps the copy on another disk. To restore, the user copies the backup file back over the store. There is no restore command yet.

## User Stories

1. As a user, I want to run `notes backup PATH` with a path on another disk, so that a copy of my notes survives a failure of this disk.
2. As a user, I want the command to print how many notes it backed up, so that I can check the copy has the notes I expect.
3. As a user, I want the command to exit 0 on success, so that a script can rely on it.
4. As a user, I want an existing file at PATH replaced without a prompt, so that I can repeat the backup to the same location.
5. As a user, I want the copy to contain every note committed before the command started, so that it is complete and not a half-written snapshot.
6. As a user, I want the backup file to open as a store by itself (for example by setting `NOTES_DB` to it), so that I can check it with the existing commands.
7. As a user, I want a backup of an empty store to succeed and print 0, so that an empty store is not an error.
8. As a user, I want a backup to be either fully written or not written at all. If the command is killed or the disk fills while it runs, the file already at PATH is still the previous file, so a failed backup never destroys an earlier good one.
9. As a user, I want a failed backup to leave no temporary file in PATH's directory, so that the directory stays clean.
10. As a user, I want an unreadable store reported on stderr as `notes: <message>` with exit 1, like every other command's errors.
11. As a user, I want a PATH that is a directory, or whose parent directory does not exist, reported on stderr with exit 1, so that I learn the path is wrong.
12. As a user, I want PATH refused when it is the store file itself, so that a backup cannot overwrite the live store.
13. As a user, I want to restore by a plain file copy, so that recovery needs no extra command.
14. As a user, I want `notes backup` to work on Linux and macOS with only the standard library, so that nothing new is installed (R-3).
15. As a contributor, I want the backup logic in the store module, so that swapping the storage engine changes only the store module and its tests (QS-3).

## Implementation Decisions

- The `cli` block gains one command, `backup`, with one required argument, PATH. It parses the argument, asks the store block for the copy, prints the count, and reports errors on stderr with exit 1 as every command does. It does not use the storage library directly (ADR-0003).
- The `store` block gains the operation that writes the backup, and returns the number of notes in the copy it wrote. It is the only block that knows the storage.
- Snapshot: the copy holds exactly the notes committed before the operation starts. A writer active during the copy must not produce a torn file. The mechanism is left to the plan. The storage library's online backup facility meets this with the standard library; a raw byte copy of a live file does not.
- Format: the backup is the store's own file format (ADR-0001). No new format is introduced, so no export-format decision is needed.
- Atomic write (ADR-0004, proposed): the copy is written to a temporary file in PATH's directory, flushed to disk, then moved over PATH with an atomic replace. Any failure removes the temporary file and leaves PATH as it was.
- Opening the store follows existing behaviour, the same as every other command.
- Output: on success, one line on stdout containing only the integer count (assumption A2).
- Errors: `notes: <message>` on stderr, exit 1.
- No new third-party dependency (R-3).

## Testing Decisions

- Seam: the command entry point, called in-process, with the store path set through the existing environment variable and stdout captured. This is one seam (assumption A1, not confirmed with the user). The atomic-write failure is injected at the replace step, reached through the same entry point.
- Good tests check external behaviour: exit code, stdout, stderr, and the contents of files on disk. A backup is verified by opening it as a store and listing its notes, not by inspecting internals.
- Modules: the command entry point and, through it, the store block. No tests of SQLite internals.
- Behaviours to pin:
  - (a) success: notes copied, count printed, exit 0;
  - (b) an existing file at PATH is replaced;
  - (c) an empty store prints 0;
  - (d) unreadable store: `notes: ` message on stderr, exit 1, PATH untouched;
  - (e) replace fails mid-write: PATH keeps its old content and no temporary file is left behind;
  - (f) PATH is a directory, or its parent is missing: exit 1;
  - (g) PATH equals the store file: refused, exit 1, store unchanged;
  - (h) restore by copy: copying the backup over the store, then listing, shows the same notes.
- Prior art: `tests/test_notes.py`, `CliTest.test_add_and_search` (store path via environment variable, redirected stdout), and `StoreTest.setUp` (temporary store path).

## Quality Requirements

- **Serves:** R-2 (no note is lost; a copy on another disk survives the loss of this one), QG-1, and the stakeholder expectation that users keep notes for years without losing any.
- **Keeps:**
  - QS-1: the atomic-write rule for every file the store writes, and the store still opens after a crash.
  - QS-2: `python3 -m notes backup` needs no install step.
  - QS-3: the backup logic sits in the store block; no other block touches the storage.
- **Builds on:** ADR-0001 (SQLite file, which the backup copies), ADR-0003 (only the store touches the database), ADR-0002 (dependency and command decisions are central).
- **Blocked by:**
  - **ADR-0004**, "Write notes atomically via a temporary file and rename", status `proposed`. The atomic-write requirement rests on it. This spec does not build on it until the architect accepts it.
  - **The `backup` command name.** ADR-0002 lists CLI command names as decided centrally. No accepted ADR records `backup`. The architect must accept an ADR for it, or record acceptance of this spec's command name.
- **Affected by, not blocking:** ADR-0005, "Add a PostgreSQL backend", status `proposed`. A PostgreSQL store is not one file, so "copy the store to PATH" would need a new definition if ADR-0005 is accepted. See Further Notes.

## Out of Scope

- A restore command. A later spec adds it. This spec only ensures the backup file is restorable by copying and opens as a store.
- Scheduled or automatic backups, retention, rotation, and incremental backups.
- Encrypting or compressing the backup.
- Backing up to a remote or synced location (R-4 is deferred).
- Backing up a PostgreSQL store (ADR-0005, proposed).
- Verifying backup contents beyond the count printed.

## Further Notes

**Assumptions.** The user was unavailable, so these were stated rather than asked. The architect should confirm or change each.

- **A1 Seam.** The command entry point, with the store path set through the environment. Not agreed with the user.
- **A2 Output.** A bare integer on one line on stdout, as `add` prints a bare id. The approved design says only "prints the number of notes".
- **A3 Missing store.** Opening follows existing behaviour, which creates an empty store file at the store path. So `notes backup` with no store creates one, writes a backup of 0 notes, and exits 0. The side effect creates a file; the architect may prefer an error.
- **A4 PATH equals the store file.** Refused with exit 1; the store is untouched. The approved design does not cover this case.
- **A5 Relative PATH.** Resolved against the current working directory, as for any path argument.
- **A6 Directory or missing parent.** Exit 1 with a message on stderr.
- **A7 Restore by copy.** The user must not copy over the store while a `notes` command is running. The spec does not guard against it.
- **A8 Command name and argument.** `backup` with one positional PATH, as approved. It still needs the architect's recorded decision (see Quality Requirements).
- **A9 ADR-0004.** Used as the user stated ("as ADR-0004 says"). Its status is still `proposed`, so the blocked-by rule applies until it is accepted.
- **A10 Snapshot mechanism.** Not fixed by the design. The spec requires a consistent snapshot; the plan chooses how.

**Glossary.** "Backup" was added to `GLOSSARY.md`.

**ADR-0005.** If the PostgreSQL backend is accepted, the definition of a backup for that engine must be written before this command supports it.

**Pending for the architect, in order:**
1. Accept ADR-0004, which this spec's atomic-write rule rests on.
2. Record the `backup` command name, per ADR-0002.
3. Confirm assumptions A1 to A4, which the design left open.
