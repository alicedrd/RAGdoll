from fastapi import APIRouter

from ragdoll.models.api.chat import ChatRequest, ChatResponse
from ragdoll.api.deps import RagEngineDep, SqlSessionDep

router = APIRouter()

# RAG query
@router.post("", response_model = ChatResponse, tags = ["RAG"])
def ask_rag(request: ChatRequest, rag_engine: RagEngineDep, sql_session: SqlSessionDep) -> ChatResponse:
    res = rag_engine.ask_question(request.question, request.top_k, sql_session)
    return res