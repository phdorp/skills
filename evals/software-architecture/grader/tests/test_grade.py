import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import grade  # noqa: E402


class Measure(unittest.TestCase):
    def test_has_measure_accepts_numbers(self):
        for text in ("0 unreadable logs in 100 trials", "the suite passes on all three OSes",
                     "100% of 50 sightings accepted", "every one of the twelve tests passes"):
            self.assertTrue(grade.has_measure(text), text)

    def test_has_measure_rejects_vague_wording(self):
        for text in ("every command feels fast", "all requests are quick", "fast enough",
                     "none of the users complain", "responds instantly for one user", "no"):
            self.assertFalse(grade.has_measure(text), text)


if __name__ == "__main__":
    unittest.main()
