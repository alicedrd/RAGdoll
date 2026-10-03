from abc import ABC, abstractmethod

from app.models.services.documents import AddDocsResponse

class BaseRetriever(ABC):
    @abstractmethod
    def add_docs(self: BaseRetriever, docs: list[str], doc_name: str) -> str:
        pass

    @abstractmethod
    def del_doc(self: BaseRetriever, doc_id: str):
        pass

    @abstractmethod
    def search(self: BaseRetriever, query: str, nb_results: int = 3) -> list[str]:
        pass

    def __query_failure(self: BaseRetriever):
        raise Exception("Cannot retrieve answer from collection")