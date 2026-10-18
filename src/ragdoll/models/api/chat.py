from pydantic import BaseModel, Field

from ragdoll.core.config import settings

# RAG Query models
class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length = 3,
        max_length = settings.chat_prompt_limit,
        description = "The question you want to ask the RAG",
        examples = ["What do the articles say about ML use in radiology ?"]
    )
    top_k: int = Field(
        default = 3,
        ge = 1, # min. 1,
        le = 15, # max. 15
        description = "Number of chunks of contexts to use to answer the question"
    )

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
