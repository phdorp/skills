# 4. Export notes as JSON Lines through an `export` command

## Status

accepted 2026-11-21

## Context

Users ask to export their notes so they can back them up and move them to other tools (R-6).
An export is also a second copy of the notes, so it must not lose or alter any note (R-2, QG-1).
The program may use only the Python standard library (R-3, QG-2).

Each note has three values: an integer id, text that may contain any character including
newlines, and a creation time stored as ISO 8601 UTC with second precision. The format must carry
all three without loss and must be readable by a line-based tool and by a future `import`.

Candidate formats:

- **JSON Lines** (one JSON object per line, UTF-8): keeps types, escapes newlines and quotes,
  is streamable, and `json` ships with the standard library.
- **CSV**: opened by spreadsheets and many importers, but every value is text and column
  conventions vary between tools.
- **JSON array**: lossless, but must be held in full and is awkward to append or stream.
- **Markdown**: readable by people, but has no reliable round trip for multi-line text.

## Decision

1. **Format.** An export is a UTF-8 file with LF line endings. Each line is one JSON object
   with exactly these keys, in this order:

   ```json
   {"id": 1, "text": "Buy milk", "created": "2026-10-01T10:00:00+00:00"}
   ```

   `id` is the note id as an integer, `text` is the note text unchanged, and `created` is the
   stored value unchanged. Notes appear in ascending `id`, the order `Store.all()` returns.
   Characters are written as-is (`ensure_ascii=False`), not escaped to `\uXXXX`.
   An empty store produces an empty file.

2. **Command.** `python3 -m notes export` writes to standard output, so it can be redirected
   (`python3 -m notes export > notes.jsonl`). `python3 -m notes export --output PATH` writes to
   the file at `PATH` instead.

3. **Safety.** `--output` never overwrites an existing file; it fails with
   `notes: <path> already exists` on stderr and exit code 1. The file is written to a temporary
   file in the same directory and renamed into place only after every line is written, so a
   crash leaves either the complete export or no file at `PATH`.

4. **Exit codes.** `0` on success. `1` on any error, reported on stderr as `notes: <message>`
   (arc42 section 8), in the same way as the other commands.

5. **Architecture.** `notes/export.py` turns a sequence of `Note` values into JSON Lines text.
   It imports only `notes.model`. `notes/cli.py` gets the notes from `Store.all()`, as ADR-0003
   requires, and passes them to `notes/export.py`. The dependency rule becomes:
   `cli` → `store` → `model`, and `cli` → `export` → `model`.

6. **Compatibility.** Readers must ignore keys they do not know. A future change that adds a
   key is therefore compatible. Renaming or removing a key, or changing the meaning of one,
   needs a new ADR.

## Consequences

- A backup is a plain text file that any editor, `jq`, or a spreadsheet's JSON import can read.
  Other tools can convert it without this program.
- The format has no header, so the file does not say which program or version wrote it. Key
  compatibility (decision 6) is the only versioning mechanism.
- Import is not decided here. A later `import` command needs its own ADR, and it must read the
  format above.
- Adding CSV or Markdown output later is a new decision, not a change to this one.
- The atomic write (decision 3) depends on the target directory allowing a temporary file. If it
  does not, `export` fails with exit code 1 and writes nothing.
- Acceptance check for the first implementation: export a store of notes containing commas,
  quotes, newlines, and non-ASCII text, then read the file back line by line with `json.loads`.
  Every note must match the store exactly, with no extra or missing notes.
