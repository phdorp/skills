"""Read the Markdown tables of an arc42 document: the R-list, quality goals, quality scenarios.

A table is found by its first header cell (case-insensitive), and by a header it must have
when several tables share the first one, and returned as row dicts keyed by
the lower-cased header. Extra columns are kept. Standard library only.
"""
import re

ROW = re.compile(r"^\s*\|(.*)\|\s*$")
RULE = re.compile(r"^[\s|:-]+$")


def _cells(line):
    return [c.strip() for c in ROW.match(line).group(1).split("|")]


def table(text, first_header, column=None):
    """First table whose first header is `first_header` and, if given, that has header `column`."""
    lines = text.splitlines()
    for i, line in enumerate(lines[:-1]):
        if not (ROW.match(line) and RULE.match(lines[i + 1]) and "-" in lines[i + 1]):
            continue
        head = [h.lower() for h in _cells(line)]
        if head[0] != first_header.lower() or (column and column.lower() not in head):
            continue
        rows = []
        for row in lines[i + 2:]:
            if not ROW.match(row):
                break
            cells = _cells(row)
            rows.append(dict(zip(head, cells + [""] * (len(head) - len(cells)))))
        return rows
    return []
