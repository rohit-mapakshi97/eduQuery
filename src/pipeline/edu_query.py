import json
from pathlib import Path

from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Dict

# This Module has the following:
# Abstract Class for EduQuery which can be used to write pipelines for different backend systems
# Pydantic templates used within the pipeline
# Prompt Repository that manages the LLM prompts (uses app_config.yaml)

class EduQuery(ABC):
    """
    Abstract class for EduQuery Pipeline, defines the core methods that need to be implemented by any subclass.
    """

    @abstractmethod
    def ask(self, question: str, verbose: bool = False) -> str:
        """
        Processes a natural language question through the query pipeline and returns the response.
        If `verbose` is set to True, it provides detailed output of each step.
        """
        pass

    @abstractmethod
    def prepare_ner_chain(self) -> Any:
        """
        Prepares a Named Entity Recognition chain using prompts and the LLM.
        Returns a chain that processes the input question to identify entities.
        """
        pass

    @abstractmethod
    def map_to_database(self, values: List[str]) -> str:
        """
        Matches the provided list of entity names to nodes in the Neo4j database.
        Returns a formatted string describing the mapping results for each entity.
        """
        pass

    @abstractmethod
    def prepare_cypher_response(self, entity_chain: Any) -> Any:
        """
        Prepares the Cypher query response chain based on the identified entities and database matches.
        It generates a Cypher query and processes it with the LLM.
        """
        pass

    @abstractmethod
    def prepare_response_chain(self, cypher_response: Any) -> Any:
        """
        Validates the generated Cypher query and prepares the final response chain.
        Integrates validation and response generation steps to produce the output.
        """
        pass

    @abstractmethod
    def prepare_edu_query_chain(self) -> Any:
        """
        Combines the NER chain, Cypher query generation, and response preparation into one pipeline.
        """
        pass


class Entities(BaseModel):
    """Identifying information about entities."""

    names: List[str] = Field(
        ...,
        description="All the Students or Assessments or Modules or Instructors or Courses appearing in the text",
    )


# [TODO]
# class FinalResponse(BaseModel):
#     """Final Response"""
#     question: str = Field(
#         ...,
#         description="Question asked by the user"
#     )
#
#     cypher_query: str = Field(
#         ...,
#         description="Cypher Query that was generated to answer the question"
#     )
#
#     answer: str = Field(
#         ...,
#         description="Final Answer that was generated to answer the question"
#     )
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

    def get_ner_prompt(self) -> Tuple[str, str]:
        """
        Returns the prompt for Named Entity Recognition
        """
        return self._prepare_prompt('entityRecognition')

    def get_cypher_prompt(self) -> Tuple[str, str]:
        """
        Returns the prompt used for creating Cypher Query
        """
        return self._prepare_prompt('cypherPrompt')

    def get_response_prompt(self) -> Tuple[str, str]:
        """
        Returns the prompt for generating the final response
        """
        return self._prepare_prompt('responsePrompt')

    def _load_prompts(self) -> Dict[str, Any]:
        file_path = Path(__file__).resolve().parent / 'prompts' / 'graph_prompts.json'
        with open(file_path, 'r') as file:
            return json.load(file)

    def _prepare_prompt(self, key: str) -> Tuple[str, str]:
        def _concat(lines: list) -> str:
            return ' \n '.join(lines)

        system = _concat(self.prompts[key]["system"])
        human = _concat(self.prompts[key]["human"])
        return system, human
