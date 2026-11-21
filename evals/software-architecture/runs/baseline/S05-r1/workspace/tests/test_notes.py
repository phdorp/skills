import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from notes.cli import main
from notes.store import Store


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.store = Store(self.dir / "notes")

    def test_add_writes_a_plain_text_file(self):
        note = self.store.add("Buy milk")
        self.assertEqual((self.dir / "notes" / f"{note.id}.txt").read_text(encoding="utf-8"),
                         "Buy milk\n")

    def test_add_then_list(self):
        self.store.add("Buy milk")
        self.assertEqual([n.text for n in self.store.all()], ["Buy milk"])

    def test_list_is_newest_first(self):
        self.store.add("first")
        self.store.add("second")
        self.store.add("third")
        self.assertEqual([n.text for n in self.store.all()], ["third", "second", "first"])

    def test_search_matches_substring_oldest_first(self):
        self.store.add("Buy milk")
        self.store.add("Call Ann")
        self.store.add("Oat MILK")
        self.assertEqual([n.text for n in self.store.search("milk")], ["Buy milk", "Oat MILK"])

    def test_edits_made_in_a_text_editor_are_seen(self):
        note = self.store.add("Buy milk")
        (self.dir / "notes" / f"{note.id}.txt").write_text("Buy oat milk\n", encoding="utf-8")
        self.assertEqual([n.text for n in self.store.all()], ["Buy oat milk"])

    def test_hand_made_file_is_listed(self):
        (self.dir / "notes" / "ideas.txt").write_text("Try a new idea", encoding="utf-8")
        notes = self.store.all()
        self.assertEqual([(n.id, n.text) for n in notes], [("ideas", "Try a new idea")])

    def test_no_temporary_file_is_left_behind(self):
        self.store.add("Buy milk")
        self.assertEqual(sorted(p.suffix for p in (self.dir / "notes").iterdir()), [".txt"])


class CliTest(unittest.TestCase):
    def test_add_and_search(self):
        notes_dir = Path(tempfile.mkdtemp()) / "notes"
        with mock.patch.dict(os.environ, {"NOTES_DIR": str(notes_dir)}):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["add", "Buy milk"]), 0)
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(main(["search", "milk"]), 0)
        self.assertIn("Buy milk", out.getvalue())


if __name__ == "__main__":
    unittest.main()
