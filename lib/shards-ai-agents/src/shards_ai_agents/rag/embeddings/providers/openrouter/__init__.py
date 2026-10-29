"""OpenRouter embedding providers."""

from shards_ai_agents.rag.embeddings.providers.openrouter.openrouter_provider import (
    OpenRouterProvider,
)
from shards_ai_agents.rag.embeddings.providers.openrouter.types import (
    OpenRouterProviderConfig,
    OpenRouterProviderSpec,
)


__all__ = [
    "OpenRouterProvider",
    "OpenRouterProviderConfig",
    "OpenRouterProviderSpec",
]
