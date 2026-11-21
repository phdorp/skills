# notes

Keep short notes from the command line.

```sh
python3 -m notes add "Buy milk"
python3 -m notes list
python3 -m notes search milk
```

`notes list` shows the newest notes first. Each note is a plain UTF-8 text file in `~/.notes/`,
so you can read and edit notes with any text editor (set `NOTES_DIR` to use another directory).
Run the tests with `python3 -m unittest`. Architecture: [docs/architecture/arc42.md](docs/architecture/arc42.md).
Storage: [ADR-0004](docs/adr/0004-store-notes-as-plain-text-files.md).
Notes are not encrypted yet; see [ADR-0005](docs/adr/0005-encrypt-notes-at-rest.md).
