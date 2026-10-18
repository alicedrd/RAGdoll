from fastapi import APIRouter

from ragdoll.models.api.chat import ChatRequest, ChatResponse
from ragdoll.api.deps import RagEngineDep

router = APIRouter()

# RAG query
@router.post("", response_model = ChatResponse, tags = ["RAG"])
def ask_rag(request: ChatRequest, rag_engine: RagEngineDep) -> ChatResponse:
    res = rag_engine.ask_question(request.question, request.top_k)
    return res