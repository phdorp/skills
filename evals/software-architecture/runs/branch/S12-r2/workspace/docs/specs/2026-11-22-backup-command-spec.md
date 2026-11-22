# Backup Command Spec

Status: blocked. Do not implement until ADR-0004 is accepted and the `backup` command name is settled (see Quality Requirements).
Source: approved design in the conversation of 2026-11-22 (`notes backup PATH`). The architect was not available to answer questions; every gap is stated as an assumption under Further Notes.

## Problem Statement

Users keep notes for years (arc42 stakeholders) and must not lose any (R-2). The store is one SQLite file in `~/.notes.db` on the same disk as everything else. A user who wants a second copy on another disk has to know where the file is and copy it by hand. Copying a database file while the program may be writing to it can produce a copy that does not open or is missing recent notes, and the tool gives no way to check it.

## Solution

The user runs `notes backup PATH`. The command writes a complete, readable copy of the store to PATH and prints how many notes it holds. If PATH already holds a file, that file is replaced. If the store cannot be read, or the copy cannot be written, the command says why on stderr and exits 1, and PATH is left as it was. To restore, the user copies the backup file back to the store's location (`NOTES_DB` or `~/.notes.db`). There is no restore command.

## User Stories

1. As a user, I want to run `notes backup PATH` with a path on another disk, so that I have a copy of my notes if the main disk fails.
2. As a user, I want the command to print the number of notes in the copy, so that I can confirm it is complete.
3. As a user, I want the command to exit 0 when the copy is written, so that a script can rely on it.
4. As a user who backs up every week, I want a second run to replace the earlier backup at the same PATH, so that I do not have to delete it first.
5. As a user with a new, empty store, I want the backup to succeed and print `0`, so that an empty store is not reported as an error.
6. As a user, I want a backup I can restore by copying the file back to the store's location, so that I need no extra tool to restore.
7. As a user, I want a failed or interrupted backup to leave the previous backup at PATH intact, so that a failure never leaves me with no usable copy.
8. As a user whose store cannot be read (missing permission, corrupt file, or not a database), I want an error on stderr and exit 1, so that I know the backup was not made.
9. As a user who gives a PATH in a directory that does not exist or cannot be written, I want an error on stderr and exit 1 with the store untouched, so that I can fix the path and retry.
10. As a user who gives a directory as PATH, I want an error on stderr and exit 1, so that no directory is replaced or damaged.
11. As a user who gives the store's own file as PATH, I want an error on stderr and exit 1, so that the live store is never overwritten by its own copy.
12. As a user who gives a relative PATH, I want it resolved from the directory I ran the command in, so that it behaves like any other file argument.
13. As a user with many notes, I want the backup to finish without a size limit, so that a large store can be backed up.
14. As a user who runs `notes backup` with no PATH, I want the usage message from the argument parser and exit 2, as every command already does for usage errors.
15. As a user backing up while another `notes` command is writing, I want the copy to contain a consistent set of notes (no half-written note), so that the backup is restorable.

## Implementation Decisions

- **Store owns the copy.** `Store` gains one operation that takes a destination path and returns the number of notes written. Only `notes/store.py` imports `sqlite3` (ADR-0003). The CLI calls this operation and does not touch the database.
- **CLI gains one subcommand.** `backup` takes one required argument, PATH. It calls the store operation and prints the returned count as a bare integer followed by a newline on stdout, then exits 0. Errors go to stderr as `notes: <message>` and exit 1, as in arc42 section 8.
- **The copy is a SQLite database.** It has the same format as the store (ADR-0001), so restoring is a file copy and needs no conversion.
- **Consistent copy.** The copy is made with SQLite's online backup, which reads a consistent snapshot of the store, so a concurrent write cannot produce a half-copied file.
- **Atomic write, per ADR-0004.** The copy is first written to a temporary file in the same directory as PATH, flushed with `os.fsync`, then moved onto PATH with `os.replace`. The temporary file is removed if any step fails. Any failure leaves PATH as it was.
- **Count from the file.** The printed count is the number of rows in the notes table of the temporary copy, read before the move. The number printed is therefore the number of notes in the file at PATH.
- **No new dependency.** Only the standard library is used (R-3). No new third-party package (arc42 section 2).
- **No new storage engine behaviour.** The command reads the store through the existing open path, so it inherits the existing behaviour for missing or unreadable store files (see Further Notes).

## Testing Decisions

What makes a good test here: observable behaviour at the command boundary and at the store's public operation: the return value, the output, the exit code, the stderr text, and whether PATH is replaced or left unchanged. Do not assert on the temporary file name or on SQL text.

Seams (no new seam is proposed; both already exist):

- **`notes.cli.main(argv)`**, the command seam. Tests set `NOTES_DB` to a temporary file (as `CliTest` does) and capture stdout and stderr.
- **`notes.store.Store`**, the storage seam. Tests open a store in a temporary directory (as `StoreTest` does).

Modules tested:

- `notes/cli.py`: the `backup` subcommand: success output and exit 0; store unreadable gives stderr and exit 1; PATH is a directory gives exit 1; PATH is the store file gives exit 1 and the store is unchanged; missing usage argument gives exit 2.
- `notes/store.py`: the store operation returns the number of notes; the copy opens as a `Store` and lists the same notes in the same order; an existing file at PATH is replaced; with an injected failure during the move (for example `os.replace` raising `OSError`), the previous file at PATH is byte-for-byte unchanged and no temporary file remains in the directory.

Prior art: `tests/test_notes.py`, classes `StoreTest` (store behaviour through `Store`) and `CliTest` (commands through `main` with `NOTES_DB` patched via `mock.patch.dict`).

Not tested automatically: that `os.fsync` reaches the disk. This is verified by reading the code.

## Quality Requirements

- **Serves:** R-2 (no note is lost; a copy protects against loss of the main store), R-3 (standard library only).
- **Keeps:** QS-1 (a crash during backup leaves PATH either as it was or fully replaced, never partial, and the store still opens). QG-1 applies to the store, not only to `add`.
- **Builds on:** ADR-0001 (SQLite file format), ADR-0003 (only `store.py` touches the database), ADR-0002 (accepted; its list of centrally decided items includes CLI command names and exit codes).
- **Blocked by:**
  - **ADR-0004** (`docs/adr/0004-write-notes-atomically.md`, status `proposed`). The atomic write rule in this spec is ADR-0004's rule. The spec is not built on an unaccepted ADR. The architect must accept ADR-0004.
  - **A decision for the `backup` command name.** ADR-0002 lists CLI command names and exit codes as central decisions. No ADR records the `backup` command yet. The architect must accept a decision (an ADR, or an amendment) before implementation.

## Out of Scope

- A restore command. Restoring is a file copy by the user (stated requirement).
- Scheduled or automatic backups.
- Backup to a remote location or any sync between devices (R-4 is deferred).
- Compression, encryption, or incremental backups.
- Backing up the PostgreSQL backend (ADR-0005, proposed). If that backend is accepted, its backup is a separate spec.
- Verifying the backup beyond the count printed (no integrity check command).

## Further Notes

Assumptions made because the architect was not available. Each is a recommendation the architect should confirm or change before implementation:

1. **Output format.** stdout is the bare count and a newline (for example `3`), mirroring `add`, which prints the new note's id.
2. **Any failure exits 1.** Both a store read error and a write error to PATH (missing directory, no permission, disk full) print `notes: <message>` on stderr and exit 1. The user named the store-read case; the write case is assumed to follow the same rule.
3. **Missing store file.** The store opens through the same path as every command, which creates an empty store if the file does not exist. So `notes backup PATH` on a machine with no store writes a copy with zero notes, prints `0`, exits 0, and leaves an empty `~/.notes.db` behind. This is the existing side effect of opening the store, not new behaviour. Recommendation: accept it now. If the architect prefers to refuse, the command would need a check before the store is opened.
4. **PATH equal to the store file** is refused with exit 1 and the store is left unchanged. Overwriting the live store with its own copy is never wanted.
5. **Symlink at PATH.** The link is replaced, not the file it points to (the behaviour of `os.replace`).
6. **Relative PATH** is resolved from the current working directory.
7. **Argument errors** (no PATH, extra arguments) keep argparse's behaviour, which exits 2 before the store is touched.
8. **Store with a large number of notes** is copied in one operation with no progress output.

Notes for the builder:

- ADR-0003 and QS-3: QS-3 says that swapping the storage engine changes only `store.py` and its tests. The new operation is part of the store's interface, so a future engine must implement it too. This is expected, not a conflict.
- Restore is a file copy while no `notes` command is running. The spec does not require the command to refuse while the store is open. If that matters, it is a new requirement.
