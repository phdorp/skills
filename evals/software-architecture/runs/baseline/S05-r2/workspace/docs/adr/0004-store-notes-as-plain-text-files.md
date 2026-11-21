# 4. Store notes as plain text files

## Status

accepted 2026-11-21. Supersedes [ADR-0001](0001-use-sqlite-for-storage.md).

## Context

Users must be able to read and edit their notes with any text editor (R-7). A SQLite file is
binary, so it cannot be opened or edited that way. Notes must still survive crashes (R-2, QG-1,
QS-1), and the program may use only the Python standard library (R-3, QG-2).

## Decision

Each note is one UTF-8 text file in a notes directory, by default `~/.notes/` (set `NOTES_DIR`
to use another directory).

- The file name is the note id: the creation time in UTC, `YYYYMMDDTHHMMSSffffffZ`. The id
  orders notes by creation time, so `notes list` shows the newest first (R-8).
- The file content is the note text. One trailing newline added by an editor is ignored.
- A note is written to a hidden temporary file in the same directory, flushed to disk, then
  hard-linked to its final name. `link` fails rather than overwrites an existing file, and the
  temporary file is removed afterwards. A crash leaves either the complete note or no note, plus
  at most a hidden temporary file that listing ignores.
- Files in the directory whose names are not note ids are ignored, so users may keep other files
  there.

## Consequences

Crash safety comes from the write-then-link sequence, not from SQLite transactions. The format
is editable with any editor, and renaming or deleting a file in a text editor changes the notes.
Editing content does not change a note's id, so the order stays stable.

Only `notes/store.py` knows this layout (ADR-0003). Notes are not encrypted by this decision; see
[ADR-0005](0005-encrypt-notes-at-rest.md). Existing SQLite databases are not read or migrated by
this version.
