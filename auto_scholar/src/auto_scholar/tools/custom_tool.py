from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class summarizeText(BaseTool):
    """Tool to summarize text."""
    name: str = "Summarize Text"
    description: str = (
        "Summarizes the provided text. Returns a concise summary of the input text."
    )
    args_schema: Type[BaseModel] = BaseModel

    def _run(self, text: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    
class addToVectorDB(BaseTool):
    """Tool to add text to a vector database."""
    name: str = "Add to VectorDB"
    description: str = (
        "Adds the provided text to a vector database. Returns a confirmation message."
    )
    args_schema: Type[BaseModel] = BaseModel

    def _run(self, text: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    
class getFromVectorDB(BaseTool):
    """Tool to retrieve text from a vector database."""
    name: str = "Get from VectorDB"
    description: str = (
        "Retrieves the provided text from a vector database. Returns the retrieved text."
    )
    args_schema: Type[BaseModel] = BaseModel

    def _run(self, text: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."



