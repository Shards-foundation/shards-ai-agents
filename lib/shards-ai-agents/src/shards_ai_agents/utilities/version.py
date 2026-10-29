"""Deprecated: use ``shards_ai_agents_core.version`` instead."""

from __future__ import annotations

import warnings

from shards_ai_agents_core.version import (
    get_shards_ai_agents_version as get_shards_ai_agents_version,
)


__all__ = ["get_shards_ai_agents_version"]


warnings.warn(
    "shards_ai_agents.utilities.version is deprecated; import from shards_ai_agents_core.version.",
    DeprecationWarning,
    stacklevel=2,
)
