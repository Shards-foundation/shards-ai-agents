"""Re-exports of version utilities from ``shards_ai_agents_core.version``.

Kept as a stable import path for the framework; new code should import from
``shards_ai_agents_core.version`` directly.
"""

from __future__ import annotations

from shards_ai_agents_core.version import (
    check_version as check_version,
    get_latest_version_from_pypi as get_latest_version_from_pypi,
    get_shards_ai_agents_version as get_shards_ai_agents_version,
    is_current_version_yanked as is_current_version_yanked,
    is_newer_version_available as is_newer_version_available,
)


__all__ = [
    "check_version",
    "get_latest_version_from_pypi",
    "get_shards_ai_agents_version",
    "is_current_version_yanked",
    "is_newer_version_available",
]
