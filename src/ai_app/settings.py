"""Application runtime settings and shared constants."""

from __future__ import annotations

import os

from .utils.env import env_int


MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-7")
MAX_TOKENS = env_int("ANTHROPIC_MAX_TOKENS", 8096)
MAX_ITERATIONS = env_int("SUPERVISOR_MAX_ITERATIONS", 40)
