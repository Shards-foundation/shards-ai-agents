"""AWS embedding providers."""

from shards_ai_agents.rag.embeddings.providers.aws.bedrock import BedrockProvider
from shards_ai_agents.rag.embeddings.providers.aws.types import (
    BedrockProviderConfig,
    BedrockProviderSpec,
)


__all__ = [
    "BedrockProvider",
    "BedrockProviderConfig",
    "BedrockProviderSpec",
]
