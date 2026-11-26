"""Command-line entry point. Parses arguments and delegates; no business logic here."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .ebird import write_ebird_csv
from .store import Sighting, Store


def default_db_path() -> Path:
    """Per-OS data directory. ``BIRDLOG_DB`` overrides it."""
    override = os.environ.get("BIRDLOG_DB")
    if override:
        return Path(override)
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    return base / "birdlog" / "birdlog.sqlite3"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="birdlog", description="Log bird sightings.")
    parser.add_argument("--db", type=Path, default=None,
                        help="database file (default: per-OS data dir, or $BIRDLOG_DB)")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="log a sighting")
    add.add_argument("species")
    add.add_argument("location")
    add.add_argument("count", type=_positive_int)
    add.add_argument("--at", type=_parse_time, default=None, metavar="ISO8601",
                     help="when it was observed (default: now)")
    add.add_argument("--lat", type=float)
    add.add_argument("--lon", type=float)

    lst = sub.add_parser("list", help="show sightings, latest first")
    lst.add_argument("-n", "--limit", type=int, default=20, help="0 means all")

    exp = sub.add_parser("export", help="write sightings as eBird CSV")
    exp.add_argument("-o", "--output", type=Path, default=None,
                     help="output file (default: stdout)")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    db_path = args.db or default_db_path()

    with Store(db_path) as store:
        if args.command == "add":
            sighting = Sighting(
                species=args.species,
                location=args.location,
                count=args.count,
                observed_at=args.at or datetime.now().astimezone(),
                latitude=args.lat,
                longitude=args.lon,
            )
            print(f"logged #{store.add(sighting)}")
        elif args.command == "list":
            for s in store.latest(limit=args.limit or None):
                print(f"{s.id:>6}  {s.observed_at:%Y-%m-%d %H:%M}  "
                      f"{s.count:>5}  {s.species}  @ {s.location}")
        elif args.command == "export":
            if args.output is None:
                write_ebird_csv(store.chronological(), sys.stdout)
            else:
                with open(args.output, "w", newline="", encoding="utf-8") as fh:
                    write_ebird_csv(store.chronological(), fh)
    return 0


def _positive_int(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("count must be at least 1")
    return value


def _parse_time(text: str) -> datetime:
    try:
        dt = datetime.fromisoformat(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not an ISO 8601 time: {text!r}") from exc
    # Naive input is taken as local wall-clock time.
    return dt if dt.tzinfo is not None else dt.astimezone()
