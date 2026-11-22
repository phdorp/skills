"""Hidden check for S15/S16 Task 1: search lists the newest notes first."""
import tempfile
import unittest
from pathlib import Path

from notes.store import Store


class HiddenSearch(unittest.TestCase):
    def test_search_lists_newest_first(self):
        store = Store(Path(tempfile.mkdtemp()) / "n.db")
        try:
            store.add("Buy milk")
            store.add("Call Ann")
            store.add("Milk the budget")
            self.assertEqual([n.text for n in store.search("milk")], ["Milk the budget", "Buy milk"])
        finally:
            store.close()


if __name__ == "__main__":
    unittest.main()
