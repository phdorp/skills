import argparse
import sys

from notes.store import Store, default_path


def _tag(value):
    # Tags are stored comma-separated, so a comma inside one would split it in two.
    tag = value.strip()
    if not tag or "," in tag:
        raise argparse.ArgumentTypeError(f"invalid tag {value!r}: must be non-empty and contain no comma")
    return tag


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes", description="Keep short notes.")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="add a note")
    add.add_argument("text")
    add.add_argument("--tag", action="append", type=_tag, help="tag the note (repeatable)")
    lst = sub.add_parser("list", help="list all notes")
    lst.add_argument("--tag", type=_tag, help="only notes with this tag")
    sub.add_parser("search", help="find notes containing a term").add_argument("term")
    args = parser.parse_args(argv)
    try:
        store = Store(default_path())
    except Exception as e:  # arc42 section 8: errors go to stderr, exit code 1
        print(f"notes: {e}", file=sys.stderr)
        return 1
    try:
        if args.command == "add":
            note = store.add(args.text, tags=args.tag or ())
            print(note.id)
        else:
            found = store.all(tag=args.tag) if args.command == "list" else store.search(args.term)
            for note in found:
                print(f"{note.id}\t{note.created}\t{note.text}")
    finally:
        store.close()
    return 0
