"""Microsoft embedding providers."""

from shards_ai_agents.rag.embeddings.providers.microsoft.azure import (
    AzureProvider,
)
from shards_ai_agents.rag.embeddings.providers.microsoft.types import (
    AzureProviderConfig,
    AzureProviderSpec,
)


__all__ = [
    "AzureProvider",
    "AzureProviderConfig",
    "AzureProviderSpec",
]
