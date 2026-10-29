"""HuggingFace embedding providers."""

from shards_ai_agents.rag.embeddings.providers.huggingface.huggingface_provider import (
    HuggingFaceProvider,
)
from shards_ai_agents.rag.embeddings.providers.huggingface.types import (
    HuggingFaceProviderConfig,
    HuggingFaceProviderSpec,
)


__all__ = [
    "HuggingFaceProvider",
    "HuggingFaceProviderConfig",
    "HuggingFaceProviderSpec",
]
