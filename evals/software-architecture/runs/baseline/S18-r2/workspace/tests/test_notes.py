import io
import os
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from notes.cli import main
from notes.store import Store


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.store = Store(Path(tempfile.mkdtemp()) / "n.db")

    def tearDown(self):
        self.store.close()

    def test_add_then_list(self):
        self.store.add("Buy milk")
        self.assertEqual([n.text for n in self.store.all()], ["Buy milk"])

    def test_search_matches_substring(self):
        self.store.add("Buy milk")
        self.store.add("Call Ann")
        self.assertEqual([n.text for n in self.store.search("mil")], ["Buy milk"])

    def test_search_lists_newest_first(self):
        self.store.add("Buy milk")
        self.store.add("Milk the budget")
        self.assertEqual([n.text for n in self.store.search("milk")],
                         ["Milk the budget", "Buy milk"])

    def test_add_stores_tags(self):
        self.store.add("Call Ann", tags=["work"])
        self.assertEqual(self.store.all()[0].tags, ("work",))

    def test_all_filters_by_tag(self):
        self.store.add("Call Ann", tags=["work"])
        self.store.add("Buy milk")
        self.store.add("Standup", tags=["work", "team"])
        self.assertEqual([n.text for n in self.store.all(tag="work")], ["Call Ann", "Standup"])

    def test_tag_cannot_contain_comma(self):
        with self.assertRaises(ValueError):
            self.store.add("Call Ann", tags=["a,b"])

    def test_store_created_before_tags_still_opens(self):
        path = Path(tempfile.mkdtemp()) / "old.db"
        old = sqlite3.connect(path)
        old.execute("CREATE TABLE notes "
                    "(id INTEGER PRIMARY KEY, text TEXT NOT NULL, created TEXT NOT NULL)")
        old.execute("INSERT INTO notes (text, created) VALUES ('Old note', '2026-01-01T00:00:00+00:00')")
        old.commit()
        old.close()
        store = Store(path)
        self.addCleanup(store.close)
        self.assertEqual([(n.text, n.tags) for n in store.all()], [("Old note", ())])


class CliTest(unittest.TestCase):
    def test_add_and_search(self):
        db = Path(tempfile.mkdtemp()) / "n.db"
        with mock.patch.dict(os.environ, {"NOTES_DB": str(db)}):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["add", "Buy milk"]), 0)
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(main(["search", "milk"]), 0)
        self.assertIn("Buy milk", out.getvalue())

    def test_add_with_tag_then_list_filters_by_tag(self):
        db = Path(tempfile.mkdtemp()) / "n.db"
        with mock.patch.dict(os.environ, {"NOTES_DB": str(db)}):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["add", "--tag", "work", "Call Ann"]), 0)
                self.assertEqual(main(["add", "Buy milk"]), 0)
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(main(["list", "--tag", "work"]), 0)
        self.assertIn("Call Ann", out.getvalue())
        self.assertNotIn("Buy milk", out.getvalue())


if __name__ == "__main__":
    unittest.main()
