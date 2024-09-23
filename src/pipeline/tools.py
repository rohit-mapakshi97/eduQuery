from typing import Optional, Type
from langchain_core.callbacks import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from typing import Any


# This file has various tools that the LLM can use to give complex responses
# These tools follow the Strategy Design Pattern.
# Based on our backend, we can pass strategies to query the relevant information

class QueryStrategy(ABC):
    @abstractmethod
    def get_information(self, entity: str) -> str:
        pass


# Tool 1: To process questions like: How is the student performing
class StudentInformation(BaseModel):
    entity: str = Field(description="Student mentioned in the question")


class StudentPerformanceTool(BaseTool):
    def __init__(self, query_strategy: QueryStrategy, **kwargs: Any):
        super().__init__(**kwargs)
        self.query_strategy = query_strategy

    name = "Student Performance"
    description = (
        "useful for when you need to answer questions about various actors or movies"
    )
    args_schema: Type[BaseModel] = StudentInformation

    def _run(
            self,
            entity: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return self.query_strategy.get_information(entity)

    async def _arun(
            self,
            entity: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return self.query_strategy.get_information(entity)
