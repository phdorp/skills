"""Locate the per-user data directory on Linux, macOS and Windows.

Implemented by hand so that birdlog needs no third-party packages.
Set BIRDLOG_HOME to override (useful for tests and backups).
"""

import os
import sys
from pathlib import Path

APP_NAME = "birdlog"
DB_FILENAME = "birdlog.sqlite3"


def data_dir() -> Path:
    override = os.environ.get("BIRDLOG_HOME")
    if override:
        return Path(override).expanduser()

    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    return base / APP_NAME


def db_path() -> Path:
    return data_dir() / DB_FILENAME
