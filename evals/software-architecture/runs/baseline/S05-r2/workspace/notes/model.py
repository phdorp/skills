from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: str
    text: str
    created: str
