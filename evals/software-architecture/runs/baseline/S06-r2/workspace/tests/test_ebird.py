import io
import unittest
from datetime import datetime, timedelta, timezone

from birdlog.ebird import HEADER, write_ebird_csv
from birdlog.store import Sighting


class EBirdExportTests(unittest.TestCase):
    def test_header_and_single_row(self):
        plus_one = timezone(timedelta(hours=1))
        s = Sighting("Blue Jay", "Lake", 4, datetime(2026, 11, 1, 15, 5, tzinfo=plus_one),
                     latitude=51.5, longitude=-0.12)
        out = io.StringIO()
        write_ebird_csv([s], out)
        lines = out.getvalue().split("\n")
        self.assertEqual(lines[0], ",".join(HEADER))
        self.assertEqual(len(HEADER), 21)
        self.assertEqual(
            lines[1],
            "Blue Jay,,,4,,Lake,51.500000,-0.120000,11/01/2026,3:05 PM,,,Incidental,1,,N,,,,,",
        )

    def test_midnight_and_noon_are_twelve_hour_clock(self):
        utc = timezone.utc
        rows = []
        for hour in (0, 12):
            out = io.StringIO()
            write_ebird_csv([Sighting("Wren", "Park", 1, datetime(2026, 1, 2, hour, 0, tzinfo=utc))], out)
            rows.append(out.getvalue().split("\n")[1].split(",")[9])
        self.assertEqual(rows, ["12:00 AM", "12:00 PM"])


if __name__ == "__main__":
    unittest.main()
