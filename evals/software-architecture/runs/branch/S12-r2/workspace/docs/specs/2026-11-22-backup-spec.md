# Backup Spec

Status: blocked (ADR-0004)
Source: the approved design for `notes backup`, given in the conversation of 2026-11-22.

## Problem Statement

Users keep notes for years (R-2), but the only copy of their notes is the single store file on
the machine they use. A disk failure or a lost laptop loses everything. A user who wants a second
copy on another disk has no supported way to make one that is guaranteed to be whole.

## Solution

A user runs `notes backup PATH`. The command writes a complete copy of the store to PATH and
prints how many notes the copy holds. The user keeps that file on another disk. The copy is the
store itself, so restoring is copying the file back to the store location. A restore command is
not part of this work.

## User Stories

1. As a user, I want to run `notes backup PATH`, so that I get a copy of all my notes at PATH.
2. As a user, I want the command to print the number of notes in the backup, so that I can check it
   against the number I expect.
3. As a user, I want the command to exit 0 when the backup succeeds, so that a script can rely on it.
4. As a user, I want an existing file at PATH replaced by the backup, so that I can reuse one
   backup name for each run.
5. As a user, I want a backup to contain every note the store holds at that moment, so that no note
   is missing from the copy.
6. As a user, I want a backup taken while the store is in use by another `notes add` to be a
   consistent copy, so that it never holds half of a change.
7. As a user, I want a backup of an empty store to succeed and print `0`, so that a fresh install
   can be backed up without special cases.
8. As a user, I want a backup to be a valid store, so that I can copy it back and run `notes list`
   on it.
9. As a user, I want the store to be left unchanged by a backup, so that backing up never costs me
   a note.
10. As a user, I want a failed backup to report the error on stderr and exit 1, so that I know the
    copy was not made.
11. As a user, I want a failed backup to leave any existing file at PATH exactly as it was, so that
    a bad run does not destroy my previous backup.
12. As a user, I want a backup killed partway through (for example by a power cut) to leave PATH
    either as it was or as a complete new backup, never as a partial file, so that a crash cannot
    corrupt my backup (ADR-0004).
13. As a user, I want the command to refuse when the store file does not exist, so that a backup
    does not create an empty store as a side effect.
14. As a user, I want the command to refuse when PATH is the store file itself, so that a backup
    cannot overwrite the notes it copies.
15. As a user, I want the command to refuse when the directory of PATH does not exist or PATH is a
    directory, so that I get a clear error instead of a partial result.
16. As a user, I want the command to report an unreadable or corrupt store on stderr and exit 1, so
    that I know the store, not the backup, is the problem.
17. As a user, I want the command to work with `NOTES_DB` set, so that a backup copies the store I
    am actually using.
18. As a user, I want a missing PATH argument to get the usual usage message, so that the command
    behaves like the others.
19. As a user on Linux or macOS, I want the backup to need no installed packages, so that it works
    on the same locked-down machines as the rest of the program (R-3).
20. As a user, I want the backup file to be a normal file that I can copy to another disk with
    ordinary tools, so that I do not need the program to move it.

## Implementation Decisions

- **Store block**: a new method on `Store` writes the backup and returns the number of notes in it.
  It is the only code that touches the database, so the rule that only the store block uses the
  storage engine holds (ADR-0003).
- **Consistent copy**: the copy is made with the SQLite online backup facility, which the standard
  library provides. It copies one consistent snapshot, so a concurrent writer cannot produce a torn
  copy. A plain file copy of the store file is rejected because it can copy a half-written store.
- **Atomic write (ADR-0004)**: the copy is first written to a temporary file in the same directory
  as PATH, flushed to disk, and then moved over PATH. This applies to the backup file as ADR-0004
  requires for every file the store writes. The temporary file must be in the same directory so the
  final move stays on one filesystem.
- **Store must exist**: the backup does not create the store. If the store file is missing, the
  command fails with an error and writes nothing. Opening the store for backup must not run the
  table creation that `Store` runs on a normal open.
- **Refuse PATH equal to the store**: if PATH names the store file (after resolving the path), the
  command fails with an error and changes nothing.
- **CLI**: a new subcommand `backup` takes one positional argument, PATH. It is dispatched in the
  CLI block alongside `add`, `list` and `search`. The CLI block reaches storage only through `Store`
  (ADR-0003).
- **Output**: on success, the command prints the note count alone on one line to stdout, as a
  decimal integer, and exits 0. Nothing else is printed to stdout.
- **Errors**: every failure prints `notes: <message>` on stderr and exits 1, as arc42 section 8
  requires. Usage errors keep argparse's current behaviour (exit 2) and are not changed.
- **Store path**: the store is located as it is for every other command, through `NOTES_DB` or the
  default path. PATH is taken as given and is not affected by `NOTES_DB`.
- **No schema or format change**: the backup is the store's own SQLite file (ADR-0001). No new
  format is introduced.
- **Quality requirements**: a backup must keep QS-1's guarantee for the backup file: a crash
  during the backup leaves PATH readable as the old file or the complete new one.

## Testing Decisions

What makes a good test here: external behaviour through the seams below. Check what the user sees
(stdout, stderr, exit code) and what is on disk afterwards (the store and PATH). Do not check which
SQLite calls were made.

Seams:

- **Command seam**: `notes.cli.main(["backup", PATH])`, with `NOTES_DB` pointing at a temporary
  store, as the existing CLI test does. This proves output, exit codes, refusal cases, and that the
  store is unchanged. Most behaviour in the user stories is tested here.
- **Store seam**: `Store.backup(path)`, called directly. This proves the returned count, the copy's
  contents, and the atomic-replace behaviour. For the failure cases (the write or the final move
  fails), inject the failure at the point where the store flushes or moves the temporary file, and
  assert that PATH still holds its previous content and no temporary file is left behind. The
  existing store tests are prior art for setup and teardown.
- No new seam is proposed. Both tests above use seams that already exist (`main` and `Store`).

Modules tested: the store block (`Store`) and the CLI block (`main`). The test for a killed process
(SIGKILL during backup) follows the QS-1 test pattern if one exists; if not, it is out of scope for
the first version and the in-process failure test stands in for it.

Prior art: `tests/test_notes.py`, class `StoreTest` for store behaviour and class `CliTest` for
command behaviour, including the `NOTES_DB` setup.

## Quality Requirements

- **Serves:** R-2 (no note is lost), R-3 (standard library only)
- **Keeps:** QS-1 (a crash leaves the store and the backup readable), QS-3 (only the store block and
  its tests change for the storage engine)
- **Builds on:** ADR-0001 (SQLite file, atomic transactions), ADR-0003 (CLI reaches storage only
  through `Store`)
- **Blocked by:** ADR-0004 (write notes atomically via a temporary file and rename; currently
  `proposed`). The atomic write in this spec depends on it. Implementation waits until the architect
  accepts ADR-0004.

## Out of Scope

- A restore command. A user restores by copying the file back. A restore command is a later spec.
- Automatic or scheduled backups, and backup rotation or retention.
- Compression or encryption of the backup file.
- Verifying the backup beyond the count printed. The command does not reopen the copy to check it.
- Backups of the PostgreSQL backend (ADR-0005 is `proposed`). This spec covers the SQLite store only.
- Sync between devices (R-4, deferred).

## Further Notes

Open assumptions, stated because the author could not ask. Each one is a choice the architect can
change before implementation starts:

1. **Missing store**: a missing store file is an error, not an empty backup (story 13).
2. **Output format**: stdout is the count alone on one line (story 2). The brief said "prints the
   number" and did not give a format.
3. **Refuse PATH = store** (story 14). The brief did not cover this case.
4. **Symlink at PATH**: the move replaces the symlink itself, not what it points to.
5. **Existing PATH**: replaced whatever its content, since the command does not read it.
6. **Leftover temporary file**: a crash can leave a temporary file beside PATH. Later runs do not
   clean it up. This matches ADR-0004 (the target is never partial) and is not a bug.
7. **Count source**: the count comes from the same snapshot that is copied, not from a second read.
8. **Command name and exit codes**: ADR-0002 lists CLI command names and exit codes as decided
   centrally. No ADR records `backup` yet. The approved design is taken as the architect's decision.
   The architect should record it in an ADR, or confirm it in ADR-0004's review.

Open decisions: none left to the implementer. Items 1 to 8 above are stated assumptions, not
deferred decisions. The architect should confirm or change them before implementation.

Blocking: ADR-0004 must be accepted before implementation starts. Writing this spec does not depend
on it.

Glossary: "Backup" added to `GLOSSARY.md`.
