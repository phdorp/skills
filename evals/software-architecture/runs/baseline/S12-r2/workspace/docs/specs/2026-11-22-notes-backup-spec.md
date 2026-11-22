# Notes Backup Spec

Status: ready-for-agent. Implementation is blocked until ADR-0004 is accepted (see Further Notes, item 1).
Source: the approved design for `notes backup`, given in the conversation of 2026-11-22.

### Problem Statement

Notes are kept in one SQLite file (ADR-0001). A user who loses that file, or the disk it sits on, loses every note. Users who keep notes for years (R-2) have no supported way to keep a second copy on another disk. They can copy the file by hand, but they do not know that a copy taken while the program writes can be torn, and the program gives them no count to check the copy against.

### Solution

`notes backup PATH` writes a copy of the store to PATH. The copy is complete or absent, never partial. The command prints how many notes the copy holds and exits 0. To restore, the user copies the file back over the store. No restore command exists yet.

### User Stories

1. As a user, I want to run `notes backup PATH`, so that I have a copy of my notes on another disk.
2. As a user, I want the command to print the number of notes in the copy, so that I can check the copy holds what I expect.
3. As a user, I want the command to exit 0 when the copy is written, so that scripts can rely on it.
4. As a user with a previous backup at PATH, I want the new backup to replace that file, so that I do not have to delete it first.
5. As a user with an empty store, I want the backup to succeed and print 0, so that an empty store is backed up like any other.
6. As a user with many notes, I want the copy to hold every note, so that restoring it gives back everything.
7. As a user, I want the copy to be a complete snapshot, so that a note added while the backup runs is either in the copy or not, and the copy always opens.
8. As a user, I want to restore by copying the backup file over my store path, so that I need no restore command.
9. As a user whose store is at a path set by `NOTES_DB`, I want the backup to copy that store, so that the setting applies to backup too.
10. As a user whose store file does not exist yet, I want an error on stderr and exit 1, so that I learn there is nothing to back up and no empty store is created as a side effect.
11. As a user whose store is unreadable (for example a corrupt file), I want the error on stderr, exit 1, and any existing file at PATH left unchanged, so that a failed backup never destroys a good backup.
12. As a user whose PATH is in a directory that does not exist, I want an error on stderr and exit 1, so that I can correct the path.
13. As a user whose PATH is an existing directory, I want an error on stderr and exit 1, so that the directory is not touched.
14. As a user who gives the store's own path as PATH, I want an error on stderr and exit 1 with the store unchanged, so that the store is never replaced by a copy of itself.
15. As a user whose disk fills up or whose PATH is not writable during the copy, I want an error on stderr, exit 1, the existing file at PATH unchanged, and no temporary file left in the directory.
16. As a user, I want the backup file readable only by my account, so that my notes are not exposed by default.

### Implementation Decisions

- **Store module.** The backup operation belongs to the store module. ADR-0003 forbids the CLI from touching the database file. The CLI parses `backup PATH`, calls the store, prints the count, and maps errors as it does for every command.
- **Consistent snapshot.** The copy is made with SQLite's online backup facility in one step, from the open store. The result is a point-in-time snapshot even if another process writes during the copy.
- **Atomic write (ADR-0004).** The copy is first written to a temporary file in the same directory as PATH, flushed with `os.fsync`, and moved onto PATH with `os.replace`. The temporary file must be in PATH's directory so the replace stays on one filesystem. The temporary file is removed if any step fails.
- **File format.** The backup file is a SQLite database with the same schema as the store. Restoring is a plain file copy, so the format must be the store format and nothing else.
- **Count.** The count printed is the number of rows in the `notes` table of the finished copy, read from the copy, not from the source. Printed alone on stdout followed by a newline, matching how `add` prints its id.
- **Exit codes and errors.** Success exits 0. Every failure prints `notes: <message>` on stderr and exits 1. The existing error path covers only opening the store; the backup's errors (write, rename, path checks) must go through the same reporting.
- **No side effects on failure.** On any failure, PATH keeps its previous content (or stays absent) and no temporary file remains in its directory.
- **Missing store.** The backup does not create the store file. If it does not exist, the command fails with exit 1. This differs from today's open behaviour, which creates an empty store, so the existence check must come before the store is opened.
- **Same path.** If PATH resolves to the store file, the command fails with exit 1 and changes nothing.
- **Permissions.** The backup file gets owner-only permissions (0600), the default for a newly created temporary file.
- **Dependencies.** Standard library only (R-3).

### Testing Decisions

- **Seam.** The CLI entry point `main(argv)` with `NOTES_DB` pointed at a temporary store, as `CliTest.test_add_and_search` does in `tests/test_notes.py`. This is the one seam; all behaviours below are tested through it, with no mocking.
- **Behaviours to pin:**
  - `backup` prints the note count and returns 0 (stories 1–3).
  - The copy, opened with `Store`, holds the same notes as the source (stories 6, 8).
  - An existing file at PATH is replaced (story 4).
  - An empty store backs up and prints `0` (story 5).
  - `NOTES_DB` selects the source store (story 9).
  - A missing store exits 1, prints to stderr, and creates neither the store nor PATH (story 10).
  - A corrupt store exits 1, leaves an existing PATH byte-for-byte unchanged, and leaves no temporary file in the directory (story 11).
  - A PATH in a missing directory exits 1 (story 12).
  - A PATH that is an existing directory exits 1 and the directory is unchanged (story 13).
  - A PATH equal to the store exits 1 and the store is unchanged (story 14).
- **Not unit-tested.** Crash safety (a kill mid-write) and the 0600 mode are checked by inspection of the write sequence and by a manual run. Story 15 (disk full) is not reproducible without mocking, so it is covered by the corrupt-store and unwritable-target cases above.
- **Prior art.** `tests/test_notes.py`: `StoreTest` for store behaviour and `CliTest` for command behaviour, using `tempfile.mkdtemp()` and `mock.patch.dict(os.environ, ...)`.

### Out of Scope

- A restore command (story 8 covers restore by file copy only).
- Backup of other stores, such as a PostgreSQL store (ADR-0005 is proposed and not implemented).
- Scheduling, rotation, or retention of backups.
- Encryption or compression of the backup file.
- A text or JSON export format (a separate export decision under ADR-0002).
- Prompting before replacing an existing file.
- A directory `fsync` after the rename. ADR-0004 does not require it.

### Further Notes

1. **ADR-0004 is still `proposed`.** This spec relies on its atomic-write rule. ADR-0002 says work depending on an undecided ADR waits until the architect accepts it. Accepting ADR-0004 is the architect's decision; I have not changed its status.
2. **Central decisions without an ADR.** ADR-0002 lists CLI command names, exit codes, and import/export formats as decisions needing an accepted ADR. The `backup` command, its exit codes, and the backup file format are not recorded in any ADR. They should be recorded (a new ADR, or an amendment to ADR-0004) before implementation.
3. **Assumptions made without you.** Each is stated in the body and can be reversed:
   - A missing store is an error, not a reason to create an empty store (story 10).
   - Backing up onto the store's own path is an error (story 14).
   - The backup file is owner-only, 0600 (story 16).
   - The count is printed as a bare number, like `add` prints an id (Implementation Decisions).
   - The backup file has the store's schema, so restore is a file copy (Implementation Decisions).
4. **Existing gap, not fixed here.** The CLI reports only store-open errors in the `notes: <message>` form. Errors raised by `add`, `list`, or `search` after the store opens still surface as tracebacks. This spec does not change that.
5. **Glossary.** "Backup" and "backup file" are used here but not defined in `GLOSSARY.md`. They should be added through the domain-modeling skill.
