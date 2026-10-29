"""Deprecated: use ``shards_ai_agents_core.paths`` instead."""

from __future__ import annotations

import warnings

from shards_ai_agents_core.paths import (
    db_storage_path as db_storage_path,
    get_project_directory_name as get_project_directory_name,
)


__all__ = ["db_storage_path", "get_project_directory_name"]


warnings.warn(
    "shards_ai_agents.utilities.paths is deprecated; import from shards_ai_agents_core.paths.",
    DeprecationWarning,
    stacklevel=2,
)
