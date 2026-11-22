# Backup Command Spec

Status: ready-for-agent, blocked by ADR-0004 (proposed, not yet accepted). Do not start the atomic-write work until the architect accepts it.
Source: the approved design passed to `/sa:spec-and-plan` on 2026-11-22. The architect was unavailable; every point where a question would have been asked is stated as an assumption under Further Notes.

## Problem Statement

Notes are kept in one file on one disk (`~/.notes.db`, or the path in `NOTES_DB`). If that disk fails or the file is lost, every note is lost. Users who keep notes for years have no simple way to keep a second copy on another disk, and no way to check that such a copy holds everything.

## Solution

A user runs `notes backup PATH`. The command writes a complete copy of the note store to PATH and prints how many notes the copy holds. An existing file at PATH is replaced. If anything goes wrong, the command says so on stderr and exits 1, and the user's existing store and any earlier backup at PATH are left as they were. Restoring is done by hand: the user copies the backup file back over the store file. There is no restore command in this version.

## User Stories

1. As a user, I want to run `notes backup PATH`, so that I keep a copy of my notes on another disk.
2. As a user, I want the command to print the number of notes backed up, so that I can check the copy is complete.
3. As a user, I want the printed number to equal the number of notes in the backup file, so that the count can be trusted.
4. As a user who already has a backup at PATH, I want the new backup to replace it, so that I do not have to delete the old file first.
5. As a user with an empty store, I want the backup to succeed and print `0`, so that an empty store is not an error.
6. As a user whose store cannot be read, I want an error on stderr and exit code 1, so that I know no backup was made.
7. As a user whose PATH cannot be written (the directory does not exist, it is read-only, or PATH is a directory), I want an error on stderr and exit code 1, and my earlier backup at PATH left intact.
8. As a user whose backup is interrupted by a crash, power loss or kill, I want PATH to hold either the old backup or the complete new one, never a partial file, so that a backup I later rely on is never truncated.
9. As a user who passes the store's own file as PATH, I want the command refused with an error and exit code 1, so that the store is not overwritten.
10. As a user, I want no temporary files left in PATH's directory after a success or a failure.
11. As a user, I want to restore by copying the backup file over my store file, and then `notes list` to show every note from the backup.
12. As a user who gives a relative PATH, I want it resolved from the directory I ran the command in.
13. As a user with no PATH argument, I want the usual argparse usage error, so that the command behaves like the other subcommands.
14. As a user on Linux or macOS, I want backup to work with only the Python standard library, so that no install step is needed (R-3).
15. As a contributor, I want the CLI to reach the store only through the `Store` class, so that only `notes/store.py` knows about SQLite (ADR-0003).

## Implementation Decisions

- **Store method.** `Store` gains one method that takes a target path and returns the number of notes written to it. It is the only code that reads the database for the backup. `notes/cli.py` does not import `sqlite3`.
- **How the copy is made.** The method uses SQLite's online backup facility to copy the open store into a temporary file. This gives a consistent copy even if another process writes during the copy. The backup file is a SQLite database in the same format as the store (ADR-0001), so restoring by copying the file back works.
- **Atomic write (ADR-0004).** The temporary file is created in the same directory as PATH and flushed to disk before it is moved into place with a single rename over PATH. On any failure the temporary file is removed and PATH is not touched. This applies ADR-0004's rule to a file the store writes other than the database.
- **Count.** The number returned is counted from the temporary file, after the copy and before the rename, so the printed number matches the file the user receives.
- **Refusing the store itself.** If PATH resolves to the same file as the store, the method raises an error before writing anything.
- **CLI.** A new subcommand `backup` takes one positional argument, `path`. On success it prints the count on stdout as a single line containing only the integer, and returns exit code 0. On any error it prints `notes: <message>` on stderr and returns exit code 1.
- **Error handling covers the copy and the write, not only opening the store.** Today `cli.py` catches only errors from opening the store. The backup subcommand must also catch errors raised while copying and writing, so that every failure follows the stated error convention (arc42 section 8).
- **Store opening is unchanged.** The store is opened through `default_path()` as for every other command, which honours `NOTES_DB`. Opening creates the store file if it does not exist (see Further Notes).
- **Permissions.** The backup file is created with the temporary-file default (readable and writable by the owner only). It is not given the store file's permissions.

## Testing Decisions

- **What makes a good test here.** Test observable behaviour: exit code, stdout, stderr, the bytes and content of the file at PATH, and the list of files in PATH's directory. Do not test which SQLite call is made.
- **Seams.** Use the existing seams and add none:
  - `notes.cli.main(argv)` with `NOTES_DB` pointed at a temporary database. This is the highest seam and proves the command.
  - `notes.store.Store(path)` for the method itself, which needs a store with known notes.
- **Modules tested.**
  - CLI: exit 0 and the count line on stdout; replacement of an existing file; exit 1 with `notes: ` on stderr for an unreadable store, an unwritable PATH, a PATH that is a directory, and PATH equal to the store file; no leftover temporary file after success or failure; an existing PATH unchanged after a failure.
  - Store: the method returns the number of notes; the file written can be opened with `Store` and returns the same notes; an empty store returns 0.
  - Restore by hand: copy the backup over the store path, then `main(["list"])` shows the notes.
  - Atomicity: make the rename step fail (for example by injecting a failure into the rename call) and check that the earlier file at PATH is unchanged and no temporary file remains.
- **Prior art.** `tests/test_notes.py`: `StoreTest` builds a store in a temporary directory; `CliTest.test_add_and_search` sets `NOTES_DB` with `mock.patch.dict(os.environ, ...)` and captures stdout with `redirect_stdout`. Follow both patterns. Tests run with `python3 -m unittest`.

## Quality Requirements

- **Serves:** R-2 (no note is lost when the process or machine crashes; a backup is one way to make that hold beyond one disk); R-3 (standard library only).
- **Keeps:** QS-1 (a crash during the backup leaves PATH either old or complete and the store still opens; the same rule as QS-1 applied to the backup); QS-3 (the backup code lives in `notes/store.py`, with the CLI change confined to `notes/cli.py`).
- **Builds on:** ADR-0001 (SQLite file format and crash safety); ADR-0003 (only `notes/store.py` touches SQLite); ADR-0002 (error reporting and the central list of CLI command names and exit codes).
- **Blocked by:** ADR-0004 (*Write notes atomically via a temporary file and rename*, status proposed). The atomic-write requirement in this spec rests on it. The architect must accept it before implementation of that part begins. If it is rejected, the atomic requirement is withdrawn and this spec must be revised.

## Out of Scope

- A restore command, including any check that a file is a valid backup before it is copied over the store.
- Scheduled or automatic backups.
- Backup to a server, sync between devices (R-4, deferred), or a cloud location.
- Encryption or compression of the backup file.
- Incremental backups.
- Backing up more than one store at once.
- A confirmation prompt before replacing an existing file at PATH. Replacement is immediate, as the design states.
- PostgreSQL backend (ADR-0005, proposed). Backup covers the SQLite store only.

## Further Notes

**Assumptions** (the architect was unavailable; each choice below is what this spec adopts, and each can be changed when the architect returns):

1. **Stdout format.** The command prints only the integer and a newline, as `add` prints only the new id. It does not print a sentence.
2. **Missing store.** The store is opened as every other command opens it, so a missing store file is created empty and backed up as `0` notes with exit code 0. This is consistent with the other commands, but it creates a file in the user's home directory as a side effect of `backup`. The architect may prefer an error for a missing store instead.
3. **Write failures.** Failures while writing PATH (missing directory, no permission, PATH is a directory, disk full) are reported as `notes: <message>` with exit code 1. The design only names the unreadable-store case; this extends the same rule to write failures.
4. **PATH equal to the store.** Refused with exit code 1 and the store untouched. The design does not name this case.
5. **Symbolic link at PATH.** The link itself is replaced, not followed, because the rename replaces the directory entry. The design does not say.
6. **Relative PATH.** Resolved from the current directory.
7. **Backup file format.** The backup is the store's own SQLite file, so no new file format is introduced. ADR-0002 lists import and export formats as central decisions. The architect should confirm that a backup of the existing format does not need its own ADR.
8. **Command name and exit codes.** The design fixes the name `backup` and exit codes 0 and 1. ADR-0002 lists CLI command names and exit codes as central decisions, but no ADR records this command yet. The architect's approval of the design is taken as the decision. If the architect wants it recorded, that needs a new ADR.

**Open items for the architect:**

- Accept or reject ADR-0004. This is a blocker for the atomic-write part (see Quality Requirements).
- Confirm or change assumptions 1 to 8 above.
- Decide whether the term "backup" should be added to `GLOSSARY.md`. It was not added in this pass; the glossary change should go through domain modelling.

**Not produced in this pass:** tickets and an implementation plan. The request asked for the spec only. The work is one slice, so the spec can go straight to a plan once the architect accepts ADR-0004 and confirms the assumptions.

**Tracker:** no tracker configuration exists in this repo (`docs/agents/issue-tracker.md` is absent), so the spec is published as a local file.
