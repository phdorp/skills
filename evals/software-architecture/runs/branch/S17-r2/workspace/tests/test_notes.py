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


class LegacyStoreTest(unittest.TestCase):
    def test_store_created_before_tags_still_opens(self):
        db = Path(tempfile.mkdtemp()) / "n.db"
        legacy = sqlite3.connect(db)
        legacy.execute("CREATE TABLE notes "
                       "(id INTEGER PRIMARY KEY, text TEXT NOT NULL, created TEXT NOT NULL)")
        legacy.execute("INSERT INTO notes (text, created) "
                       "VALUES ('Buy milk', '2026-11-01T09:00:00+00:00')")
        legacy.commit()
        legacy.close()

        store = Store(db)
        try:
            self.assertEqual([(n.text, n.tags) for n in store.all()], [("Buy milk", ())])
            store.add("Call Ann", ["work"])
            self.assertEqual([n.tags for n in store.all(tag="work")], [("work",)])
        finally:
            store.close()


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

    def test_add_with_tag_stores_tag(self):
        db = Path(tempfile.mkdtemp()) / "n.db"
        with mock.patch.dict(os.environ, {"NOTES_DB": str(db)}):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["add", "--tag", "work", "Call Ann"]), 0)
        store = Store(db)
        try:
            self.assertEqual([n.tags for n in store.all()], [("work",)])
        finally:
            store.close()

    def test_list_with_tag_prints_only_tagged_notes(self):
        db = Path(tempfile.mkdtemp()) / "n.db"
        with mock.patch.dict(os.environ, {"NOTES_DB": str(db)}):
            with redirect_stdout(io.StringIO()):
                main(["add", "--tag", "work", "Call Ann"])
                main(["add", "Buy milk"])
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(main(["list", "--tag", "work"]), 0)
        self.assertIn("Call Ann", out.getvalue())
        self.assertNotIn("Buy milk", out.getvalue())


if __name__ == "__main__":
    unittest.main()
