# Notes Backup Spec

Status: blocked on ADR-0004 (proposed). The body is ready for review. Implementation waits until the architect accepts ADR-0004.
Source: the approved design for `notes backup PATH`, as given in the session on 2026-11-22.

## Problem Statement

Users keep their notes in one file on one disk. If that disk fails or the machine is lost, every note is lost with it, and users keep notes for years (R-2). Today the only way to make a second copy is to find the store file by hand (`~/.notes.db`, or wherever `NOTES_DB` points), copy it while no command is writing, and trust that the copy is complete. Most users will not do that, and those who try cannot tell whether the copy is good.

## Solution

`notes backup PATH` writes a complete copy of the note store to PATH, for example a file on another disk. It prints the number of notes it copied and exits 0. An existing file at PATH is replaced. The copy is either complete or not written at all: if anything fails, the file at PATH stays as it was. There is no restore command yet. To restore, the user copies the backup file back to the store path. Nothing else about `add`, `list` or `search` changes.

## User Stories

1. As a user, I want to copy my notes to a path on another disk, so that a failure of my main disk does not lose them.
2. As a user, I want the backup to print how many notes it copied, so that I can check the copy against my notes.
3. As a user, I want a successful backup to exit 0, so that a script can rely on the exit code.
4. As a user with an earlier backup at PATH, I want the new backup to replace that file, so that I keep one up-to-date copy in one place without deleting the old one first.
5. As a user with an empty store, I want the backup to succeed and print 0, so that an empty store needs no special handling.
6. As a user who runs backup before adding any note, I want it to work the same way, so that the first run is not an error. (The store is created empty when it does not exist yet; see Further Notes.)
7. As a user whose store cannot be read (corrupt, or not a notes store at all), I want the backup to report the error on stderr and exit 1, so that I know no copy was made.
8. As a user, if the backup fails partway (disk full, process killed, interrupted), I want the file at PATH to be exactly what it was before, so that I never end up with a half-written backup that looks valid.
9. As a user, if the backup fails, I want no temporary files left behind next to PATH, so that the folder stays clean.
10. As a user who gives a PATH whose folder does not exist or cannot be written, I want an error on stderr, exit 1, and no file created, so that I can fix the path and retry.
11. As a user who gives a PATH that is an existing directory, I want an error on stderr and exit 1, with nothing written inside the directory.
12. As a user who gives the store's own file as PATH by mistake, I want the backup refused with an error and exit 1, so that my notes are not overwritten.
13. As a user, I want a backup to leave my store unchanged (same notes, same file), so that running backup at any time is safe.
14. As a user, I want the backup file to be a complete note store in the same format, so that restoring it is only a copy back to the store path.
15. As a user who adds notes while a backup runs, I want the backup to be a consistent snapshot, so that it never holds a partly written note.
16. As a user who forgets PATH, I want the usual usage error (exit 2, as the argument parser gives every command), so that the failure looks like the other commands' failures.
17. As a user reading help, I want `notes --help` to list `backup` with a one-line description, so that I can find the command.
18. As a user with `NOTES_DB` set, I want the backup to copy the store that `NOTES_DB` points to, so that backup works like the other commands.

## Implementation Decisions

- **CLI block**: a new `backup` command takes one required argument, PATH, and has a one-line help text. The CLI block parses it, calls the store to make the backup, prints the count, and maps errors to stderr and exit 1, as it does for every command (arc42 section 8).
- **Store block**: the store gains a backup operation. Only the store block reads the database file (ADR-0003), so the CLI never copies the file itself.
- **Snapshot**: the store writes a consistent snapshot of the database through SQLite's own backup facility, not a byte copy of the file. A byte copy of a database another process may be writing can be inconsistent, and restoring from one would be unsafe.
- **Atomic write**: the snapshot goes to a temporary file in the same directory as PATH, is flushed to disk, and is then moved over PATH in one step, as ADR-0004 requires for any file the store writes. The temporary file is removed if any step fails. (ADR-0004 is proposed; see Blocked by.)
- **Count**: the number printed is the number of notes in the snapshot. It is the only thing printed, on stdout, followed by a newline.
- **Path rules**: PATH is refused before anything is written when it is an existing directory, or when it refers to the store's own file. Any other PATH is accepted; a missing or unwritable folder fails in the write step.
- **Error rule**: opening, reading or writing the store, or moving the temporary file into place, all produce `notes: <message>` on stderr, exit 1, and nothing on stdout. A failure leaves PATH as it was.
- **Backup file format**: the backup is a store in the same SQLite format (ADR-0001), so restore is a file copy. The format and the command name are decisions ADR-0002 leaves to the architect; see Further Notes.
- **No new dependencies**: the feature uses the Python standard library only (R-3, QS-2).
- **Unchanged**: the `Note` model, the schema, and the behaviour of `add`, `list` and `search`.

## Testing Decisions

- **Seam**: `cli.main(argv)` with `NOTES_DB` pointing at a temporary store. This is the highest seam, and it proves what users see. It is the same seam `CliTest.test_add_and_search` uses. No new seam is needed.
- **Checking the backup**: open the backup file with the public `Store` class and read its notes with `all()`. Do not inspect the temporary file or call private helpers.
- **What to test** (behaviours, not implementation):
  - A store with two notes: the backup prints `2`, returns 0, and the backup file holds both notes.
  - An existing file at PATH with other content: after a successful backup it is a valid store with the notes.
  - An empty store: prints `0`, returns 0.
  - Backup does not change the store: same notes after the backup.
  - `NOTES_DB` holds a file that is not a database: stdout is empty, stderr starts with `notes: `, the return value is 1, and an existing file at PATH keeps its content.
  - PATH is an existing directory: stderr message, return 1, directory contents unchanged.
  - PATH is the store's own file: stderr message, return 1, store intact.
  - Failure at the move step: an existing file at PATH keeps its content, return 1, and no temporary file remains beside it. This test has to make the move step fail, for example by patching the replace call to raise. It is the one place a test reaches below the seam, because a real crash cannot be produced otherwise.
- **Prior art**: `tests/test_notes.py`, classes `StoreTest` and `CliTest`. Use `unittest`, `tempfile.mkdtemp()`, and `mock.patch.dict(os.environ, {"NOTES_DB": ...})`, as the existing tests do.
- **Isolation**: no test may touch the user's real `~/.notes.db`.
- **Gate**: the suite runs with `python3 -m unittest`.

## Quality Requirements

- **Serves:** R-2 (no note is lost). A copy on another disk protects against losing the machine or its disk.
- **Keeps:** QS-1 (the store still opens after a failure), QS-2 (no install steps, standard library only), QS-3 (only the store block touches the database; the CLI only calls the store).
- **Builds on:** ADR-0001 (SQLite file format), ADR-0002 (command names and exit codes are decided centrally), ADR-0003 (only the store touches the database).
- **Blocked by:** ADR-0004 (write notes atomically). It is proposed, so it is an open decision. Implementation waits until the architect accepts it.

## Out of Scope

- A restore command. Restoring is a file copy by the user, for now.
- Scheduled or automatic backups, backup rotation, retention, compression, and encryption.
- Backing up the PostgreSQL backend (ADR-0005 is proposed, and no such backend exists yet).
- Note sync between devices (R-4 is deferred).
- Checking that PATH is on a different disk from the store.
- Fixing error reporting for `add`, `list` and `search`. Today a store error after the store opens can escape as a traceback instead of the `notes: <message>` form. That is a real gap. It should be a separate spec or ticket, not part of this work.

## Further Notes

**Blocked by ADR-0004.** ADR-0004 is still `proposed` in `docs/adr/`. This spec follows it because the approved design relies on it, but it cannot be treated as accepted until the architect accepts it. Until then, the spec status stays `blocked`.

**Command name and file format have no accepted ADR.** ADR-0002 says CLI command names and import and export formats are decided centrally, by an accepted ADR. The `backup` command name and the backup file format have no such ADR. The approved design is taken as the architect's decision, but the architect should confirm it, by accepting an ADR or by adding it to ADR-0002. Confirm this before implementation.

**Assumptions made without the architect.** The request asked for assumptions to be stated where a question would otherwise be asked. Each one below can be changed by the architect before implementation starts.

- A1. Success output is the count alone, on stdout, with a trailing newline. Failure output is `notes: <message>` on stderr.
- A2. The count is the number of notes in the snapshot, taken from the same read that makes the copy.
- A3. The copy is a consistent snapshot through SQLite's backup facility, so it is correct even if another process writes during the backup. A byte copy of the file is not used.
- A4. The temporary file is created in PATH's directory, so the final move is within one filesystem and atomic.
- A5. A PATH that is an existing directory is refused with exit 1. A PATH whose folder is missing or unwritable fails in the write step, with exit 1 and no file created.
- A6. A PATH that refers to the store's own file is refused with exit 1 before any write, so the store is never overwritten by its own backup.
- A7. The store is opened as the other commands open it. If the store file does not exist, it is created empty and the backup prints `0`. This matches what `add`, `list` and `search` already do. The side effect of creating the file at the store path is kept as it is.
- A8. A missing PATH is an argument-parser usage error, exit 2, like every other command's usage error today.
- A9. If PATH is a symbolic link, the link is replaced and its target is not written. This is how the atomic move behaves.
- A10. The backup file is not encrypted and is not restricted in permissions beyond what the file system gives a new file. The notes are readable to anyone who can read the file.

No open decision is deferred to a named person. Each assumption above is the decision as written.

**Glossary.** No new term was added to `GLOSSARY.md`. "Backup" is used as an ordinary word, so no glossary entry is needed yet. Add one through domain-modeling if the architect wants the term defined.

**Tracker.** The repo has no `docs/agents/issue-tracker.md`, so the spec is published as a local file. No tickets or plan were written, because the work is one slice in one sitting. Those can follow once the ADR is accepted.
