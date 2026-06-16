"""Environment parsing helpers shared across runtime modules."""

from __future__ import annotations

import os


def env_int(name: str, default: int) -> int:
    """Read an integer environment variable with safe fallback."""

    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default
