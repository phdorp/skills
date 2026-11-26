"""Command-line entry point. Thin: parses arguments and delegates.

Commands:
  birdlog add SPECIES --place PLACE [--count N] [--at WHEN]
  birdlog list [-n N]
  birdlog export PATH|-
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Sequence

from birdlog import ebird
from birdlog.model import new_sighting
from birdlog.paths import db_path
from birdlog.store import Store


def _parse_when(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"invalid time {value!r}; use ISO 8601, e.g. 2026-11-20T07:30 or '2026-11-20 07:30'"
        )


def _positive_int(value: str) -> int:
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be an integer")
    if n < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return n


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="birdlog", description="Log bird sightings.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="log a sighting")
    add.add_argument("species")
    add.add_argument("--place", required=True)
    add.add_argument("--count", type=_positive_int, default=1)
    add.add_argument("--at", type=_parse_when, default=None, metavar="WHEN",
                     help="ISO 8601 local time; default: now")

    lst = sub.add_parser("list", help="show sightings, latest first")
    lst.add_argument("-n", "--limit", type=_positive_int, default=20)

    exp = sub.add_parser("export", help="write sightings as eBird CSV")
    exp.add_argument("path", help="output file, or - for stdout")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        with Store(db_path()) as store:
            if args.command == "add":
                s = store.add(new_sighting(args.species, args.place, args.count, args.at))
                print(f"Logged #{s.id}: {s.count} x {s.species} at {s.place} "
                      f"({s.local_time():%Y-%m-%d %H:%M})")
            elif args.command == "list":
                for s in store.latest(args.limit):
                    print(f"#{s.id:<5} {s.local_time():%Y-%m-%d %H:%M}  "
                          f"{s.count:>4} x {s.species}  @ {s.place}")
            elif args.command == "export":
                ebird.write_atomic(Path(args.path), store.all_chronological())
                if args.path != "-":
                    print(f"Exported to {args.path}", file=sys.stderr)
    except ValueError as e:  # validation errors from model
        print(f"birdlog: error: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"birdlog: error: {e}", file=sys.stderr)
        return 1
    return 0
