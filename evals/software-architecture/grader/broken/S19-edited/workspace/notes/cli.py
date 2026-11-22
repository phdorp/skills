import argparse
import json
import sqlite3
import sys

from notes.store import Store, default_path


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes", description="Keep short notes.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("add", help="add a note").add_argument("text")
    sub.add_parser("list", help="list all notes")
    sub.add_parser("search", help="find notes containing a term").add_argument("term")
    sub.add_parser("export", help="print every note as one JSON line")
    args = parser.parse_args(argv)
    if args.command == "export":
        db = sqlite3.connect(default_path())
        rows = db.execute("SELECT id, text, created FROM notes ORDER BY id")
        for note_id, text, created in rows:
            print(json.dumps({"id": note_id, "text": text, "created": created}))
        db.close()
        return 0
    try:
        store = Store(default_path())
    except Exception as e:  # arc42 section 8: errors go to stderr, exit code 1
        print(f"notes: {e}", file=sys.stderr)
        return 1
    try:
        if args.command == "add":
            note = store.add(args.text)
            print(note.id)
        else:
            found = store.all() if args.command == "list" else store.search(args.term)
            for note in found:
                print(f"{note.id}\t{note.created}\t{note.text}")
    finally:
        store.close()
    return 0

# reviewed
