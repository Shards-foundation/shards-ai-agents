"""Deprecated location for the Skills Repository.

The registry-backed skills feature graduated out of experimental; it now
lives in `shards_ai_agents.skills` alongside the filesystem-based loader. This module
re-exports the public names and aliases the old submodules so imports
written against the experimental namespace keep working, and will be
removed in a future release.
"""

import sys

from shards_ai_agents.skills import cache, events, registry
from shards_ai_agents.skills.cache import SkillCacheManager
from shards_ai_agents.skills.registry import (
    SkillRef,
    is_registry_ref,
    parse_registry_ref,
    parse_skill_ref,
    resolve_registry_ref,
)


# Keep `shards_ai_agents.experimental.skills.<module>` imports (and patch targets)
# resolving to the real modules in shards_ai_agents.skills.
sys.modules[__name__ + ".cache"] = cache
sys.modules[__name__ + ".events"] = events
sys.modules[__name__ + ".registry"] = registry

__all__ = [
    "SkillCacheManager",
    "SkillRef",
    "cache",
    "events",
    "is_registry_ref",
    "parse_registry_ref",
    "parse_skill_ref",
    "registry",
    "resolve_registry_ref",
]
