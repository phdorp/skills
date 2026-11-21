# birdlog architecture

## Requirements → decisions

| # | Requirement | Decision |
|---|---|---|
| 1 | Log species, place, time, count from the CLI | `birdlog add SPECIES --place P [--count N] [--at WHEN]`. Time defaults to now. |
| 2 | No sighting lost, even on a crash mid-write | SQLite, one explicit transaction per write, `synchronous=FULL`. A write is either fully committed or absent. No in-place rewrites of data files. |
| 3 | Offline on Linux, macOS, Windows; only Python needed | Standard library only (`sqlite3`, `argparse`, `csv`). `dependencies = []`. Data dir resolved by hand per OS. |
| 4 | Export to eBird CSV | `birdlog export PATH`. Pure mapping in `ebird.py`; file written via temp file + fsync + `os.replace`. |
| 5 | Fast | One SQLite file, indexed on `(observed_at DESC, id DESC)`. Lazy-free imports kept to stdlib basics. One fsync per `add`. |
| 6 | `list` shows latest first | `ORDER BY observed_at DESC, id DESC`. "Latest" means the time the bird was seen, not when it was typed in. |

Minimum Python is 3.11 (for `datetime.fromisoformat` with flexible input and `X | Y` type hints).

## Module layout

```
birdlog/
  __main__.py   python -m birdlog
  cli.py        argparse wiring only; no SQL, no formatting rules
  model.py      Sighting dataclass + validation (pure)
  store.py      SQLite persistence, migrations, transactions (only SQL lives here)
  ebird.py      Sighting -> eBird CSV rows; atomic file write
  paths.py      per-OS data directory (BIRDLOG_HOME overrides)
tests/          unittest (stdlib); no pytest needed to run
```

Dependency direction: `cli → {store, ebird, model, paths}`, `store → model`, `ebird → model`. `model` depends on nothing.

## Data

Table `sightings`: `id`, `species`, `place`, `observed_at` (UTC epoch s), `utc_offset_min` (observer's local offset at the time), `count` (> 0), `created_at`.

Storing the offset lets us reproduce the local date and start time exactly, which eBird needs, without storing a timezone name.

Schema version lives in `PRAGMA user_version`. Migrations are an ordered list in `store.py`, run inside a single `BEGIN IMMEDIATE` transaction. A database from a newer version is refused rather than misread.

Database location: `%LOCALAPPDATA%\birdlog` (Windows), `~/Library/Application Support/birdlog` (macOS), `$XDG_DATA_HOME/birdlog` or `~/.local/share/birdlog` (Linux). Override with `BIRDLOG_HOME`.

## Trade-offs

- **SQLite over an append-only text log.** A JSONL file needs hand-written torn-line recovery. SQLite gives atomic commits and crash recovery for free, and it is in the stdlib on all three platforms.
- **One fsync per `add`.** Costs a few ms (more on macOS, where SQLite uses full fsync). Accepted: a birder logs a few sightings at a time, and durability is requirement 2.
- **No WAL.** The default rollback journal is simpler and keeps the database a single file that is safe to copy when no command is running. WAL would be faster for bulk writes, which birdlog does not need.

## Open questions (need a decision before the eBird export is usable)

1. **Taxonomy.** eBird matches species by common name, but its record format also has Genus/Species columns. Do we store a scientific name, or rely on common-name matching?
2. **Location.** eBird needs a location name that matches a hotspot or coordinates, plus state and country codes. `--place` is free text. Options: add optional `--lat/--lon` and `--country/--state`, or keep free text and fill those columns at export time.
3. **Protocol.** Export currently writes `Incidental` for every row. Checklist protocols (Stationary, Traveling) would need duration and distance per checklist, which means a new "checklist" concept.
4. **Column list.** `ebird.COLUMNS` is written from memory of eBird's record format. Check it against eBird's current import spec before release.
5. **Editing and deleting.** Not in scope yet. Mistakes are fixed by editing the database. A `delete` command would need a confirmation step.

## Testing

`python -m unittest` from the repo root. Tests use a temporary database (`Store(path)`), so they never touch the real data directory.
