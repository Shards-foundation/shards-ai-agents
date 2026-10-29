"""The old experimental namespace must keep re-exporting the public names."""


def test_experimental_namespace_reexports_public_names():
    from shards_ai_agents.experimental import skills as experimental_skills
    from shards_ai_agents.skills.cache import SkillCacheManager
    from shards_ai_agents.skills.registry import (
        is_registry_ref,
        parse_registry_ref,
        resolve_registry_ref,
    )

    assert experimental_skills.SkillCacheManager is SkillCacheManager
    assert experimental_skills.is_registry_ref is is_registry_ref
    assert experimental_skills.parse_registry_ref is parse_registry_ref
    assert experimental_skills.resolve_registry_ref is resolve_registry_ref


def test_experimental_submodule_imports_alias_real_modules():
    """Old submodule import style must resolve to the shards_ai_agents.skills modules."""
    import importlib

    from shards_ai_agents.experimental.skills import cache as shim_cache
    from shards_ai_agents.experimental.skills import events as shim_events
    from shards_ai_agents.experimental.skills import registry as shim_registry
    from shards_ai_agents.experimental.skills.cache import SkillCacheManager
    from shards_ai_agents.experimental.skills.registry import resolve_registry_ref
    from shards_ai_agents.skills import cache as real_cache
    from shards_ai_agents.skills import events as real_events
    from shards_ai_agents.skills import registry as real_registry

    assert shim_cache is real_cache
    assert shim_events is real_events
    assert shim_registry is real_registry
    assert SkillCacheManager is real_cache.SkillCacheManager
    assert resolve_registry_ref is real_registry.resolve_registry_ref
    # Dotted-path import resolves through sys.modules to the same module.
    assert (
        importlib.import_module("shards_ai_agents.experimental.skills.registry")
        is real_registry
    )
