"""ONNX embedding providers."""

from shards_ai_agents.rag.embeddings.providers.onnx.onnx_provider import ONNXProvider
from shards_ai_agents.rag.embeddings.providers.onnx.types import (
    ONNXProviderConfig,
    ONNXProviderSpec,
)


__all__ = [
    "ONNXProvider",
    "ONNXProviderConfig",
    "ONNXProviderSpec",
]
