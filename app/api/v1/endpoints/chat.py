from fastapi import APIRouter

from app.models.services.chat import ChatRequest, ChatResponse
from app.api.deps import RagEngineDep

router = APIRouter()

# RAG query
@router.post("/", response_model = ChatResponse, tags = ["RAG"])
def ask_rag(request: ChatRequest, rag_engine: RagEngineDep) -> ChatResponse:
    res = rag_engine.ask_question(request.question, request.top_k)
    return res