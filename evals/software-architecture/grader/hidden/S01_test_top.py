"""Hidden check for S01: `python3 -m tally --top N FILE` prints the N most frequent words."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def tally(*args):
    path = Path(tempfile.mkdtemp()) / "in.txt"
    path.write_text("b a b c a b d\n")
    return subprocess.run([sys.executable, "-m", "tally", *args, str(path)],
                          capture_output=True, text=True, timeout=30)


class Top(unittest.TestCase):
    def test_top_two(self):
        self.assertEqual(tally("--top", "2").stdout, "b 3\na 2\n")

    def test_without_top_prints_all(self):
        self.assertEqual(tally().stdout, "b 3\na 2\nc 1\nd 1\n")


if __name__ == "__main__":
    unittest.main()
