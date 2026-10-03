import mimetypes
from pathlib import Path
from typing import Annotated, Generator
from os.path import splitext
from os import SEEK_END

from fastapi import Depends, Request, UploadFile, File
from sqlalchemy.orm import Session, sessionmaker

from app.services.parser import SUPPORTED_MIME_TYPES
from app.services.rag import RagEngine
from app.services.retriever.base_retriever import BaseRetriever
from app.core.exceptions import UnsupportedDocTypeError, EmptyDocParsingError, OtherFileValidationError

def get_retriever_dep(request: Request) -> BaseRetriever:
    return request.app.state.retriever

def get_rag_engine_dep(request: Request) -> RagEngine:
    return request.app.state.rag_engine

def get_sql_session(request: Request) -> Generator[Session]:
    maker: sessionmaker = request.app.state.sql_session_maker
    session: Session = maker()
    try:
        yield session
    finally:
        session.close()

async def validate_and_read_pdf(
    file: Annotated[UploadFile, File(description="PDF file")]
) -> tuple[UploadFile, str, str, bytes]:
    if not file.filename:
        raise OtherFileValidationError()

    filename = file.filename
    orig_path = Path(filename)
    mime = mimetypes.guess_file_type(orig_path)[0]
    ext = orig_path.suffix.lower()
    if not mime:
        raise UnsupportedDocTypeError(filename, ext)
    if mime not in SUPPORTED_MIME_TYPES:
        raise UnsupportedDocTypeError(filename, ext)

    content = await file.read()
    if not content:
        raise EmptyDocParsingError(file.filename)

    return file, file.filename, mime, content


RetrieverDep = Annotated[BaseRetriever, Depends(get_retriever_dep)]
RagEngineDep = Annotated[RagEngine, Depends(get_rag_engine_dep)]
SqlSessionDep = Annotated[Session, Depends(get_sql_session)]
ValidatePdfDep = Annotated[tuple[UploadFile, str, str, bytes], Depends(validate_and_read_pdf)]