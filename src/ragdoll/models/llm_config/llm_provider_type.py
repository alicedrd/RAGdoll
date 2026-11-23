from enum import StrEnum


class LLMProviderType(StrEnum):
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"
