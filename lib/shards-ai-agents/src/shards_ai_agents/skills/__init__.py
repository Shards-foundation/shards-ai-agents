"""Agent Skills standard implementation for Shards-ai-agents.

Provides filesystem-based skill packaging with progressive disclosure, plus
the registry-backed Skills Repository (`@org/name` refs, global cache,
downloads).
"""

from shards_ai_agents.skills.cache import SkillCacheManager
from shards_ai_agents.skills.loader import (
    activate_skill,
    discover_skills,
    load_skill,
    load_skills,
)
from shards_ai_agents.skills.models import Skill, SkillFrontmatter
from shards_ai_agents.skills.parser import SkillParseError
from shards_ai_agents.skills.registry import (
    SkillRef,
    is_registry_ref,
    parse_registry_ref,
    parse_skill_ref,
    resolve_registry_ref,
)


__all__ = [
    "Skill",
    "SkillCacheManager",
    "SkillFrontmatter",
    "SkillParseError",
    "SkillRef",
    "activate_skill",
    "discover_skills",
    "is_registry_ref",
    "load_skill",
    "load_skills",
    "parse_registry_ref",
    "parse_skill_ref",
    "resolve_registry_ref",
]
