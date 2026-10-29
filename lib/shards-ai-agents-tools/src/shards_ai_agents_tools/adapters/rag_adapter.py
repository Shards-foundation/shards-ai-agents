from typing import Any

from shards_ai_agents_tools.rag.core import RAG
from shards_ai_agents_tools.tools.rag.rag_tool import Adapter


class RAGAdapter(Adapter):
    def __init__(
        self,
        collection_name: str = "shards_ai_agents_knowledge_base",
        persist_directory: str | None = None,
        embedding_model: str = "text-embedding-3-small",
        top_k: int = 5,
        embedding_api_key: str | None = None,
        **embedding_kwargs: Any,
    ):
        super().__init__()

        embedding_config = {"api_key": embedding_api_key, **embedding_kwargs}

        self._adapter = RAG(
            collection_name=collection_name,
            persist_directory=persist_directory,
            embedding_model=embedding_model,
            top_k=top_k,
            embedding_config=embedding_config,
        )

    def query(self, question: str) -> str:  # type: ignore[override]
        return self._adapter.query(question)

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._adapter.add(*args, **kwargs)
