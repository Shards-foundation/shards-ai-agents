"""Deprecated: use ``shards_ai_agents_core.lock_store`` instead."""

from __future__ import annotations

import warnings

from shards_ai_agents_core.lock_store import lock as lock


__all__ = ["lock"]


warnings.warn(
    "shards_ai_agents.utilities.lock_store is deprecated; import from shards_ai_agents_core.lock_store.",
    DeprecationWarning,
    stacklevel=2,
)
