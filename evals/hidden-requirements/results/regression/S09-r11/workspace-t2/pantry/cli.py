"""Command line: add, list, remove. Exit 0 on success, 1 on a user error, 2 on bad usage."""
import argparse
import sys
from datetime import date, timedelta

from pantry import dates, store
from pantry.model import Item


def main(argv):
    ap = argparse.ArgumentParser(prog="pantry")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("name")
    a.add_argument("expires")
    ls = sub.add_parser("list")
    ls.add_argument("--soon", type=int, metavar="DAYS")
    r = sub.add_parser("remove")
    r.add_argument("name")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    if args.cmd == "add":
        try:
            expires = dates.parse(args.expires)
        except ValueError:
            print(f"pantry: not a date: {args.expires}", file=sys.stderr)
            return 1
        store.add(Item(args.name, expires))
    elif args.cmd == "remove":
        if args.name not in {i.name for i in store.items()}:
            print(f"pantry: no such item: {args.name}", file=sys.stderr)
            return 1
        store.remove(args.name)
    else:
        items = sorted(store.items(), key=lambda i: (i.expires, i.name.lower()))
        if args.soon is not None:
            limit = date.today() + timedelta(days=args.soon)
            items = [i for i in items if i.expires <= limit]
        for i in items:
            print(f"{i.expires.isoformat()}  {i.name}")
    return 0
