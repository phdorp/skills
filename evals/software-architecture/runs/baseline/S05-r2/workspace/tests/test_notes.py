import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from notes.cli import main
from notes.store import Store


def new_dir():
    return Path(tempfile.mkdtemp()) / "notes"


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.dir = new_dir()
        self.store = Store(self.dir)

    def test_add_then_list(self):
        self.store.add("Buy milk")
        self.assertEqual([n.text for n in self.store.all()], ["Buy milk"])

    def test_search_matches_substring(self):
        self.store.add("Buy milk")
        self.store.add("Call Ann")
        self.assertEqual([n.text for n in self.store.search("mil")], ["Buy milk"])

    def test_search_ignores_case(self):
        self.store.add("Buy Milk")
        self.assertEqual([n.text for n in self.store.search("milk")], ["Buy Milk"])

    def test_all_lists_newest_first(self):
        self.store.add("first")
        self.store.add("second")
        self.store.add("third")
        self.assertEqual([n.text for n in self.store.all()], ["third", "second", "first"])

    def test_search_lists_newest_first(self):
        self.store.add("milk one")
        self.store.add("bread")
        self.store.add("milk two")
        self.assertEqual([n.text for n in self.store.search("milk")], ["milk two", "milk one"])

    def test_each_note_is_a_plain_text_file_with_its_text(self):
        note = self.store.add("Buy milk\nand eggs")
        path = self.dir / f"{note.id}.txt"
        self.assertEqual(path.read_text(encoding="utf-8"), "Buy milk\nand eggs\n")

    def test_edit_in_text_editor_is_seen_by_list(self):
        note = self.store.add("Buy milk")
        (self.dir / f"{note.id}.txt").write_text("Buy oat milk\n", encoding="utf-8")
        self.assertEqual([n.text for n in self.store.all()], ["Buy oat milk"])

    def test_edit_keeps_position(self):
        first = self.store.add("first")
        self.store.add("second")
        (self.dir / f"{first.id}.txt").write_text("first, edited\n", encoding="utf-8")
        self.assertEqual([n.text for n in self.store.all()], ["second", "first, edited"])

    def test_ignores_files_that_are_not_notes(self):
        self.store.add("real note")
        (self.dir / "shopping.txt").write_text("not a note id\n", encoding="utf-8")
        (self.dir / ".tmp-leftover").write_text("half written\n", encoding="utf-8")
        self.assertEqual([n.text for n in self.store.all()], ["real note"])

    def test_creates_directory_when_missing(self):
        missing = new_dir()
        self.assertFalse(missing.exists())
        Store(missing)
        self.assertTrue(missing.is_dir())

    def test_no_temporary_files_remain_after_add(self):
        self.store.add("Buy milk")
        self.assertEqual([p.suffix for p in self.dir.iterdir()], [".txt"])

    def test_notes_added_at_the_same_instant_are_both_kept(self):
        instant = datetime(2026, 11, 21, 10, 0, 0, tzinfo=timezone.utc)
        with mock.patch("notes.store.utc_now", return_value=instant):
            a = self.store.add("a")
            b = self.store.add("b")
        self.assertNotEqual(a.id, b.id)
        self.assertEqual([n.text for n in self.store.all()], ["b", "a"])


class CliTest(unittest.TestCase):
    def run_cli(self, env_dir, *argv):
        out = io.StringIO()
        with mock.patch.dict(os.environ, {"NOTES_DIR": str(env_dir)}):
            with redirect_stdout(out):
                code = main(list(argv))
        return code, out.getvalue()

    def test_add_and_search(self):
        d = new_dir()
        code, _ = self.run_cli(d, "add", "Buy milk")
        self.assertEqual(code, 0)
        code, out = self.run_cli(d, "search", "milk")
        self.assertEqual(code, 0)
        self.assertIn("Buy milk", out)

    def test_list_shows_newest_first(self):
        d = new_dir()
        self.run_cli(d, "add", "older note")
        self.run_cli(d, "add", "newer note")
        _, out = self.run_cli(d, "list")
        lines = out.strip().splitlines()
        self.assertTrue(lines[0].endswith("newer note"))
        self.assertTrue(lines[1].endswith("older note"))


if __name__ == "__main__":
    unittest.main()
