from io import BytesIO
from typing import Annotated
import logging
from fastapi import APIRouter, File, Form, UploadFile, status

from ragdoll.models.api.search import SearchRequest, SearchResElement
from ragdoll.api.deps import RagEngineDep, SqlSessionDep
from ragdoll.utils import clean_name

logger = logging.getLogger(__name__)

router = APIRouter()

# search contextual informations based on query
@router.post(
    "",
    response_model = list[SearchResElement]
)
async def search(
    rag_engine: RagEngineDep,
    session: SqlSessionDep,
    req: SearchRequest
):
    pass
    # todo