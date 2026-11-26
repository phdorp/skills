# 4. Store notes as plain text files

## Status

accepted 2026-11-21; supersedes [ADR-0001](0001-use-sqlite-for-storage.md)

## Context

Users want to read and edit their notes with any text editor (R-6). A SQLite file is binary
and cannot be edited that way. Notes must still survive crashes (R-2, QS-1), and the program
may use only the Python standard library (R-3).

## Decision

Each note is one UTF-8 text file in the notes directory, by default `~/.notes/` (set
`NOTES_DIR` to use another directory). The file name is the creation time in UTC,
`YYYYMMDDTHHMMSSffffffZ.txt`, which makes the id unique and gives the newest-first order
without reading the contents. The file content is the note text followed by a newline.

- `add` writes the file to a temporary file in the same directory, flushes it to disk, and
  renames it into place (`os.replace`). A crash leaves the whole note or none of it.
- Files that do not match the time-based name are still listed, using their modification
  time as the creation time, so notes created by hand in an editor are not hidden.
- `notes list` shows the newest notes first. `notes search` keeps oldest-first order.

## Consequences

- Crash safety comes from the atomic rename, not from a database transaction.
- The notes are not encrypted by this decision; see [ADR-0005](0005-encryption-at-rest.md).
- Notes are only as private as the directory permissions and the disk they are on. Files
  are created with mode `0600`.
- Sync (R-4) is still deferred; a plain directory is a simpler base for it later.
- The module that touches the files is still only `notes/store.py` (ADR-0003).
