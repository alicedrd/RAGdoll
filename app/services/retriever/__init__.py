from enum import StrEnum

from .base_retriever import BaseRetriever
from .chromadb_retriever import ChromaDBRetriever

class RetrieverType(StrEnum):
    CHROMADB = "chromadb"

_RETRIEVERS: dict[RetrieverType, type[BaseRetriever]] = {
    RetrieverType.CHROMADB: ChromaDBRetriever
}

def get_retriever(type: RetrieverType, **kwargs) -> BaseRetriever:
    cls = _RETRIEVERS.get(type)
    if cls is None:
        raise ValueError(f"Unknown docs retriever type: {type}")
    return cls(**kwargs)

__all__ = ["BaseRetriever", "RetrieverType", "get_retriever"]