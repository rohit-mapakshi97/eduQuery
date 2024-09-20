from pydantic import BaseModel, Field
from typing import List

# This file has all the LLM tools that are used as signals to the LLM

class Entities(BaseModel):
    """Identifying information about entities."""

    names: List[str] = Field(
        ...,
        description="All the Students or Assessments or Modules or Instructors or Courses appearing in the text",
    )
