import io
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from birdlog import ebird
from birdlog.model import new_sighting
from birdlog.store import Store

UTC_PLUS_2 = timezone(timedelta(hours=2))


class ModelTests(unittest.TestCase):
    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            new_sighting("  ", "Park")
        with self.assertRaises(ValueError):
            new_sighting("Robin", "")
        with self.assertRaises(ValueError):
            new_sighting("Robin", "Park", count=0)

    def test_keeps_local_offset_for_export(self):
        when = datetime(2026, 11, 20, 7, 30, tzinfo=UTC_PLUS_2)
        s = new_sighting("Robin", "Park", 3, when)
        self.assertEqual(s.utc_offset_min, 120)
        self.assertEqual(s.local_time().strftime("%H:%M"), "07:30")


class StoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "db" / "birdlog.sqlite3"

    def tearDown(self):
        self._tmp.cleanup()

    def test_sightings_survive_reopen(self):
        with Store(self.path) as store:
            store.add(new_sighting("Robin", "Park", 2))
        with Store(self.path) as store:
            rows = store.latest()
        self.assertEqual([(r.species, r.count) for r in rows], [("Robin", 2)])

    def test_latest_first_by_observed_time_not_insert_order(self):
        base = datetime(2026, 11, 20, 8, 0, tzinfo=UTC_PLUS_2)
        with Store(self.path) as store:
            store.add(new_sighting("Late", "A", when=base + timedelta(hours=3)))
            store.add(new_sighting("Early", "A", when=base))
            store.add(new_sighting("Middle", "A", when=base + timedelta(hours=1)))
            self.assertEqual(
                [s.species for s in store.latest()], ["Late", "Middle", "Early"]
            )
            self.assertEqual([s.species for s in store.latest(1)], ["Late"])

    def test_export_csv_header_and_row(self):
        when = datetime(2026, 11, 20, 7, 5, tzinfo=UTC_PLUS_2)
        with Store(self.path) as store:
            store.add(new_sighting("Blue Tit", "Hyde Park", 4, when))
            text = ebird.render(store.all_chronological())
        lines = text.splitlines()
        self.assertEqual(lines[0], ",".join(ebird.COLUMNS))
        self.assertIn("Blue Tit", lines[1])
        self.assertIn("11/20/2026", lines[1])
        self.assertIn("07:05 AM", lines[1])
        self.assertIn("Hyde Park", lines[1])

    def test_write_atomic_replaces_file(self):
        out = Path(self._tmp.name) / "export.csv"
        out.write_text("old")
        with Store(self.path) as store:
            store.add(new_sighting("Robin", "Park"))
            ebird.write_atomic(out, store.all_chronological())
        self.assertTrue(out.read_text().startswith(",".join(ebird.COLUMNS)))
        self.assertEqual(list(out.parent.glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
