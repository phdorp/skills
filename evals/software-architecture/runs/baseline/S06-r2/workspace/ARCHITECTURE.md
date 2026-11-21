# birdlog architecture

birdlog is a command-line tool for logging bird sightings. It is a single
Python package that uses only the standard library.

## Layout

```
src/birdlog/
  store.py   Sighting model + SQLite persistence (the durability boundary)
  ebird.py   Pure exporter: Sightings -> eBird CSV text
  cli.py     argparse front end; parses, calls store/ebird, prints. No logic.
  __main__.py  `python -m birdlog`
tests/       unittest only (no pytest, so dev setup is also just Python)
```

Dependencies flow one way: `cli -> store, ebird`, and `ebird -> store`
(for the `Sighting` type). `store` imports nothing from the package.

## Decisions

| Requirement | Decision |
|---|---|
| Stdlib only, Linux/macOS/Windows | `sqlite3` ships with CPython on all three. No third-party packages. `pyproject.toml` declares `dependencies = []`. |
| No sighting lost on crash | SQLite in WAL mode with `synchronous=FULL`. Each `add` is one autocommitted INSERT and returns only after commit. A kill or power cut leaves the last committed state, never a torn row. Covered by a SIGKILL test that checks every acknowledged id survives. |
| Export to eBird CSV | `ebird.py` writes the 21-column eBird Record Format. Each sighting is an Incidental, single-observer row. Date and time are formatted by hand, because `%-I` does not exist on Windows. |
| Fast | Startup is about 50–80 ms because the CLI imports only `argparse`, `sqlite3` and the package. `add` costs about 3 ms, dominated by fsync. `latest(20)` on 20k rows takes about 0.3 ms via the `(observed_at DESC, id DESC)` index. |
| `list` shows latest first | `ORDER BY observed_at DESC, id DESC`. "Latest" means observation time; ties go to the most recently inserted row. |

## Data model

Table `sightings`: `id`, `species`, `location`, `count` (CHECK > 0),
`observed_at` (UTC epoch seconds), `utc_offset_min` (the local offset at
the time of observation, which is what eBird needs for local date and time),
`latitude`, `longitude` (optional), `created_at` (when it was logged).

The schema version is stored in `PRAGMA user_version`. A database with a
newer version than the code is refused rather than misread.

Database location: `$BIRDLOG_DB` if set, otherwise `%APPDATA%\birdlog`
on Windows, `~/Library/Application Support/birdlog` on macOS, and
`$XDG_DATA_HOME/birdlog` (default `~/.local/share/birdlog`) on Linux.

## Quality goals

Listed in the order of the original requirements. "Measure" is what is
verified today. Where no target was set, the goal stays open.

1. **Durability.** A sighting that `add` reported as logged is never lost.
   Measure: `test_acknowledged_sightings_survive_sigkill_mid_write` passes
   (0 acknowledged sightings missing, `integrity_check` = ok). Verified on
   Linux only, with one kill-timing pattern.
2. **Offline and portable.** Runs on Linux, macOS and Windows with only
   Python installed. Measure: no third-party dependencies. Tested only on
   Linux with Python 3.13. macOS, Windows and Python 3.9 are **not yet tested**.
3. **eBird export.** Output matches the eBird CSV import format. Measure: the
   header and row format are covered by tests against our own expected
   output. Matching eBird's spec is **open** (see question 3 below).
4. **Speed.** Measured: `add` about 2.8 ms average over 20k rows; `latest(20)`
   about 0.3 ms over 20k rows; CLI startup about 50–80 ms. No numeric target
   has been set, so **the target is open**.
5. **Ordering.** `list` shows the latest observation first. Measure:
   ordering and tie-break tests pass.

## Open questions (need a decision before v1)

1. **eBird taxonomy.** The export writes the common name as given. eBird
   rejects unknown names on import, so v1 needs either a bundled eBird
   taxonomy file for validation (offline, so it must ship with the package)
   or a documented requirement that users type exact eBird names.
   Genus and Species are left blank. Confirm against eBird's current import
   spec whether they are required.
2. **Checklists.** Every sighting is currently its own Incidental checklist.
   Real birding is usually a checklist with several species, a duration, and
   a Stationary or Traveling protocol. Adding a `checklists` table is a
   schema v2 migration; `Store._migrate` in `store.py` is the hook for it.
3. **Country and state.** eBird accepts location by name plus coordinates.
   Country and State/Province are blank in the export. Confirm whether
   coordinates alone are enough for import.
4. **Column list.** The 21-column header was written from memory of the
   eBird Record Format. Verify it against eBird's import documentation before
   relying on it.

## Testing

```
PYTHONPATH=src python -m unittest discover -s tests -v
```

`test_acknowledged_sightings_survive_sigkill_mid_write` is the durability
test. It is the one to keep green. It starts a writer subprocess, kills it
mid-loop, and asserts that every acknowledged id is present and that
`PRAGMA integrity_check` returns `ok`.
