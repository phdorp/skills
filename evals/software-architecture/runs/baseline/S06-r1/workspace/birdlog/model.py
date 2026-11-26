"""Domain model: a Sighting and the rules for creating one.

Pure Python, no I/O. Times are stored as UTC epoch seconds plus the local
UTC offset at the moment of observation, so the local date/time can be
reconstructed exactly for display and eBird export.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class Sighting:
    species: str
    place: str
    observed_at: int  # UTC epoch seconds
    utc_offset_min: int  # observer's local offset at observation time
    count: int
    id: int | None = None

    def local_time(self) -> datetime:
        tz = timezone(timedelta(minutes=self.utc_offset_min))
        return datetime.fromtimestamp(self.observed_at, tz)


def new_sighting(
    species: str,
    place: str,
    count: int = 1,
    when: datetime | None = None,
) -> Sighting:
    """Validate user input and build an unsaved Sighting.

    `when` may be naive (interpreted as local time) or timezone-aware.
    Defaults to now.
    """
    species = species.strip()
    place = place.strip()
    if not species:
        raise ValueError("species must not be empty")
    if not place:
        raise ValueError("place must not be empty")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise ValueError("count must be a positive integer")

    if when is None:
        aware = datetime.now().astimezone()
    elif when.tzinfo is None:
        aware = when.astimezone()  # naive: interpret as machine-local time
    else:
        aware = when  # keep the offset the observer gave; don't convert to local
    offset = aware.utcoffset()
    assert offset is not None  # astimezone() always yields a concrete offset
    return Sighting(
        species=species,
        place=place,
        observed_at=int(aware.timestamp()),
        utc_offset_min=int(offset.total_seconds() // 60),
        count=count,
    )
