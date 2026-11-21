# 4. Export notes as JSON Lines through an `export` command

## Status

proposed

## Context

Users want to back up their notes and move them to other tools (new requirement, named in
words here; not yet an ID in arc42 section 1). The export must not lose data (R-2), must run
on the standard library only (R-3), and must keep the storage behind `Store` (ADR-0003). The
file format and the command name are centrally decided (ADR-0002), so they need this ADR.

## Decision

We will export all notes with `python3 -m notes export [PATH]`.

- **Format:** JSON Lines, UTF-8, one JSON object per note, one object per line, each ending in
  `\n`. Keys are exactly the `Note` fields: `id` (integer), `text` (string), `created` (string,
  as stored). Notes are ordered by ascending `id`. An empty store produces an empty file.
- **Destination:** with no `PATH` or `PATH` = `-`, write to stdout. With a `PATH`, write to a
  temporary file in the same directory, flush and `fsync` it, then `os.replace` it onto `PATH`.
- **Existing file:** if `PATH` exists, print `notes: <path> already exists` to stderr and exit
  1 without touching it. There is no overwrite flag in this version.
- **Exit codes:** 0 on success; 1 on any error, reported as `notes: <message>` on stderr
  (arc42 section 8).
- **Data access:** `notes/cli.py` calls `Store.all()` and serializes the `Note` values with
  the standard `json` module. No change to `notes/store.py` and no `sqlite3` import in the CLI.

Not in this decision: import, other formats (CSV, Markdown), export filtered by search term.
Each needs its own ADR if wanted.

## Consequences

- Backups are plain text, readable and diffable with any editor, and convert to other tools
  with a short script. JSON Lines keeps `text` lossless, because newlines inside a note are
  escaped as `\n`.
- Writing to a temporary file and renaming it means a crash during export leaves either the
  complete file or no file at `PATH`, never a partial one (same goal as QS-1).
- The format is a public contract once users rely on it. Changing a key or its type needs a
  new ADR.
- No change to ADR-0001 (storage) or ADR-0003 (store boundary). The CLI building block in
  arc42 section 5 is unchanged.
- The "users back up and move notes" requirement must be confirmed by the architect and added
  to arc42 section 1 before this ADR is accepted.
- A future import command would read the same format; it is not decided here.
