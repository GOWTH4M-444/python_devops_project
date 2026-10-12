"""Utility functions for directory management, file checks, and DevOps reporting."""

import platform
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def ensure_directory(path: str | Path) -> Path:
    """Ensure that the given directory exists, creating parents if necessary."""
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target


def file_exists(path: str | Path) -> bool:
    """Check if a file or path exists."""
    return Path(path).exists()


def get_system_metadata() -> Dict[str, Any]:
    """Collect host system metadata for deployment environment auditing."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "system_time": datetime.now(timezone.utc).isoformat(),
    }
