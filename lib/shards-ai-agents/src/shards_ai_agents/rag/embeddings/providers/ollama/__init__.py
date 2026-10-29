"""Ollama embedding providers."""

from shards_ai_agents.rag.embeddings.providers.ollama.ollama_provider import (
    OllamaProvider,
)
from shards_ai_agents.rag.embeddings.providers.ollama.types import (
    OllamaProviderConfig,
    OllamaProviderSpec,
)


__all__ = [
    "OllamaProvider",
    "OllamaProviderConfig",
    "OllamaProviderSpec",
]
