# Backup Command Spec

Status: blocked (ADR-0004)
Source: the approved design for `notes backup PATH`, given in the spec request of 2026-11-22 (conversation). The architect was not available, so every point where a question would have been asked is stated below as an assumption.

### Problem Statement

The store is one binary file in the user's home directory (ADR-0001). A user who wants a copy of their notes on another disk must find that file and copy it by hand. A plain copy can be cut short, and a copy made while notes are being added may not match the store. Nothing tells the user whether the copy is complete or how many notes it holds. A user who loses their machine loses every note they have not copied, and an interrupted copy can leave a damaged file where the old copy was.

### Solution

`notes backup PATH` writes a complete copy of the store to PATH and prints how many notes the copy holds. If the copy fails, the command says why, exits 1, and leaves any file already at PATH as it was. To restore, the user copies the backup file back over the store location. No restore command exists in this version.

### User Stories

1. As a user, I want to run `notes backup PATH` and get a copy of all my notes at PATH, so that I can keep the copy on another disk.
2. As a user, I want the command to print the number of notes in the backup, so that I can check the copy holds what I expect.
3. As a user, I want the command to exit 0 when the backup succeeds, so that scripts can rely on it.
4. As a user with an earlier backup at PATH, I want the new backup to replace it, so that I do not have to delete the old file first.
5. As a user, I want the earlier backup at PATH to stay intact when a new backup fails, so that a failed run never destroys my last good copy.
6. As a user whose store is in use by a running `notes add`, I want the backup to be a consistent copy, so that it neither lacks a note that was committed before the backup started nor contains a half-written one.
7. As a user with a new install and no notes yet, I want backup to succeed and print `0`, so that the command works from day one.
8. As a user whose store file is damaged or is not a notes store, I want the error on stderr as `notes: <message>` and exit 1, so that I know no backup was made.
9. As a user whose PATH is in a directory that does not exist, I want an error on stderr and exit 1, with no file left at PATH and no temporary file left in any directory.
10. As a user whose PATH is a directory or a file I may not write, I want an error on stderr and exit 1, so that the failure is visible.
11. As a user who gives the store file itself as PATH, I want the command to refuse with an error and exit 1, so that the store is never overwritten by its own backup.
12. As a user who sets `NOTES_DB`, I want backup to copy the store that `NOTES_DB` names, so that the backup matches the store I use.
13. As a user, I want backup to leave the store unchanged, so that running it never costs me a note.
14. As a user restoring from a backup, I want the backup file to open as a store with the same notes, so that restoring is only a copy.
15. As a user with a large store, I want the backup to contain every note, so that size does not truncate the copy.
16. As a user who runs `notes backup` with no PATH, I want the usage message that every command gives for missing arguments, so that I see how to use the command.
17. As a contributor, I want the database to be read only in `notes/store.py`, so that the CLI reaches storage only through the store (ADR-0003).
18. As a contributor, I want the backup to use only the standard library, so that users install nothing new (R-3, QS-2).

### Implementation Decisions

- **Store** gains one operation: given a destination path, it writes a complete copy of the store to that path and returns the number of notes in the copy. It is the only module that reads the database for this, per ADR-0003.
- **Atomic write**: ADR-0004 governs the write. The copy goes to a temporary file in the same directory as PATH, is flushed to disk, and is then moved over PATH. A failure at any step leaves the previous file at PATH unchanged and removes the temporary file. ADR-0004 is `proposed`; see Blocked by and Further Notes.
- **Consistent snapshot**: the copy must be a consistent snapshot of the store, even if another process writes while the copy is made. The mechanism is left to the plan.
- **Count**: the number printed is the number of notes in the backup file, not a separate count taken from the store.
- **CLI**: a new `backup` command takes one required PATH argument. It opens the store as every other command does, calls the store operation, prints the count on stdout as a bare integer followed by a newline (as `add` prints a bare id), and returns 0.
- **Errors**: any error from the store operation is reported as `notes: <message>` on stderr and returns 1. The CLI today catches errors only while opening the store; the backup step must be covered by the same handling, so no traceback reaches the user.
- **Refusal of the store path**: if PATH names the same file as the store, the command fails with an error and exit 1 before writing anything.
- **Path handling**: PATH is used as given, relative to the current directory. The shell expands `~`; the program does not.
- **Source**: the store is the file `NOTES_DB` names, or the default path when it is unset.
- **Dependencies**: standard library only (R-3).
- **Command name and exit codes**: ADR-0002 lists CLI command names and exit codes as decided centrally. No accepted ADR covers `backup`. See Further Notes.

### Testing Decisions

What makes a good test here: observable behaviour through the existing entry points: the exit code, what is printed on stdout and stderr, and the bytes at PATH. Tests must not inspect temporary files or internal calls.

Seams: no new seam is proposed. Two existing seams are used:

- `notes.cli.main` with `NOTES_DB` set, the seam `CliTest` already uses. It proves the command's exit codes, output, and error messages.
- `notes.store.Store`, the seam `StoreTest` already uses. It proves the copy's contents, the count, and the replace-on-failure rule.

Behaviours to test:

- backup of a store with notes creates PATH, prints the count, and exits 0;
- the backup file opens as a store and lists the same notes;
- backup replaces an existing file at PATH;
- backup of an empty store prints `0` and exits 0;
- a store that is not a notes store exits 1, writes the error to stderr, and leaves an existing file at PATH byte-identical;
- PATH in a missing directory exits 1 with an error on stderr and leaves no file behind;
- PATH equal to the store file exits 1 and leaves the store unchanged;
- `backup` with no PATH follows argparse's usage error (exit 2, as the existing commands do);
- the store's notes are unchanged after a backup.

Prior art: `tests/test_notes.py`, `StoreTest` (setUp with a temporary database) and `CliTest.test_add_and_search` (`NOTES_DB` set through `mock.patch.dict`).

Atomicity is checked by the failure test above and by review against ADR-0004. A kill-during-backup test in the style of QS-1 is not required by this spec; the plan may add one.

### Quality Requirements

- **Serves:** R-2 (no note is lost; a user-kept copy protects against loss of the machine). The arc42 requirements list has no backup requirement; see Further Notes.
- **Keeps:** QS-1 (the store and any backup file are never left partial, as ADR-0004 extends it to every file the store writes); QS-2 (no install steps; standard library only); QS-3 (the database is touched only in `notes/store.py`; `cli.py` gains only the command and its handling).
- **Builds on:** ADR-0001 (SQLite store), ADR-0002 (decision list), ADR-0003 (CLI reaches storage only through the store).
- **Blocked by:** ADR-0004 (Write notes atomically via a temporary file and rename), status `proposed`. The architect must accept it before implementation.

### Out of Scope

- A restore command. Restore is a manual copy in this version.
- Automatic or scheduled backups, retention, or rotation of old backups.
- Compression, encryption, or checksums of the backup file.
- Backup of the PostgreSQL backend in ADR-0005, which is `proposed`.
- Sync between devices (R-4, deferred).
- Verifying a backup beyond the note count.
- An fsync of the directory after the replace. ADR-0004 requires only the file flush; a later ADR may add more.

### Further Notes

**Blocked by.** The status is `blocked (ADR-0004)` because ADR-0004 is `proposed`. Once the architect accepts it, change the status to `ready-for-agent`. Only the architect can accept it.

**Central decision needing an ADR.** ADR-0002 lists CLI command names and exit codes as decided centrally, and requires an accepted ADR before work that depends on them. No ADR covers `backup`. The architect should accept an ADR for the command name, the output format, and the exit codes, or confirm this spec as that record. This spec does not draft one.

**Assumptions**, made because the architect was not available. Each is a decision the architect can change:

1. The number is printed as a bare integer on its own line, matching `add`.
2. A failure to write PATH (missing directory, no permission, PATH is a directory) exits 1 with `notes: <message>` on stderr, the same as a store read failure. The request names only the read case.
3. PATH equal to the store file is refused (exit 1), because the backup would overwrite the store.
4. A missing store is opened as every command opens it, so it is created empty and backed up as `0`. This means backup can create the default store file. It is the existing behaviour of every command.
5. The backup file gets the default permissions of a new file, as the store does. It is not made private. A user who wants it private can set `umask`.
6. Usage errors (no PATH) exit 2 through argparse, as the existing commands do for missing arguments. The exit-1 rule covers store and write errors only.
7. A backup of a store that another process has locked for writing is not specified beyond the consistent-snapshot rule.

**Requirements.** arc42 section 1 has no requirement for backup. The architect may want one (for example R-6, "users keep a copy of their notes on another disk"). This spec cites R-2 and does not add a requirement, since requirements belong to the architect.

**Restore.** A backup is a SQLite file, not text (ADR-0001), so it cannot be checked or edited by hand. The user restores by copying it over the store location while no `notes` command is running.
