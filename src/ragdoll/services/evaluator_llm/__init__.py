from collections.abc import Callable

from ragas.llms import InstructorBaseRagasLLM

from ragdoll.models.llm_config.llm_config import LLMConfig
from ragdoll.models.llm_config.llm_provider_type import LLMProviderType

from .gemini_eval_llm import get_gemini_eval_llm


_RAGAS_EVAL_LLM_FACTORIES: dict[LLMProviderType, Callable[[LLMConfig], InstructorBaseRagasLLM]] = {
    LLMProviderType.GEMINI: get_gemini_eval_llm
}

def get_evaluator_llm(config: LLMConfig) -> InstructorBaseRagasLLM:
    factory = _RAGAS_EVAL_LLM_FACTORIES.get(config.provider)
    if factory is None:
        raise ValueError(f"Unknown LLM provider type: {config.provider}")
    return factory(config)

__all__ = ["get_evaluator_llm"]