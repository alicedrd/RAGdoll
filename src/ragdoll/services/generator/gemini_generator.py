from fastapi import status
from google import genai
from google.genai import errors
import logging

from ragdoll.core.exceptions import AppException, ServiceOverloadError, PolicyViolatedError, GenerationExhaustedError, RemoteFailureError, RemoteTimeoutError, OtherGeneratorError, BlacklistViolationError
from ragdoll.services.generator.base_generator import BaseGenerator

logger = logging.getLogger(__name__)

class GeminiGenerator(BaseGenerator):
    def __init__(self , model : str, api_key: str | None = None, temperature: float = 0.2):
        logger.info('Initializing Gemini API client')
        logger.debug(f'Using system prompt : ${self._SYSTEM_PROMPT}')
        self._client = genai.Client(api_key = api_key)
        self._model = model
        self._TEMPERATURE = temperature

    # build exception from a blocked prompt/halted generation response
    def _build_exception_from_response(self, prompt: str, res: genai.types.GenerateContentResponse) -> AppException:
        # API may have blocked the prompt without even an attempt to generate a response
        if not res.candidates or len(res.candidates) == 0:
            block_reason = getattr(res.prompt_feedback, "block_reason", "EMPTY_REASON")
            if block_reason == "BLOCKLIST":
                logger.warning(f"Input prompt violated blocklist. Full prompt : {prompt}", exc_info=True)
                return BlacklistViolationError("Prompt violated internal blocklist")
            else:
                logger.warning(f"Input prompt or context violates Gemini content policy ({block_reason}).\nFull input prompt : {prompt}", exc_info=True)
                return PolicyViolatedError("Input prompt or context violates Gemini content policy")

        # text generation halted during generation
        finish_reason = getattr(res.candidates[0], "finish_reason", "UNKNOWN")
        if finish_reason in ["SAFETY", "RECITATION"]:
            logger.warning(f"During generation, response violated Gemini content/copyright policy ({finish_reason}). Full prompt: {prompt}", exc_info=True)
            return PolicyViolatedError("Gemini content or copyright policy violated during generation. This is probably imputable to prompt")
        elif finish_reason == "MAX_TOKENS":
            logger.critical(f"During generation, response exceed token limit. Prompt: {prompt}", exc_info=True)
            return OtherGeneratorError()
        else:
            logger.warning(f"Generation halted for unknown reasons", exc_info=True)
            return RemoteFailureError()

    # send a question to Gemini
    def ask(self, question: str, context: list[str]) -> str:
        user_prompt = f"""
            Context : {'\n'.join(context)}
            Question : {question}
        """

        chat = self._client.chats.create(
            model = self._model,
            config = genai.types.GenerateContentConfig(
                system_instruction = self._SYSTEM_PROMPT,
                temperature = self._TEMPERATURE
            )
        )

        logger.info(f'Sending query to model ${self._model}')
        try:
            res = chat.send_message(user_prompt)
        except errors.APIError as e:
            if e.code == status.HTTP_429_TOO_MANY_REQUESTS:
                logger.critical(f"Gemini API resource exhausted : {e.message}", exc_info = True)
                raise ServiceOverloadError("Too many requests or service overload : retry later.") from e
            elif e.code == status.HTTP_401_UNAUTHORIZED:
                logger.critical(f"Auth failure in Gemini API call ; check API key. {e.message}", exc_info=True)
                raise OtherGeneratorError() from e
            elif e.code == status.HTTP_400_BAD_REQUEST:
                logger.warning(f"Prompt returned Invalid argument error from Gemini API. May refer to use of a forbidden parameter or context overflow. {e.message}", exc_info=True)
                raise OtherGeneratorError() from e
            elif (e.code == status.HTTP_500_INTERNAL_SERVER_ERROR
                or e.code == status.HTTP_503_SERVICE_UNAVAILABLE):
                logger.warning(f"Gemini API unavailable : {e.message}", exc_info=True)
                raise RemoteFailureError() from e
            elif e.code == status.HTTP_504_GATEWAY_TIMEOUT:
                logger.warning(f"Gemini API call exceed timeout : {e.message}", exc_info = True)
                raise RemoteTimeoutError() from e
            else:
                logger.critical(f"Unknown error returned from Gemini API without attempt of text generation : {e.code}, {e.message}", exc_info=True)
                raise OtherGeneratorError() from e

        try:
            if not res.text:
                raise self._build_exception_from_response(user_prompt, res)
            return res.text
        except ValueError as e:
            raise self._build_exception_from_response(user_prompt, res) from e