import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import arc42  # noqa: E402

DOC = """# x

## 1. Introduction

| role | expectation |
|---|---|
| Users | keep notes |

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add notes. | 1 | active | core use |
| R-4 | Sync. | - | deferred | needs a server; revisit |

## 10. Quality requirements

| id | goal | measure |
|---|---|---|
| QS-1 | QG-1 | 0 in 100 |
"""


class Table(unittest.TestCase):
    def test_table_by_first_header(self):
        rows = arc42.table(DOC, "ID")
        self.assertEqual([r["id"] for r in rows], ["R-1", "R-4"])
        self.assertEqual(rows[1], {"id": "R-4", "requirement": "Sync.", "rank": "-",
                                   "status": "deferred", "reason": "needs a server; revisit"})
        self.assertEqual(arc42.table(DOC, "role"), [{"role": "Users", "expectation": "keep notes"}])

    def test_table_tolerates_extra_column(self):
        doc = ("| ID | requirement | rank | status | reason | source |\n"
               "|---|---|---|---|---|---|\n"
               "| R-6 | Encrypt notes. | 4 | active | stolen laptop | interviews |\n")
        rows = arc42.table(doc, "ID")
        self.assertEqual((rows[0]["id"], rows[0]["status"], rows[0]["source"]),
                         ("R-6", "active", "interviews"))

    def test_table_picks_by_column_when_first_headers_agree(self):
        doc = DOC.replace("| id | goal | measure |", "| ID | goal | measure |")
        self.assertEqual([r["id"] for r in arc42.table(doc, "ID", column="measure")], ["QS-1"])
        self.assertEqual([r["id"] for r in arc42.table(doc, "ID", column="requirement")],
                         ["R-1", "R-4"])

    def test_table_missing_returns_empty(self):
        self.assertEqual(arc42.table(DOC, "nothing"), [])


if __name__ == "__main__":
    unittest.main()
