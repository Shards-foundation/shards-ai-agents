"""Type definitions for the embeddings module."""

from typing import Any, Literal, TypeAlias

from shards_ai_agents.rag.core.base_embeddings_provider import BaseEmbeddingsProvider
from shards_ai_agents.rag.embeddings.providers.aws.types import BedrockProviderSpec
from shards_ai_agents.rag.embeddings.providers.cohere.types import CohereProviderSpec
from shards_ai_agents.rag.embeddings.providers.custom.types import CustomProviderSpec
from shards_ai_agents.rag.embeddings.providers.google.types import (
    GenerativeAiProviderSpec,
    VertexAIProviderSpec,
)
from shards_ai_agents.rag.embeddings.providers.huggingface.types import (
    HuggingFaceProviderSpec,
)
from shards_ai_agents.rag.embeddings.providers.ibm.types import (
    WatsonXProviderSpec,
)
from shards_ai_agents.rag.embeddings.providers.instructor.types import (
    InstructorProviderSpec,
)
from shards_ai_agents.rag.embeddings.providers.jina.types import JinaProviderSpec
from shards_ai_agents.rag.embeddings.providers.microsoft.types import AzureProviderSpec
from shards_ai_agents.rag.embeddings.providers.ollama.types import OllamaProviderSpec
from shards_ai_agents.rag.embeddings.providers.onnx.types import ONNXProviderSpec
from shards_ai_agents.rag.embeddings.providers.openai.types import OpenAIProviderSpec
from shards_ai_agents.rag.embeddings.providers.openclip.types import (
    OpenCLIPProviderSpec,
)
from shards_ai_agents.rag.embeddings.providers.openrouter.types import (
    OpenRouterProviderSpec,
)
from shards_ai_agents.rag.embeddings.providers.oracle.types import OracleProviderSpec
from shards_ai_agents.rag.embeddings.providers.roboflow.types import (
    RoboflowProviderSpec,
)
from shards_ai_agents.rag.embeddings.providers.sentence_transformer.types import (
    SentenceTransformerProviderSpec,
)
from shards_ai_agents.rag.embeddings.providers.text2vec.types import (
    Text2VecProviderSpec,
)
from shards_ai_agents.rag.embeddings.providers.voyageai.types import (
    VoyageAIProviderSpec,
)


ProviderSpec: TypeAlias = (
    AzureProviderSpec
    | BedrockProviderSpec
    | CohereProviderSpec
    | CustomProviderSpec
    | GenerativeAiProviderSpec
    | HuggingFaceProviderSpec
    | InstructorProviderSpec
    | JinaProviderSpec
    | OllamaProviderSpec
    | ONNXProviderSpec
    | OpenAIProviderSpec
    | OpenCLIPProviderSpec
    | OpenRouterProviderSpec
    | OracleProviderSpec
    | RoboflowProviderSpec
    | SentenceTransformerProviderSpec
    | Text2VecProviderSpec
    | VertexAIProviderSpec
    | VoyageAIProviderSpec
    | WatsonXProviderSpec
)

AllowedEmbeddingProviders = Literal[
    "azure",
    "amazon-bedrock",
    "cohere",
    "custom",
    "google-generativeai",
    "google-vertex",
    "huggingface",
    "instructor",
    "jina",
    "ollama",
    "onnx",
    "openai",
    "openclip",
    "openrouter",
    "oracle",
    "roboflow",
    "sentence-transformer",
    "text2vec",
    "voyageai",
    "watsonx",
]

EmbedderConfig: TypeAlias = (
    ProviderSpec | BaseEmbeddingsProvider[Any] | type[BaseEmbeddingsProvider[Any]]
)
