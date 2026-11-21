import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from birdlog.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.db = Path(self._tmp.name) / "birdlog.sqlite3"

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(["--db", str(self.db), *argv])
        return code, out.getvalue()

    def test_add_then_list_shows_latest_first(self):
        self.assertEqual(self.run_cli("add", "Robin", "Park", "2", "--at", "2026-11-01T08:00:00+00:00")[0], 0)
        self.run_cli("add", "Wren", "Garden", "1", "--at", "2026-11-03T09:30:00+00:00")
        _, out = self.run_cli("list")
        lines = out.strip().splitlines()
        self.assertIn("Wren", lines[0])
        self.assertIn("Robin", lines[1])

    def test_export_writes_ebird_file(self):
        self.run_cli("add", "Robin", "Park", "2", "--at", "2026-11-01T08:00:00+00:00")
        target = Path(self._tmp.name) / "out.csv"
        self.run_cli("export", "-o", str(target))
        text = target.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("Common Name,Genus,Species,"))
        self.assertIn("Robin,,,2,,Park,", text)

    def test_count_must_be_positive(self):
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                self.run_cli("add", "Robin", "Park", "0")


if __name__ == "__main__":
    unittest.main()
