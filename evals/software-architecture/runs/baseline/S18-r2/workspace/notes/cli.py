import argparse
import sys

from notes.store import Store, default_path


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes", description="Keep short notes.")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="add a note")
    add.add_argument("text")
    add.add_argument("--tag", action="append", default=[], help="tag the note (repeatable)")
    sub.add_parser("list", help="list all notes").add_argument("--tag", help="only notes with this tag")
    sub.add_parser("search", help="find notes containing a term").add_argument("term")
    args = parser.parse_args(argv)
    try:
        store = Store(default_path())
    except Exception as e:  # arc42 section 8: errors go to stderr, exit code 1
        print(f"notes: {e}", file=sys.stderr)
        return 1
    try:
        if args.command == "add":
            try:
                note = store.add(args.text, tags=args.tag)
            except ValueError as e:
                print(f"notes: {e}", file=sys.stderr)
                return 1
            print(note.id)
        else:
            found = store.all(tag=args.tag) if args.command == "list" else store.search(args.term)
            for note in found:
                print(f"{note.id}\t{note.created}\t{note.text}")
    finally:
        store.close()
    return 0
