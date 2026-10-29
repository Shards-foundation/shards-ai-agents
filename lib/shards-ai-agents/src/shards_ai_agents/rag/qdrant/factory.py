"""Factory functions for creating Qdrant clients from configuration."""

from qdrant_client import QdrantClient as SyncQdrantClientBase

from shards_ai_agents.rag.qdrant.client import QdrantClient
from shards_ai_agents.rag.qdrant.config import QdrantConfig


def create_client(config: QdrantConfig) -> QdrantClient:
    """Create a Qdrant client from configuration.

    Args:
        config: The Qdrant configuration.

    Returns:
        A configured QdrantClient instance.
    """

    qdrant_client = SyncQdrantClientBase(**config.options)
    return QdrantClient(
        client=qdrant_client,
        embedding_function=config.embedding_function,
        default_limit=config.limit,
        default_score_threshold=config.score_threshold,
        default_batch_size=config.batch_size,
    )
