from typing import Literal

from pydantic import BaseModel, SecretStr

from .llm_provider_type import LLMProviderType

class GeminiConfig(BaseModel):
    provider: Literal[LLMProviderType.GEMINI] = LLMProviderType.GEMINI
    model: str = "gemini-2.5-flash"
    api_key: SecretStr
    temperature: float = 0.2