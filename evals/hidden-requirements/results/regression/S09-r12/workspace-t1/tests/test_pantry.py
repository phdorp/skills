import io
import os
import tempfile
import unittest
import unittest.mock
from contextlib import redirect_stdout
from datetime import date, timedelta
from pathlib import Path

from pantry import cli, dates, store
from pantry.model import Item


class Pantry(unittest.TestCase):
    def setUp(self):
        self.file = Path(tempfile.mkdtemp()) / "pantry.jsonl"
        os.environ["PANTRY_FILE"] = str(self.file)

    def run_cli(self, *argv):
        out = io.StringIO()
        with redirect_stdout(out):
            code = cli.main(list(argv))
        return code, out.getvalue()

    def test_relative_dates(self):
        today = date(2026, 11, 21)
        self.assertEqual(dates.parse("+3d", today), date(2026, 11, 24))
        self.assertEqual(dates.parse("+2w", today), date(2026, 12, 5))
        self.assertEqual(dates.parse("tomorrow", today), date(2026, 11, 22))
        self.assertEqual(dates.parse("2026-12-01", today), date(2026, 12, 1))

    def test_add_remove_replays_from_the_file(self):
        store.add(Item("Milk", date(2026, 11, 25)))
        store.add(Item("Rice", date(2027, 6, 1)))
        store.remove("Milk")
        self.assertEqual([i.name for i in store.items()], ["Rice"])
        self.assertEqual(len(self.file.read_text().splitlines()), 3)

    def test_a_torn_last_line_is_skipped(self):
        store.add(Item("Rice", date(2027, 6, 1)))
        with open(self.file, "a") as f:
            f.write('{"op": "add", "na')
        self.assertEqual([i.name for i in store.items()], ["Rice"])

    def test_list_soon_sorted_by_expiry(self):
        soon = (date.today() + timedelta(days=2)).isoformat()
        sooner = (date.today() + timedelta(days=1)).isoformat()
        self.run_cli("add", "Yoghurt", soon)
        self.run_cli("add", "Milk", sooner)
        self.run_cli("add", "Rice", "2099-01-01")
        code, out = self.run_cli("list", "--soon", "7")
        self.assertEqual(code, 0)
        self.assertEqual([line.split()[-1] for line in out.splitlines()], ["Milk", "Yoghurt"])

    def test_exit_codes(self):
        self.assertEqual(self.run_cli("add", "Milk", "soonish")[0], 1)
        self.assertEqual(self.run_cli("remove", "Bread")[0], 1)
        with redirect_stdout(io.StringIO()), unittest.mock.patch("sys.stderr", io.StringIO()):
            self.assertEqual(cli.main(["frobnicate"]), 2)


if __name__ == "__main__":
    unittest.main()
