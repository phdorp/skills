"""Read ADRs the way the grader needs them: number, title, Nygard fields, status.

A field is a `#`-heading (`## Status`) or a label line (`Status: x`, `**Status:** x`),
case-insensitive. Its text runs to the next field or heading. Standard library only.
"""
import re
from dataclasses import dataclass
from pathlib import Path

FIELDS = ("status", "context", "decision", "consequences")
NUMBER = re.compile(r"^(\d{4})-")
TITLE = re.compile(r"^#\s+(.+?)\s*$", re.M)
HEADING_FIELD = re.compile(r"^#{2,}\s*(status|context|decision|consequences)\s*:?\s*(.*)$", re.I)
LABEL_FIELD = re.compile(r"^\**(status|context|decision|consequences)\s*:\**\s*:?\**\s*(.*)$", re.I)
ANY_HEADING = re.compile(r"^#{1,6}\s")
ID = re.compile(r"\b(?:R|QG|QS)-\d+\b")


@dataclass
class Adr:
    number: int
    title: str
    fields: dict
    status: str


def parse(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    m = NUMBER.match(path.name)
    title = TITLE.search(text)
    fields, current, lines = {}, None, []

    def close():
        if current is not None:
            fields[current] = "\n".join(lines).strip()

    for line in text.splitlines():
        h, lab = HEADING_FIELD.match(line), LABEL_FIELD.match(line)
        if h or lab:
            close()
            current, lines = (h or lab).group(1).lower(), []
            value = (h or lab).group(2).strip()
            if value:
                lines.append(value)
        elif ANY_HEADING.match(line):
            close()
            current, lines = None, []
        elif current is not None:
            lines.append(line)
    close()
    status_lines = [x for x in fields.get("status", "").splitlines() if x.strip()]
    status = status_lines[0].strip().strip("*_").strip().lower() if status_lines else ""
    return Adr(int(m.group(1)) if m else -1, title.group(1) if title else "", fields, status)


def _adrs(root):
    d = Path(root) / "docs" / "adr"
    return {p.name: p for p in sorted(d.glob("*.md"))} if d.is_dir() else {}


def new_adrs(workspace, fixture_ws):
    before = _adrs(fixture_ws)
    return [p for name, p in _adrs(workspace).items() if name not in before]


def changed_adrs(workspace, fixture_ws):
    """ADRs of the fixture that are missing or differ byte-wise in the workspace."""
    after = _adrs(workspace)
    return [p for name, p in _adrs(fixture_ws).items()
            if name not in after or after[name].read_bytes() != p.read_bytes()]


def ids(text):
    return set(ID.findall(text))
