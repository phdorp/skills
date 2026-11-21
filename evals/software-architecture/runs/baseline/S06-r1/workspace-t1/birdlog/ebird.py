"""Export sightings in eBird's CSV record format.

Pure mapping (sighting -> row) plus one atomic file writer. Column names
follow eBird's bulk-import "Record Format"; verify against the current
eBird spec before release (see ARCHITECTURE.md, open questions).
"""

import csv
import io
import os
import sys
import tempfile
from pathlib import Path
from typing import Iterable, TextIO

from birdlog.model import Sighting

COLUMNS = [
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
    "Country Code",
    "Protocol",
    "Number of Observers",
    "Duration (Min)",
    "All Obs Reported",
    "Distance Traveled (km)",
    "Area Covered (ha)",
    "Submission Comments",
]


def to_row(s: Sighting) -> dict[str, object]:
    t = s.local_time()
    return {
        "Common Name": s.species,
        "Genus": "",  # TODO: scientific name lookup (open question)
        "Species": "",
        "Species Count": s.count,
        "Species Comments": "",
        "Location Name": s.place,
        "Latitude": "",  # TODO: not captured yet (open question)
        "Longitude": "",
        "Date": t.strftime("%m/%d/%Y"),
        "Start Time": t.strftime("%I:%M %p"),
        "State/Province": "",
        "Country Code": "",
        "Protocol": "Incidental",
        "Number of Observers": 1,
        "Duration (Min)": "",
        "All Obs Reported": "",
        "Distance Traveled (km)": "",
        "Area Covered (ha)": "",
        "Submission Comments": "",
    }


def render(sightings: Iterable[Sighting]) -> str:
    buf = io.StringIO()
    write_csv(sightings, buf)
    return buf.getvalue()


def write_csv(sightings: Iterable[Sighting], out: TextIO) -> None:
    writer = csv.DictWriter(out, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    for s in sightings:
        writer.writerow(to_row(s))


def write_atomic(path: Path, sightings: Iterable[Sighting]) -> None:
    """Write the CSV to a temp file in the same directory, fsync, then rename.

    A crash leaves either the old file or the complete new one, never a
    truncated export.
    """
    if str(path) == "-":
        write_csv(sightings, sys.stdout)
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            write_csv(sightings, f)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise
