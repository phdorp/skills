import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from birdlog.store import Sighting, Store

UTC = timezone.utc
T0 = datetime(2026, 11, 1, 8, 0, tzinfo=UTC)

# Child process: logs sightings forever, printing each id only after add() returned.
_WRITER = """
import sys
from datetime import datetime, timedelta, timezone
from birdlog.store import Sighting, Store
store = Store(sys.argv[1])
t0 = datetime(2026, 11, 1, tzinfo=timezone.utc)
i = 0
while True:
    i += 1
    sid = store.add(Sighting("Robin", "Park", 1, t0 + timedelta(seconds=i)))
    print(sid, flush=True)
"""


class StoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "nested" / "birdlog.sqlite3"

    def tearDown(self):
        self._tmp.cleanup()

    def test_latest_orders_by_observation_time_newest_first(self):
        with Store(self.path) as store:
            for minutes in (5, 1, 9):
                store.add(Sighting("Robin", "Park", 1, T0 + timedelta(minutes=minutes)))
            times = [s.observed_at for s in store.latest()]
        self.assertEqual(times, [T0 + timedelta(minutes=m) for m in (9, 5, 1)])

    def test_latest_breaks_ties_by_newest_insert(self):
        with Store(self.path) as store:
            first = store.add(Sighting("Robin", "Park", 1, T0))
            second = store.add(Sighting("Wren", "Park", 1, T0))
            ids = [s.id for s in store.latest()]
        self.assertEqual(ids, [second, first])

    def test_limit_applies_after_ordering(self):
        with Store(self.path) as store:
            for minutes in range(10):
                store.add(Sighting("Robin", "Park", 1, T0 + timedelta(minutes=minutes)))
            self.assertEqual(len(store.latest(limit=3)), 3)
            self.assertEqual(store.latest(limit=1)[0].observed_at, T0 + timedelta(minutes=9))

    def test_sighting_round_trips_across_reopen(self):
        plus_one = timezone(timedelta(hours=1))
        original = Sighting("Blue Jay", "Lake", 4, datetime(2026, 11, 1, 15, 5, tzinfo=plus_one),
                            latitude=51.5, longitude=-0.12)
        with Store(self.path) as store:
            sid = store.add(original)
        with Store(self.path) as store:
            (got,) = store.latest()
        self.assertEqual(got.id, sid)
        self.assertEqual((got.species, got.location, got.count), ("Blue Jay", "Lake", 4))
        self.assertEqual((got.latitude, got.longitude), (51.5, -0.12))
        self.assertEqual(got.observed_at, original.observed_at)
        self.assertEqual(got.observed_at.utcoffset(), timedelta(hours=1))

    def test_rejects_naive_datetime(self):
        with Store(self.path) as store, self.assertRaises(ValueError):
            store.add(Sighting("Robin", "Park", 1, datetime(2026, 11, 1, 8, 0)))

    def test_rejects_non_positive_count(self):
        with Store(self.path) as store, self.assertRaises(sqlite3.IntegrityError):
            store.add(Sighting("Robin", "Park", 0, T0))

    def test_acknowledged_sightings_survive_sigkill_mid_write(self):
        src_dir = str(Path(__file__).resolve().parents[1] / "src")
        env = dict(os.environ, PYTHONPATH=src_dir)
        proc = subprocess.Popen(
            [sys.executable, "-c", _WRITER, str(self.path)],
            stdout=subprocess.PIPE, cwd=self._tmp.name, env=env,
        )
        try:
            head = [proc.stdout.readline() for _ in range(200)]
        finally:
            proc.kill()
            proc.wait()
            tail = proc.stdout.read()
            proc.stdout.close()
        text = (b"".join(head) + tail).decode()
        # Only newline-terminated lines count as acknowledged; a line cut off by the kill does not.
        acked = {int(line) for line in text.split("\n")[:-1] if line.strip()}
        self.assertGreaterEqual(len(acked), 200)

        conn = sqlite3.connect(self.path)
        try:
            self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        finally:
            conn.close()
        with Store(self.path) as store:
            present = {s.id for s in store.chronological()}
        missing = acked - present
        self.assertFalse(missing, f"acknowledged sightings lost: {sorted(missing)[:10]}")


if __name__ == "__main__":
    unittest.main()
