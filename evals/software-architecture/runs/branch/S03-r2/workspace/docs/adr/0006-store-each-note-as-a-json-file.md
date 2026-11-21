# 6. Store each note as one JSON file

## Status

proposed

## Context

This ADR replaces [ADR-0001 Use SQLite for storage](0001-use-sqlite-for-storage.md). SQLite files
are binary and hard to diff and repair by hand, which the architect ruled out. Notes must still
survive crashes (R-2, QG-1, QS-1), and the program may use only the Python standard library
(R-3, QG-2). ADR-0005 (PostgreSQL) was rejected because a server database contradicts R-3, so
the replacement stays file-based.

## Decision

Store each note in its own UTF-8 text file named `<id>.json` in one notes directory, by default
`~/.notes/` (set `NOTES_DIR` to use another directory). A file holds one JSON object:

```json
{"id": 1, "text": "Buy milk", "created": "2026-11-21T10:00:00+00:00"}
```

- The id is an integer, one more than the highest id in the directory (or 1 for an empty directory).
- Each file is written as [ADR-0004](0004-write-notes-atomically.md) requires: a temporary file in
  the same directory, flushed with `os.fsync`. A new note is then placed with `os.link`, which
  fails if the id is already taken, so an existing note is never overwritten; the temporary file
  is removed afterwards. Changing an existing note uses `os.replace`.
- `list` and `search` read every file in the directory.
- Only `notes/store.py` reads or writes these files (ADR-0003).

## Consequences

- A note file can be read, diffed and corrected in a text editor.
- A crash leaves each note either fully stored or absent (QS-1), and a damaged file affects only
  its own note.
- `search` scans every file on each call and there is no index. Search time grows with the number
  of notes, which is the speed problem ADR-0005 was meant to solve; R-1 may need revisiting for
  large collections.
- Writing a note costs one `fsync` for the file, as in ADR-0004.
- `notes/store.py` must be reimplemented on `json` and `pathlib`, and its tests rewritten. Only
  `notes/store.py` and its tests change (QS-3). The current code still uses `sqlite3` and
  `~/.notes.db` until that is done.
- [ADR-0001](0001-use-sqlite-for-storage.md) is superseded once this ADR is accepted.
- [ADR-0003](0003-cli-reaches-storage-only-through-store.md) still holds; its text mentions
  `sqlite3`, which no longer applies. The rule itself does not change.
