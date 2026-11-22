# Backup Command Spec

Status: ready-for-agent (blocked on ADR-0004 acceptance; see Further Notes)
Source: the approved design in the conversation of 2026-11-22, which this spec restates.
Related: ADR-0002 (decisions reserved for the architect), ADR-0003 (CLI reaches storage only through `Store`), ADR-0004 (atomic writes), arc42 QG-1 / QS-1 (no note lost).

### Problem Statement

A user's notes live in one file on one disk. If that disk fails, is lost, or is replaced, every note is gone, and the user has no copy to fall back on. Users who want a second copy on another disk must find the store file themselves, know where `notes` keeps it, and copy it while no command is writing to it. Most do not, so their notes are only one disk failure away from loss.

### Solution

`notes backup PATH` writes a copy of the note store to PATH. The user points PATH at a file on another disk, runs the command, and gets a count of the notes in the copy. Running the command again replaces the earlier copy at the same PATH. A failed backup never damages the previous copy or the live store. To restore, the user copies the backup file back over the store file. No restore command exists yet.

### User Stories

1. As a user, I want to run `notes backup PATH` and get a copy of my notes at PATH, so that I have a second copy on another disk.
2. As a user, I want the command to print how many notes it backed up, so that I can confirm the copy holds every note I expect.
3. As a user with a store that has no notes yet, I want the backup to succeed and print `0`, so that a scheduled backup script does not fail on a new store.
4. As a user who backs up to the same path each time, I want an existing file at PATH replaced, so that I do not have to delete the old copy first.
5. As a user, I want the backup file to be either the complete new copy or the untouched old one, so that an interrupted backup never leaves a damaged file in place of my last good copy.
6. As a user whose store cannot be read (corrupt, not a notes store, or unreadable permissions), I want an error on stderr and exit code 1, so that a script can detect the failed backup, and my previous copy at PATH is left as it was.
7. As a user whose PATH cannot be written (directory missing, no write permission, or PATH is a directory), I want an error on stderr and exit code 1, and any existing file at PATH unchanged.
8. As a user who runs `backup` before ever adding a note, I want an error and exit code 1 instead of a new empty store being created at the store path, so that backup never silently creates files in my home directory.
9. As a user who accidentally gives the store's own path as PATH, I want the command to refuse with an error and exit code 1, so that my live store is not overwritten by its own copy.
10. As a user restoring after data loss, I want to copy the backup file over my store file and find every note again, so that restore needs no command of its own.
11. As a user who runs `backup` while another `notes` command is adding a note, I want the backup to hold a consistent snapshot, so that the copy is never a torn mix of states.
12. As a user on a shared machine, I want the backup file readable only by me, so that other accounts cannot read my notes.
13. As a user who omits PATH, I want the usage error that every other command gives, with exit code 2, so that the command behaves like the rest of the CLI.

### Implementation Decisions

- **Command**: a new subcommand `backup` with one required positional argument, `PATH`. Its help text describes it as copying the store to PATH. The CLI decides the output and exit code; the store decides the copy.
- **Storage boundary**: the copy is made by the `store` block, not by `cli` (ADR-0003). `store` exposes one operation that takes a destination path and returns the number of notes it wrote. `cli` calls only that operation and prints the result.
- **Snapshot**: the copy is taken through SQLite's online backup mechanism, so it is a consistent snapshot even if another process writes during the copy. A plain byte copy of the store file is not used.
- **Atomic write**: follows ADR-0004 exactly. The snapshot is written to a temporary file in the same directory as PATH, the temporary file is flushed with `os.fsync`, and it is moved to PATH with `os.replace`. The temporary file is created in PATH's directory so the rename stays on one filesystem.
- **Note count**: the number printed is the count of notes in the temporary file, after the snapshot is written and before the rename. The count describes exactly what was copied.
- **Output**: on success, stdout gets the count as a bare integer and a newline, with no other text. This matches `add`, which prints the new id and nothing else. Exit code 0.
- **Errors**: any failure prints one line to stderr in the form `notes: <message>` and exits with code 1, as every command does (arc42 section 8). On failure the temporary file is removed and PATH is not changed.
- **Missing store**: if the store file does not exist, the command fails with exit code 1 and creates neither the store nor PATH. The check happens before the store is opened, because opening a store creates its file.
- **Self-copy refusal**: if PATH resolves to the same file as the store, the command fails with exit code 1 before writing anything.
- **Format**: the backup file is a SQLite database file in the same format as the store. It is not a new export format.
- **Permissions**: the backup file has owner read and write only, the default for a temporary file created this way.
- **Schema**: no change. The backup copies the existing `notes` table as it is.
- **Restore**: no code. Restore is a file copy that the user performs while no `notes` command is running.
- **Backend**: the command reads the SQLite store. It has no branch for other backends; ADR-0005 is only proposed and no other backend exists.

### Testing Decisions

- **Seam**: the existing CLI entry point, `main(argv)`, with the store location set through the `NOTES_DB` environment variable, as `CliTest.test_add_and_search` does. This is the highest seam that proves the behaviour: it covers argument parsing, the output, the exit code, and the store. One further test patches the rename step inside `notes/store.py` to fail, because nothing above that seam can show that an interrupted write leaves the old file in place. No new seam is introduced.
- **Good tests** check what a user can observe: the return value, stdout, stderr, the files on disk, and whether a copied store opens and lists the same notes. They do not assert which SQLite calls were made.
- **Tests to write** (each in `tests/test_notes.py`, in the `CliTest` class or a new `BackupTest` class beside it):
  - Backup copies every note: two notes added, then `main(["backup", p])` returns 0, stdout is `2\n`, and `Store(p).all()` returns both notes with the same ids, text, and timestamps.
  - Empty store: `main(["backup", p])` returns 0 and stdout is `0\n`.
  - Existing file replaced: `p` holds `junk`; after a successful backup, `p` is a valid store with the notes.
  - Repeat backup replaces the earlier copy: a second backup after one more note prints the new count.
  - Unreadable store: `NOTES_DB` points at a file of non-SQLite bytes; the command returns 1, stderr starts with `notes: `, and `p` is not created.
  - Missing store: `NOTES_DB` points at a path that does not exist; the command returns 1, neither that path nor `p` is created.
  - Self-copy refused: `p` is the store path; the command returns 1 and the store is unchanged.
  - Unwritable PATH: PATH's directory does not exist, and separately PATH is an existing directory; each returns 1 with a stderr message, and nothing is created or changed.
  - Failed rename leaves old file: `p` holds a valid old copy; `notes.store.os.replace` is patched to raise `OSError`; the command returns 1, `p` still holds the old copy, and no temporary file remains in the directory.
  - Restore by copy: back up, then copy `p` over the store path; a fresh `Store` lists the same notes.
  - Missing PATH: `main(["backup"])` raises `SystemExit` with code 2, as argparse does for the other commands.
- **Prior art**: `tests/test_notes.py`, `StoreTest` and `CliTest`. Use `tempfile.mkdtemp()` for paths, as they do.
- **Not tested here**: a real SIGKILL during backup, as QS-1 does for `add`. It is a useful later check, but it is not required for this spec.

### Out of Scope

- A restore command. Restore is a file copy until a later spec adds one.
- Scheduled or automatic backups, and backup rotation or retention.
- Compression, encryption, or checksums of the backup file.
- Listing, verifying, or reading back backups.
- Backing up several stores in one run.
- Sync between devices (R-4, deferred).
- A PostgreSQL backend (ADR-0005, proposed). If it is accepted, backup for that backend is a separate spec.
- A size limit or progress output for large stores.

### Further Notes

**Blocker: ADR-0004 status.** `docs/adr/0004-write-notes-atomically.md` reads `proposed`. ADR-0002 says work that depends on an unaccepted decision waits until the ADR is accepted. This spec depends on ADR-0004 for its atomic-write rule. The architect should accept ADR-0004 before implementation starts. The command name `backup`, its exit codes, and the fact that the output is a SQLite file are on ADR-0002's list of centrally decided items. They are covered by this spec, which the approved design restates. No separate ADR is written for them.

**Assumptions made without asking** (the owner was not available to answer these; each is the most likely reading of the approved design and can be changed by editing this section):

1. A missing store file is an error (exit 1), not an empty backup. The current `Store` opens and creates its file, so the backup must check for the store before opening it.
2. A PATH that resolves to the store file is refused (exit 1). Without this check, `os.replace` would overwrite the live store.
3. Any write failure after the store is read (missing directory, no permission, PATH is a directory, disk full) is an error with exit 1, and PATH is left unchanged.
4. Output is the bare integer and a newline, not a sentence. A user who wants a sentence can wrap the command.
5. PATH is taken as given: relative paths are relative to the working directory, and `~` is expanded by the shell.
6. A usage error (missing PATH) exits 2 through argparse, as the other commands do today. Exit 1 is used only for store and write errors.
7. The backup file is private (owner read and write only). This follows from the temporary-file default and is stated so it is a deliberate choice.
8. The count comes from the file that was written, not from a second read of the store, so the printed count always matches the copy.

**Glossary.** The term **Backup** is added to `GLOSSARY.md`.

**Rollout.** No migration. The command is new and does not change the store format.

**Open for the architect.** Whether the backup file counts as an export format under ADR-0002. This spec treats it as a copy of the store, not an export. If the architect disagrees, an ADR is needed before implementation.
