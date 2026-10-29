"""OpenCLIP embedding providers."""

from shards_ai_agents.rag.embeddings.providers.openclip.openclip_provider import (
    OpenCLIPProvider,
)
from shards_ai_agents.rag.embeddings.providers.openclip.types import (
    OpenCLIPProviderConfig,
    OpenCLIPProviderSpec,
)


__all__ = [
    "OpenCLIPProvider",
    "OpenCLIPProviderConfig",
    "OpenCLIPProviderSpec",
]
