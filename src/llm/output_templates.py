from pydantic import BaseModel, Field
from typing import List


# This file has the following Response Templates for structured outputs

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
