from typing import Dict, Any
from langchain_core.language_models import BaseChatModel
from src.api_keys import GeminiAPIConfig
from langchain_google_genai import ChatGoogleGenerativeAI
import logging

logger = logging.getLogger(__name__)


class LLMNotSupportedError(Exception):
    pass


class LLMFactory:
    """
    Initializes the base LLM from the provided configuration
    """

    USE_LLM = 'use_llm'
    LLM = 'llm'
    LLM_GEMINI = 'gemini'
    LLM_OPEN_AI = 'openai'
    LLM_MODEL = 'model'
    LLM_TEMPERATURE = 'temperature'
    LLM_MAX_RETRIES = 'max_retries'

    def get_LLM(self, llm_provider: str, cfg: Dict[str, Any]) -> BaseChatModel:
        llm = None

        if llm_provider == self.LLM_GEMINI:
            llm = ChatGoogleGenerativeAI(
                api_key=GeminiAPIConfig.GEMINI_API_KEY,
                model=cfg[self.LLM_MODEL],
                max_retries=cfg[self.LLM_MAX_RETRIES]
            )
        elif cfg[self.USE_LLM] == self.LLM_OPEN_AI:
            # TODO Similarly initialize and return Open AI model
            pass
        else:
            logger.error(f'LLM: {cfg[self.USE_LLM]} not supported')
            raise LLMNotSupportedError()
        return llm
