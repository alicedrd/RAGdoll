from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from ragdoll.models.llm_config.llm_config import LLMConfig
from ragdoll.services.retriever import RetrieverType


class RagSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_nested_delimiter = "__",
        env_file_encoding = "utf-8"
    )

    sql_db_url: str = Field(default = ...)
    
    rag_llm: LLMConfig = Field(default = ...)
    eval_llm: LLMConfig | None = None

    retriever_type: RetrieverType = RetrieverType.CHROMADB
    retriever_db_path: str = "./storage/chromadb/"
    retriever_collection_name: str = "docs"

    chat_prompt_limit: int = 2000

    chunk_size: int = 800
    chunk_overlap: int = 100

settings = RagSettings()