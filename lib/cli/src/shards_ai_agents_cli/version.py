"""Re-exports of version utilities from ``shards_ai_agents_core.version``.

Kept as a stable import path for the CLI; new code should import from
``shards_ai_agents_core.version`` directly.
"""

from __future__ import annotations

from packaging.version import Version
from shards_ai_agents_core.version import (
    check_version as check_version,
    get_latest_version_from_pypi as get_latest_version_from_pypi,
    get_shards_ai_agents_version as get_shards_ai_agents_version,
    is_current_version_yanked as is_current_version_yanked,
    is_newer_version_available as is_newer_version_available,
)

from shards_ai_agents_cli import __version__ as _shards_ai_agents_cli_version


def get_shards_ai_agents_dependency_range(current_version: str | None = None) -> str:
    """Return the supported Shards-ai-agents dependency range for generated projects."""
    parsed_version = Version(current_version or _shards_ai_agents_cli_version)
    return f">={parsed_version},<{parsed_version.major + 1}.0.0"


def get_shards_ai_agents_tools_dependency(current_version: str | None = None) -> str:
    """Return the generated-project dependency for Shards-ai-agents with tools."""
    return f"shards-ai-agents[tools]{get_shards_ai_agents_dependency_range(current_version)}"


__all__ = [
    "check_version",
    "get_latest_version_from_pypi",
    "get_shards_ai_agents_dependency_range",
    "get_shards_ai_agents_tools_dependency",
    "get_shards_ai_agents_version",
    "is_current_version_yanked",
    "is_newer_version_available",
]
