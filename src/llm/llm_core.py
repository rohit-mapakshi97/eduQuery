from typing import Dict, Any, Tuple, List
from langchain_core.language_models import BaseChatModel
from src.keys import OpenAPIConfig, GeminiAPIConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


# from langchain.chat_models import AzureChatOpenAI

class LLMNotSupportedError(Exception):
    pass


class LLMFactory:
    """
    Initializes the base LLM from the provided configuration
    """

    DEFAULT_LLM = 'default_llm'
    LLMS = 'llms'
    LLM_GEMINI = 'gemini'
    LLM_OPEN_AI = 'openai'
    LLM_MODEL = 'model'
    LLM_TEMPERATURE = 'temperature'
    LLM_MAX_RETRIES = 'max_retries'

    def get_LLM(self, cfg: Dict[str, Any]) -> BaseChatModel:
        llm = None

        if cfg[self.DEFAULT_LLM] == self.LLM_GEMINI:
            cfg_gemini = cfg[self.LLMS][self.LLM_GEMINI]
            llm = ChatGoogleGenerativeAI(
                api_key=GeminiAPIConfig.GEMINI_API_KEY,
                model=cfg_gemini[self.LLM_MODEL],
                max_retries=cfg_gemini[self.LLM_MAX_RETRIES]
            )
        elif cfg[self.DEFAULT_LLM] == self.LLM_OPEN_AI:
            # TODO Similarly initialize and return Open AI model
            pass
        else:
            logger.error(f'LLM: {cfg[self.DEFAULT_LLM]} not supported')
            raise LLMNotSupportedError()
        return llm


class PromptRepository:
    """
    Repository for storing and managing LLM prompts used in the pipeline.
    This is a Singleton Class.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PromptRepository, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        self.prompts = self._load_prompts()

    def get_ner_prompt(self) -> ChatPromptTemplate:
        """
        Returns the prompt for Named Entity Recognition
        """
        return ChatPromptTemplate.from_messages(
            self._prepare_prompt('entityRecognition')
        )

    def get_cypher_prompt(self) -> ChatPromptTemplate:
        """
        Returns the prompt used for creating Cypher Query
        """
        return ChatPromptTemplate.from_messages(
            self._prepare_prompt('cypherPrompt')
        )

    def get_response_prompt(self) -> ChatPromptTemplate:
        """
        Returns the prompt for generating the final response
        """
        return ChatPromptTemplate.from_messages(
            self._prepare_prompt('responsePrompt')
        )

    def _load_prompts(self) -> Dict[str, Any]:
        file_path = Path(__file__).resolve().parent / 'prompts.json'
        with open(file_path, 'r') as file:
            return json.load(file)

    def _prepare_prompt(self, key: str) -> List[Tuple[str, str]]:
        def _concat(lines: list) -> str:
            return ' \n '.join(lines)

        system = ("system", _concat(self.prompts[key]["system"]))
        human = ("human", _concat(self.prompts[key]["human"]))
        return [system, human]
