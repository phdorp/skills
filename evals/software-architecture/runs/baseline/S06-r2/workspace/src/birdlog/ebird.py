"""Export sightings to eBird's bulk-import CSV ("eBird Record Format").

Each sighting becomes one single-species Incidental checklist row. Dates and
times are written by hand rather than with ``strftime`` because ``%-I`` is
not available on Windows.
"""

from __future__ import annotations

import csv
from datetime import datetime
from typing import IO, Iterable, List, Optional

from .store import Sighting

HEADER = [
    "Common Name",
    "Genus",
    "Species",
    "Species Count",
    "Species Comments",
    "Location Name",
    "Latitude",
    "Longitude",
    "Date",
    "Start Time",
    "State/Province",
    "Country",
    "Protocol",
    "Number of Observers",
    "Duration (Min)",
    "All Obs Reported",
    "Distance Traveled (km)",
    "Area Covered (ha)",
    "Observation Details",
    "Checklist Comments",
    "ML Catalog Numbers",
]


def write_ebird_csv(sightings: Iterable[Sighting], out: IO[str]) -> None:
    """Write ``sightings`` as eBird CSV. ``out`` should be opened with newline=''."""
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(HEADER)
    for s in sightings:
        writer.writerow(_row(s))


def _row(s: Sighting) -> List[object]:
    return [
        s.species,            # Common Name (must match eBird taxonomy; see ARCHITECTURE.md)
        "",                   # Genus
        "",                   # Species (scientific)
        s.count,              # Species Count
        "",                   # Species Comments
        s.location,           # Location Name
        _coord(s.latitude),
        _coord(s.longitude),
        _date(s.observed_at),
        _time(s.observed_at),
        "",                   # State/Province
        "",                   # Country
        "Incidental",         # Protocol
        1,                    # Number of Observers
        "",                   # Duration (Min)
        "N",                  # All Obs Reported
        "",                   # Distance Traveled (km)
        "",                   # Area Covered (ha)
        "",                   # Observation Details
        "",                   # Checklist Comments
        "",                   # ML Catalog Numbers
    ]


def _coord(value: Optional[float]) -> str:
    return "" if value is None else f"{value:.6f}"


def _date(dt: datetime) -> str:
    return f"{dt.month:02d}/{dt.day:02d}/{dt.year}"


def _time(dt: datetime) -> str:
    hour12 = dt.hour % 12 or 12
    suffix = "AM" if dt.hour < 12 else "PM"
    return f"{hour12}:{dt.minute:02d} {suffix}"
