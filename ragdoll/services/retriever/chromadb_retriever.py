## - Retriever class

import chromadb
import logging
import uuid

from ragdoll.models.api.search import SearchResElement
from ragdoll.core.exceptions import DocNotFoundError
from ragdoll.services.retriever.base_retriever import BaseRetriever

logger = logging.getLogger(__name__)

class ChromaDBRetriever(BaseRetriever):
    def __init__(self: ChromaDBRetriever, db_path: str, collection_name: str = 'docs'):
        self._client = chromadb.PersistentClient(path = db_path)
        self._collection = self._client.get_or_create_collection(collection_name)

    def add_docs(self: ChromaDBRetriever, docs: list[str], doc_name: str) -> str:
        logger.info(f'Adding document {doc_name} to ChromaDB database')
        doc_id = str(uuid.uuid4())
        self._collection.add(
            ids = [f"{doc_id}_{str(i)}" for i in range(len(docs))],
            documents = docs,
            metadatas = [{
                "doc_id": doc_id,
                "filename": doc_name,
                "chunk_index": i
            } for i in range(len(docs))]
        )
        return doc_id

    def del_doc(self: ChromaDBRetriever, doc_id: str):
        logger.info(f'Deleting document {doc_id} from ChromaDB database')
        delete_result = self._collection.delete(where = {"doc_id": doc_id})
        if delete_result["deleted"] <= 0:
            raise DocNotFoundError(doc_id, "vector store")

    def search(self: ChromaDBRetriever, query: str, nb_results: int = 3) -> list[SearchResElement]:
        logger.info(f'Sending query to ChromaDB for {nb_results}')
        results = self._collection.query(query_texts = [query], n_results = nb_results)
        docs = results['documents']
        if docs is None:
            logger.warning('Nothing found in ChromaDB database !')
            return []
        else:
            return [SearchResElement(extract = d) for d in docs[0]]