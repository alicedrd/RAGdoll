from enum import StrEnum
from typing import Annotated, Union

from pydantic import Field

from .gemini_config import GeminiConfig

LLMConfig = Annotated[
    GeminiConfig,
    # pydantic va déteminer par le champ "provider" quel model utiliser (grâce au Literal)
    Field(discriminator="provider"),
]