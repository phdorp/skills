# Backup Command Spec

Status: blocked (ADR-0004)
Source: the approved design for `notes backup PATH`, as given in the conversation of 2026-11-22.

## Problem Statement

Users keep notes for years (arc42 section 2 stakeholders). All of a user's notes live in one
SQLite file whose location depends on `NOTES_DB` or `~/.notes.db`. The program offers no command
that writes a copy of that file to a path the user chooses, so a user who wants a copy on another
disk must find the file and copy it by hand. Nothing tells them whether the copy holds all their
notes.

## Solution

A user runs `notes backup PATH`. The command writes a complete copy of the store to PATH, replacing
any file already there, prints the number of notes in the copy, and exits 0. To restore, the user
copies the file back to where the store lives. No restore command is added in this change.

## User Stories

1. As a user, I want to run `notes backup PATH` with a path on another disk, so that I keep a copy of my notes outside my main disk.
2. As a user, I want the command to print the number of notes it backed up, so that I can check the copy is complete.
3. As a user, I want an existing file at PATH replaced, so that I can repeat the backup to the same place without deleting the old copy first.
4. As a user on first use with no notes yet, I want the backup to succeed and print `0`, so that I can back up from day one.
5. As a user, I want a failed or interrupted backup never to leave a partial file at PATH, so that a copy I find there is always a whole store.
6. As a user whose store cannot be read, I want the reason on stderr and exit code 1, so that I can see why the backup failed and scripts can detect it.
7. As a user whose store cannot be read, I want the file already at PATH left untouched, so that my previous backup survives a failed attempt.
8. As a user whose PATH cannot be written (missing directory, no permission, full disk), I want the reason on stderr, exit code 1, and no new or changed file at PATH, so that I know no backup was made.
9. As a user who gives PATH as the store file itself, I want the command refused with an error and exit code 1, so that my live store is never overwritten.
10. As a user restoring, I want to copy the backup file back to the store's location and have `notes list` show my notes, so that restore needs no command.
11. As a user who omits PATH, I want a usage message and nothing written, so that a mistyped command does not create a file.
12. As a user who gives a relative PATH, I want it resolved from the directory I run the command in, as all paths are on the command line.
13. As a user on Linux or macOS with only Python's standard library installed, I want backup to need nothing else, so that it works on locked-down machines (R-3).
14. As a user with a large store, I want the backup to copy every note, with no size limit imposed by the command.
15. As a contributor, I want the backup logic to live in the store module, so that the CLI never touches the database (ADR-0003).

## Implementation Decisions

- **Command**: `backup` takes one positional argument, PATH. It is added to the command set in `notes/cli.py` beside `add`, `list` and `search`. The CLI calls the store; it does not import `sqlite3`.
- **Store**: the store module gains one operation, taking the destination path and returning the number of notes written. It is the only code that reads the database file or writes the backup (ADR-0003).
- **Copy**: the backup is a copy of the whole database file in SQLite's own format (ADR-0001), so restoring is a file copy and the restored file opens with the same store. The copy is taken in a single step from one read of the store, so it is a consistent snapshot even if another process writes during the copy.
- **Atomic write**: the copy is first written to a temporary file in the same directory as PATH, flushed with `os.fsync`, then moved to PATH with `os.replace`, as ADR-0004 requires. Because the temporary file sits beside PATH, the move stays on one filesystem, so it works when PATH is on another disk. On any failure the temporary file is removed and PATH is left as it was.
- **Count**: the printed number is the count of notes in the copy as written, not a separate read of the live store. After a successful run, the number printed equals the number of notes in the file at PATH.
- **Output**: on success, stdout receives the count as a decimal number and a newline, and nothing else. Exit code 0.
- **Errors**: any failure to read the store or write PATH prints `notes: <message>` on stderr and exits 1, as arc42 section 8 requires. The check must cover the read as well as the open: today `main()` wraps only the open in that handler, so a read error in `list` or `search` is not reported this way (see Further Notes).
- **Permissions of the copy**: the file at PATH has the permissions of the temporary file it came from, which the standard library creates owner-readable and owner-writable only (assumption A4).
- **Dependencies**: standard library only (R-3, QG-2). No new third-party package.

## Testing Decisions

- **What makes a good test**: external behaviour through the command line: exit code, stdout, stderr, and the files on disk. A test should not assert how the copy is made.
- **Seam**: the existing `main(argv)` entry point in `notes/cli.py`, with `NOTES_DB` pointing the store at a temporary file. No new seam is proposed; one seam covers every behaviour in this spec.
- **Modules tested**: `notes/cli.py` (command wiring, output, exit codes) and `notes/store.py` through the CLI.
- **Behaviours to test**:
  - success: count printed, exit 0, and a store opened from the copy lists the same notes;
  - empty store: prints `0`, exit 0;
  - an existing file at PATH is replaced;
  - unreadable store (`NOTES_DB` pointing at a file that is not a database): stderr starts with `notes: `, exit 1, and the existing file at PATH keeps its exact bytes;
  - unwritable PATH (parent directory missing): stderr message, exit 1, no file created at PATH, and no temporary file left in the directory;
  - PATH equal to the store file: exit 1, store unchanged;
  - missing PATH: usage message, exit 2, no file written.
- **Failure cases without mocks**: use real bad inputs (a non-database file, a missing directory) rather than patching `os.replace` or `os.fsync`, so tests exercise the real code path.
- **Prior art**: `tests/test_notes.py`, `CliTest.test_add_and_search` (sets `NOTES_DB` with `mock.patch.dict`, calls `main`, captures stdout with `redirect_stdout`) and `StoreTest` (uses `tempfile.mkdtemp`).

### Quality Requirements

- **Serves:** R-2 (no note is lost; a backup is a second copy that survives loss of the main disk)
- **Keeps:** QS-1 (a crash or kill during backup leaves PATH either as it was or holding a complete copy, and the store still opens); QS-2 (works with no install steps on Linux or macOS); QS-3 (the backup logic stays in `notes/store.py` and its tests; `cli.py` changes only to wire the command)
- **Builds on:** ADR-0001 (SQLite file format, standard library), ADR-0002 (decision records), ADR-0003 (the CLI reaches storage only through the store)
- **Blocked by:** ADR-0004 (proposed): it sets the atomic-write rule this command relies on. Implementation waits until the architect accepts it.

## Out of Scope

- A restore command. Restoring is a file copy, as the design states.
- Scheduled or automatic backups.
- Encryption or compression of the backup file.
- Verifying a backup against a checksum after writing it.
- Backing up the PostgreSQL backend in ADR-0005, which is proposed and not built.
- Sync between devices (R-4, deferred).
- Fixing how `list` and `search` report read errors. That is separate work; see Further Notes.

## Further Notes

**Status and blocking**

- Status is `blocked (ADR-0004)`. ADR-0004 is `proposed`. Per ADR-0002, work that depends on an unaccepted decision waits. The architect should accept ADR-0004; the status then changes to `ready-for-agent`.
- The command name `backup`, its exit codes, and the backup file format sit on the central decision list in ADR-0002 ("CLI command names and exit codes", "import and export formats"). No ADR records them. The format is covered by ADR-0001, since the copy is the same SQLite file. The command name and exit codes need the architect's approval. The approved design may already cover them; if so, the architect should say so. I have not drafted a new ADR.

**Assumptions**

These are the questions I would otherwise have asked. The architect may change any of them.

- **A1 (empty or missing store):** the store is opened as every command opens it, so a missing store file is created empty, as `add` and `list` already do. Backup then writes a copy with 0 notes and exits 0.
- **A2 (PATH is the store file):** refused with `notes: ...` on stderr and exit 1, with the store unchanged. The design did not cover this; overwriting the live store would be silent data loss.
- **A3 (unwritable PATH):** a missing directory, a permission failure, or a full disk produces `notes: ...` on stderr, exit 1, and no change at PATH.
- **A4 (permissions):** the copy keeps the owner-only permissions of the temporary file. No group or world access is added.
- **A5 (output):** stdout is the bare count and a newline, matching how `add` prints a bare id.
- **A6 (usage errors):** a missing PATH is a usage error, handled by the argument parser, so the exit code is 2 as for other usage errors. The exit-1 rule covers store and write failures only.
- **A7 (relative PATH):** resolved from the current working directory.
- **A8 (replacement):** an existing file at PATH is replaced without a prompt, as the design states.

**Pre-existing gap**

- `main()` wraps only `Store(...)` construction in its error handler. A read error in `list` or `search` escapes as a traceback. The process still exits 1, but without the `notes: ...` message. Backup must follow the rule itself. Changing `list` and `search` is separate work and is not part of this spec.

**Glossary**

- `GLOSSARY.md` gained the term **Backup** in this change.

**Open for the architect**

- Accept ADR-0004 (unblocks this spec).
- Confirm the command name and exit codes, or record them in an ADR.
- Confirm or change assumptions A1 to A8.
