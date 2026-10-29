"""Jina embedding providers."""

from shards_ai_agents.rag.embeddings.providers.jina.jina_provider import JinaProvider
from shards_ai_agents.rag.embeddings.providers.jina.types import (
    JinaProviderConfig,
    JinaProviderSpec,
)


__all__ = [
    "JinaProvider",
    "JinaProviderConfig",
    "JinaProviderSpec",
]
