from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from ragdoll.services.generator import ProviderType
from ragdoll.services.retriever import RetrieverType

class RagSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

    sql_db_url: str = Field(default = ...)

    llm_provider_type: ProviderType = ProviderType.GEMINI
    llm_provider_model: str = "gemini-2.5-flash"
    # default = ... prevents VS Code static type checking 
    # from believing Settings constructor needs llm_provider_api_key as a parameter
    llm_provider_api_key: str = Field(default = ...)
    llm_temperature: float = 0.2

    retriever_type: RetrieverType = RetrieverType.CHROMADB
    retriever_db_path: str = "./storage/chromadb/"
    retriever_collection_name: str = "docs"

    chat_prompt_limit: int = 2000

    chunk_size: int = 800
    chunk_overlap: int = 100

settings = RagSettings()