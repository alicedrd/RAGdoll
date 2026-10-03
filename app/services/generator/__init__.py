from enum import StrEnum

from .base_generator import BaseGenerator
from .gemini_generator import GeminiGenerator

class ProviderType(StrEnum):
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"

_GENERATORS: dict[ProviderType, type[BaseGenerator]] = {
    ProviderType.GEMINI: GeminiGenerator
}

def get_generator(type: ProviderType, **kwargs) -> BaseGenerator:
    cls = _GENERATORS.get(type)
    if cls is None:
        raise ValueError(f"Unknown LLM provider type: {type}")
    return cls(**kwargs)

__all__ = ["BaseGenerator", "ProviderType", "get_generator"]