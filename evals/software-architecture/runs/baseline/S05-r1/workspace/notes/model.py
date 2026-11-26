from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: str  # the file name without ".txt"
    text: str
    created: str
