from pydantic import BaseModel
from datetime import datetime

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

class SearchResElement(BaseModel):
    extract: str
    similarity: float | None = None
    doc_id: str | None = None
    doc_name: str | None = None
    crated_at: datetime | None = None
