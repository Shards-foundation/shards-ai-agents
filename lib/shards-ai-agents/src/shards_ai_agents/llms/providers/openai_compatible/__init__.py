"""OpenAI-compatible providers module."""

from shards_ai_agents.llms.providers.openai_compatible.completion import (
    OPENAI_COMPATIBLE_PROVIDERS,
    OpenAICompatibleCompletion,
    ProviderConfig,
)


__all__ = [
    "OPENAI_COMPATIBLE_PROVIDERS",
    "OpenAICompatibleCompletion",
    "ProviderConfig",
]
