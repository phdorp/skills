"""Dates as users type them: 2026-11-25, today, tomorrow, +3d, +2w."""
import re
from datetime import date, timedelta

RELATIVE = re.compile(r"^\+(\d+)([dw])$")


def parse(text, today=None):
    today = today or date.today()
    text = text.strip().lower()
    if text == "today":
        return today
    if text == "tomorrow":
        return today + timedelta(days=1)
    m = RELATIVE.match(text)
    if m:
        n = int(m.group(1))
        return today + timedelta(days=n if m.group(2) == "d" else 7 * n)
    return date.fromisoformat(text)
