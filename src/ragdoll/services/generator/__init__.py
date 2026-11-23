from ragdoll.models.llm_config.llm_config import LLMConfig
from ragdoll.models.llm_config.llm_provider_type import LLMProviderType

from .base_generator import BaseGenerator
from .gemini_generator import GeminiGenerator

_GENERATORS: dict[LLMProviderType, type[BaseGenerator]] = {
    LLMProviderType.GEMINI: GeminiGenerator
}

def get_generator(config: LLMConfig) -> BaseGenerator:
    cls = _GENERATORS.get(config.provider)
    if cls is None:
        raise ValueError(f"Unknown LLM provider type: {config.provider}")
    return cls(config)

__all__ = ["BaseGenerator", "get_generator"]