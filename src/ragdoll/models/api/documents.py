from typing import Annotated

from fastapi import File, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

# AddDocsRequest can't be a model,
# because it involves FastAPI's UploadFile and Form

class AddDocsResponse(BaseModel):
    doc_name: str
    id: str
    chunk_count: int

class DocRecordResElement(BaseModel):
    # allows this pydantic model to be built directly
    # from our SQL model
    model_config = ConfigDict(from_attributes = True)

    id: str
    doc_name: str
    chunk_count: int
    size_in_bytes: int
    content_type: str
    created_at: datetime