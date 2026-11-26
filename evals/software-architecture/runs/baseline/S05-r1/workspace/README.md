# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list        # newest first
python3 -m notes search milk
```

Each note is a plain text file in `~/.notes/` (set `NOTES_DIR` to use another directory), so
you can read and edit notes with any text editor. Notes are not encrypted; on a laptop, use
full-disk encryption (see [ADR-0005](docs/adr/0005-encryption-at-rest.md)).

Run the tests with `python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
