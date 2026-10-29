"""Custom embeddings provider for user-defined embedding functions."""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from shards_ai_agents.rag.core.base_embeddings_provider import BaseEmbeddingsProvider
from shards_ai_agents.rag.embeddings.providers.custom.embedding_callable import (
    CustomEmbeddingFunction,
)


class CustomProvider(BaseEmbeddingsProvider[CustomEmbeddingFunction]):
    """Custom embeddings provider for user-defined embedding functions."""

    embedding_callable: type[CustomEmbeddingFunction] = Field(
        ..., description="Custom embedding function class"
    )

    model_config = SettingsConfigDict(extra="allow")
