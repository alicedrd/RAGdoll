# -- RAG engine main service class

import io
import logging
from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from ragdoll.core.exceptions import EmptyDocParsingError, DocNotFoundError, NoSearchResult
from ragdoll.models.registry.docrecord import DocRecord
from ragdoll.models.api.documents import AddDocsResponse
from ragdoll.models.api.chat import ChatResponse
from ragdoll.models.api.search import SearchResElement
from ragdoll.services.generator.base_generator import BaseGenerator
from ragdoll.services.parser import parse_doc
from ragdoll.services.chunker import chunk_text
from ragdoll.services.retriever.base_retriever import BaseRetriever
from ragdoll.utils import clean_name

logger = logging.getLogger(__name__)

class RagEngine:
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        self._retriever = retriever
        self._generator = generator

    # ingest a new document
    def ingest_doc(self, session: Session, content: bytes, doc_name: str, filename: str, mime: str) -> AddDocsResponse:
        if not doc_name.strip():
            logger.debug(f"No doc name specified, using filename {filename}")
            doc_name = filename
        doc_name = clean_name(doc_name)

        text = parse_doc(io.BytesIO(content), filename, mime)
        if not text.strip():
            raise EmptyDocParsingError(filename)
        
        chunks = chunk_text(text)
        chunk_count = len(chunks)
        doc_id = self._retriever.add_docs(chunks, doc_name)

        doc_record = DocRecord(
            id = doc_id,
            doc_name = doc_name,
            chunk_count = chunk_count,
            size_in_bytes = len(content),
            content_type = mime
        )
        try:
            session.add(doc_record)
            session.commit()
        except Exception:
            logger.error(f"SQL error during insertion of doc {doc_id} to DB, reverting vectorstore insertions")
            self._retriever.del_doc(doc_id)
            raise

        return AddDocsResponse(id = doc_id, doc_name = doc_name, chunk_count = chunk_count)

    # forget a document if it is stored
    def forget_doc(self, session: Session, doc_id: str):
        try:
            doc = session.get_one(DocRecord, doc_id)
        except NoResultFound as e:
            raise DocNotFoundError(doc_id, "SQL DB") from e
        # no point in catching other exceptions,
        # since exceptions that should trigger a 500 are already handled 
        # in exceptions.py:handle_sql_exception

        self._retriever.del_doc(doc_id)
        # if the doc can't be deleted by the vector store,
        # the following code won't ever be executed

        session.delete(doc)
        session.commit()
        # again, no point in catching here

    # retrieve list of stored documents
    def get_documents_list(self, session: Session) -> Sequence[DocRecord]:
        stmt = select(DocRecord).order_by(DocRecord.created_at.desc())
        docs = session.scalars(stmt).all()
        return docs

    # get info about a single document
    def get_document_info(self, session: Session, doc_id: str) -> DocRecord:
        try:
            doc = session.get_one(DocRecord, doc_id)
        except NoResultFound as e:
            raise DocNotFoundError(doc_id, "SQL DB") from e

        return doc

    # search extracts
    def search(self, query: str, top_k: int) -> list[SearchResElement]:
        context = self._retriever.search(query, nb_results = top_k)
        if len(context) == 0:
            raise NoSearchResult(query)

        return context

    # ask a question to the RAG
    def ask_question(self, question: str, top_k: int) -> ChatResponse:
        context = [c.extract for c in self._retriever.search(question, nb_results = top_k)]
        answer = self._generator.ask(question, context)
        return ChatResponse(answer = answer, sources = context)