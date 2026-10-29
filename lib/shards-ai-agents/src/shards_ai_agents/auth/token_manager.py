"""Deprecated: use ``shards_ai_agents_core.token_manager`` instead."""

from __future__ import annotations

import warnings

from shards_ai_agents_core.token_manager import TokenManager as TokenManager


__all__ = ["TokenManager"]


warnings.warn(
    "shards_ai_agents.auth.token_manager is deprecated; import from shards_ai_agents_core.token_manager.",
    DeprecationWarning,
    stacklevel=2,
)
