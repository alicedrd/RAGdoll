from ragas.llms import InstructorBaseRagasLLM, llm_factory
from google import genai

from ragdoll.models.llm_config.llm_config import LLMConfig
from ragdoll.models.llm_config.llm_provider_type import LLMProviderType


def get_gemini_eval_llm(config: LLMConfig) -> InstructorBaseRagasLLM:
    client = genai.Client(api_key = config.api_key.get_secret_value())
    return llm_factory(model = config.model, client = client)