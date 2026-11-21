# shelf

A command-line tool for keeping a list of the books you own.

```sh
python3 -m shelf add "Dune" --isbn 9780441172719
python3 -m shelf list
python3 -m shelf find dune
```

Requires Python 3 and nothing else. Books are stored in `~/.shelf.json`, or in the file named by
`SHELF_FILE`.

## How it works

shelf has three modules. `cli.py` parses commands and prints results. `catalog.py` is the only
code that reads or writes the JSON file. `isbn.py` checks ISBN-10 and ISBN-13 check digits. `cli`
calls `catalog`, never the file directly.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the components, data format, requirements
status and known gaps. Design decisions are in [docs/decisions/](docs/decisions/).

## Tests

```sh
python3 -m unittest discover -s tests -t .
```
