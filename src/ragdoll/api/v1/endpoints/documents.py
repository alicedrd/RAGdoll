from io import BytesIO
from typing import Annotated
import logging
from fastapi import APIRouter, File, Form, UploadFile, status

from ragdoll.api.deps import RagEngineDep, RetrieverDep, ValidatePdfDep, SqlSessionDep
from ragdoll.models.api.documents import AddDocsResponse, DocRecordResElement
from ragdoll.utils import clean_name

logger = logging.getLogger(__name__)

router = APIRouter()

# get document list
@router.get(
    "", 
    response_model=list[DocRecordResElement]
)
async def get_docs_list(db_session: SqlSessionDep, rag_engine: RagEngineDep):
    # automatic Sequence[DocRecord] to list[DocRecordResElement] conversion thanks to pydantic !
    return rag_engine.get_documents_list(db_session)

# get info about one document
@router.get(
    "{doc_id}",
    response_model=DocRecordResElement
)
async def get_doc_info(db_session: SqlSessionDep, rag_engine: RagEngineDep, doc_id: str):
    return rag_engine.get_document_info(db_session, doc_id)

# add docs to RAG DB
@router.post(
    "", 
    response_model=AddDocsResponse, 
    status_code=status.HTTP_201_CREATED
)
async def add_docs(
    db_session: SqlSessionDep,
    rag_engine: RagEngineDep,
    file_data: ValidatePdfDep,
    file: Annotated[UploadFile, File(description = "Document to add to RAG database")],
    doc_name: Annotated[str, Form(description = "Name of the document")] = "" 
) -> AddDocsResponse:
    _, filename, mime, content = file_data
    res = rag_engine.ingest_doc(db_session, content, doc_name, filename, mime)
    return res

# delete doc from DB
@router.delete(
    "{doc_id}", 
    status_code=status.HTTP_204_NO_CONTENT
    )
async def del_doc(db_session: SqlSessionDep, rag_engine: RagEngineDep, doc_id: str):
    rag_engine.forget_doc(db_session, doc_id)